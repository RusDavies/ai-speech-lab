#!/usr/bin/env python3
"""Validate, summarize, and run AI Speech Lab benchmark cases."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shlex
import sys
import time
import uuid
from pathlib import Path
from subprocess import CompletedProcess
import subprocess
from typing import Any


REQUIRED_FIELDS = {"id", "category", "text", "expected_focus", "tags"}


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc

        missing = REQUIRED_FIELDS - set(case)
        if missing:
            raise ValueError(f"{path}:{line_number}: missing fields: {', '.join(sorted(missing))}")
        if not isinstance(case["id"], str) or not case["id"]:
            raise ValueError(f"{path}:{line_number}: id must be a non-empty string")
        if case["id"] in seen_ids:
            raise ValueError(f"{path}:{line_number}: duplicate id {case['id']!r}")
        seen_ids.add(case["id"])

        if not isinstance(case["text"], str) or not case["text"].strip():
            raise ValueError(f"{path}:{line_number}: text must be a non-empty string")
        if not isinstance(case["tags"], list) or not all(isinstance(tag, str) for tag in case["tags"]):
            raise ValueError(f"{path}:{line_number}: tags must be a list of strings")
        if "prosody" in case and not isinstance(case["prosody"], dict):
            raise ValueError(f"{path}:{line_number}: prosody must be an object when present")

        cases.append(case)

    if not cases:
        raise ValueError(f"{path}: no benchmark cases found")
    return cases


def summarize_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    categories: dict[str, int] = {}
    prosody_cases = 0
    for case in cases:
        categories[case["category"]] = categories.get(case["category"], 0) + 1
        if "prosody" in case:
            prosody_cases += 1

    return {
        "case_count": len(cases),
        "prosody_case_count": prosody_cases,
        "categories": categories,
        "case_ids": [case["id"] for case in cases],
    }


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def shell_quote(value: Any) -> str:
    return shlex.quote(str(value))


def command_for_case(template: str, case: dict[str, Any], case_json: Path, output_path: Path) -> str:
    prosody = case.get("prosody", {})
    fields = {
        "case_id": shell_quote(case["id"]),
        "text": shell_quote(case["text"]),
        "category": shell_quote(case["category"]),
        "prosody_json": shell_quote(json.dumps(prosody, sort_keys=True)),
        "case_json": shell_quote(case_json),
        "output_path": shell_quote(output_path),
    }
    try:
        return template.format(**fields)
    except KeyError as exc:
        known = ", ".join(sorted(fields))
        raise ValueError(f"unknown command placeholder {exc}; known placeholders: {known}") from exc


def write_case_json(path: Path, case: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(case, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tail_text(value: str, limit: int = 4000) -> str:
    if len(value) <= limit:
        return value
    return value[-limit:]


def parse_engine_json(stdout: str) -> dict[str, Any]:
    """Return the last JSON object emitted on stdout, or an empty dict."""

    for line in reversed(stdout.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return {}


def run_command(command: str, timeout_seconds: float) -> tuple[CompletedProcess[str] | None, float, bool]:
    start = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            shell=True,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        completed = CompletedProcess(command, returncode=124, stdout=stdout, stderr=stderr)
        return completed, elapsed_ms, True

    elapsed_ms = (time.perf_counter() - start) * 1000
    return completed, elapsed_ms, timed_out


def run_cases(
    cases: list[dict[str, Any]],
    engine_cmd: str,
    engine_ref: str,
    environment_id: str,
    runtime_mode: str,
    artifact_dir: Path,
    results_path: Path,
    timeout_seconds: float,
    parse_stdout_json: bool,
) -> dict[str, Any]:
    run_id = f"{utc_now().replace(':', '').replace('-', '')}-{uuid.uuid4().hex[:8]}"
    run_dir = artifact_dir / run_id
    case_dir = run_dir / "cases"
    output_dir = run_dir / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    results_path.parent.mkdir(parents=True, exist_ok=True)

    counts = {"passed": 0, "failed": 0, "timeout": 0}
    with results_path.open("a", encoding="utf-8") as results_file:
        for case in cases:
            case_id = case["id"]
            case_json = case_dir / f"{case_id}.json"
            output_path = output_dir / f"{case_id}.wav"
            write_case_json(case_json, case)
            command = command_for_case(engine_cmd, case, case_json, output_path)

            started_at = utc_now()
            completed, elapsed_ms, timed_out = run_command(command, timeout_seconds)
            engine_report = parse_engine_json(completed.stdout) if parse_stdout_json and completed else {}
            exit_code = completed.returncode if completed else None
            status = "timeout" if timed_out else "passed" if exit_code == 0 else "failed"
            counts[status] += 1

            result = {
                "run_id": run_id,
                "started_at": started_at,
                "case_id": case_id,
                "category": case["category"],
                "input_chars": len(case["text"]),
                "runtime_mode": runtime_mode,
                "environment_id": environment_id,
                "engine_ref": engine_ref,
                "command_template": engine_cmd,
                "command": command,
                "status": status,
                "exit_code": exit_code,
                "timed_out": timed_out,
                "timeout_seconds": timeout_seconds,
                "first_audio_ms": engine_report.get("first_audio_ms"),
                "full_utterance_ms": round(elapsed_ms, 3),
                "artifact_output_path": str(output_path),
                "case_json_path": str(case_json),
                "stdout_tail": tail_text(completed.stdout) if completed else "",
                "stderr_tail": tail_text(completed.stderr) if completed else "",
            }
            if engine_report:
                result["engine_report"] = engine_report
            results_file.write(json.dumps(result, sort_keys=True) + "\n")
            results_file.flush()

    return {
        "mode": "run",
        "run_id": run_id,
        "case_count": len(cases),
        "results_path": str(results_path),
        "artifact_dir": str(run_dir),
        "environment_id": environment_id,
        "engine_ref": engine_ref,
        "counts": counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("benchmarks/prototype_cases.jsonl"),
        help="newline-delimited JSON benchmark case file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate cases and print the planned benchmark summary",
    )
    parser.add_argument(
        "--engine-cmd",
        help=(
            "shell command template to run once per case; supported placeholders: "
            "{case_id}, {text}, {category}, {prosody_json}, {case_json}, {output_path}"
        ),
    )
    parser.add_argument(
        "--engine-ref",
        default="unspecified",
        help="engine/model/runtime identifier recorded in results",
    )
    parser.add_argument(
        "--environment-id",
        default="R1-LOCAL-CPU-2026-10",
        help="documented benchmark environment ID recorded in results",
    )
    parser.add_argument(
        "--runtime-mode",
        default="offline",
        help="runtime mode recorded in results, such as offline or streaming",
    )
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path("artifacts/benchmark-runs"),
        help="ignored local directory for per-run case JSON and generated audio paths",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=Path("artifacts/benchmark-runs/results.jsonl"),
        help="JSONL benchmark result file",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=300.0,
        help="per-case engine command timeout",
    )
    parser.add_argument(
        "--parse-stdout-json",
        action="store_true",
        help="merge timing fields from the last JSON object printed by the engine command",
    )
    args = parser.parse_args()

    try:
        cases = load_cases(args.cases)
    except ValueError as exc:
        print(f"benchmark validation failed: {exc}", file=sys.stderr)
        return 1

    summary = summarize_cases(cases)
    if args.engine_cmd:
        try:
            summary = run_cases(
                cases=cases,
                engine_cmd=args.engine_cmd,
                engine_ref=args.engine_ref,
                environment_id=args.environment_id,
                runtime_mode=args.runtime_mode,
                artifact_dir=args.artifact_dir,
                results_path=args.results,
                timeout_seconds=args.timeout_seconds,
                parse_stdout_json=args.parse_stdout_json,
            )
        except ValueError as exc:
            print(f"benchmark run failed: {exc}", file=sys.stderr)
            return 1
    else:
        summary["mode"] = "dry-run" if args.dry_run else "validate-only"
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
