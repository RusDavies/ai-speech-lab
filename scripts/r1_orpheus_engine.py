#!/usr/bin/env python3
"""Run one benchmark case through Orpheus TTS when the runtime is available.

The Orpheus PyPI package is CUDA/vLLM-oriented and the selected model is gated
on Hugging Face. This adapter performs explicit preflight checks first so the
R1 harness records a clear blocker instead of an upstream import failure.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import wave
from importlib import metadata
from pathlib import Path


SAMPLE_RATE_HZ = 24000
DEFAULT_MODEL_ID = "canopylabs/orpheus-3b-0.1-ft"
DEFAULT_PACKAGE_MODEL_ID = "canopylabs/orpheus-tts-0.1-finetune-prod"
DEFAULT_TOKENIZER_ID = "canopylabs/orpheus-3b-0.1-pretrained"
DEFAULT_SNAC_ID = "hubertsiuzdak/snac_24khz"


def load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def model_access_status(repo_id: str, filename: str = "config.json") -> dict[str, object]:
    from huggingface_hub import hf_hub_download

    try:
        path = hf_hub_download(repo_id=repo_id, filename=filename)
    except Exception as exc:  # noqa: BLE001 - record upstream HF exception class.
        return {
            "repo_id": repo_id,
            "filename": filename,
            "accessible": False,
            "error_type": type(exc).__name__,
            "error": str(exc).splitlines()[0],
        }
    return {
        "repo_id": repo_id,
        "filename": filename,
        "accessible": True,
        "path": path,
    }


def fail_with_report(report: dict[str, object]) -> int:
    print(json.dumps(report, sort_keys=True))
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument("--package-model-id", default=DEFAULT_PACKAGE_MODEL_ID)
    parser.add_argument("--tokenizer-id", default=DEFAULT_TOKENIZER_ID)
    parser.add_argument("--snac-id", default=DEFAULT_SNAC_ID)
    parser.add_argument("--voice", default="tara")
    parser.add_argument("--max-model-len", type=int, default=2048)
    parser.add_argument("--hf-cache-dir", default="artifacts/orpheus-hf-cache")
    args = parser.parse_args()

    os.environ.setdefault("HF_HOME", args.hf_cache_dir)
    case = load_case(args.case)

    import torch

    package_report = {
        "candidate": "orpheus-3b-0.1-ft",
        "model_id": args.model_id,
        "package_model_id": args.package_model_id,
        "tokenizer_id": args.tokenizer_id,
        "snac_id": args.snac_id,
        "package": f"orpheus-speech=={package_version('orpheus-speech')}",
        "vllm": package_version("vllm"),
        "torch": package_version("torch"),
        "snac": package_version("snac"),
        "device": "cuda" if torch.cuda.is_available() else "none",
        "cuda_available": torch.cuda.is_available(),
        "sample_rate_hz": SAMPLE_RATE_HZ,
        "voice": args.voice,
    }

    model_access = model_access_status(args.model_id)
    package_model_access = model_access_status(args.package_model_id)
    tokenizer_access = model_access_status(args.tokenizer_id)
    snac_access = model_access_status(args.snac_id)
    access_report = {
        "model_access": model_access,
        "package_model_access": package_model_access,
        "tokenizer_access": tokenizer_access,
        "snac_access": snac_access,
    }

    blockers = []
    if not model_access["accessible"]:
        blockers.append("selected Orpheus model repo is gated or inaccessible")
    if not package_model_access["accessible"]:
        blockers.append("Orpheus package default finetuned repo is gated or inaccessible")
    if not tokenizer_access["accessible"]:
        blockers.append("Orpheus tokenizer/pretrained repo is gated or inaccessible")
    if not torch.cuda.is_available():
        blockers.append("local R1 environment has no CUDA device/driver for vLLM or package SNAC decode")

    if blockers:
        return fail_with_report(
            {
                **package_report,
                **access_report,
                "status": "blocked",
                "blockers": blockers,
            }
        )

    # Import only after preflight: package import initializes the SNAC decoder.
    from orpheus_tts import OrpheusModel

    load_start = time.perf_counter()
    model = OrpheusModel(model_name=args.package_model_id, max_model_len=args.max_model_len)
    load_ms = (time.perf_counter() - load_start) * 1000

    args.out.parent.mkdir(parents=True, exist_ok=True)
    synth_start = time.perf_counter()
    first_audio_ms = None
    chunk_count = 0
    total_frames = 0
    with wave.open(str(args.out), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE_HZ)
        for audio_chunk in model.generate_speech(prompt=case["text"], voice=args.voice):
            if first_audio_ms is None:
                first_audio_ms = (time.perf_counter() - synth_start) * 1000
            chunk_count += 1
            output.writeframes(audio_chunk)
            total_frames += len(audio_chunk) // (output.getsampwidth() * output.getnchannels())
    synth_ms = (time.perf_counter() - synth_start) * 1000

    if chunk_count == 0:
        raise RuntimeError("Orpheus produced no audio chunks")

    print(
        json.dumps(
            {
                **package_report,
                **access_report,
                "audio_seconds": round(total_frames / SAMPLE_RATE_HZ, 3),
                "model_load_ms": round(load_ms, 3),
                "synthesis_ms": round(synth_ms, 3),
                "first_audio_ms": round(first_audio_ms, 3) if first_audio_ms is not None else None,
                "chunk_count": chunk_count,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
