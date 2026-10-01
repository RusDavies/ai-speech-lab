# Benchmark Harness

The benchmark harness should make AI Speech Lab prototypes comparable before the
model architecture is settled.

## Case Format

Benchmark cases are newline-delimited JSON in `benchmarks/prototype_cases.jsonl`.
Each line contains:

- `id`: stable case identifier.
- `text`: text to synthesize.
- `category`: `plain`, `question`, `emphasis`, `emotion`, `pace`, or another
  documented category.
- `prosody`: optional structured prosody hints.
- `expected_focus`: what the case is meant to reveal.
- `tags`: short strings for filtering and reporting.

Prosody metadata is deliberately provisional. It is allowed to change after the
first architecture/prosody-format decision, but changes must be recorded in the
knowledge log.

## Required Metrics

- `first_audio_ms`: time until the first audio chunk is available, when
  streaming or incremental generation supports it.
- `full_utterance_ms`: time until the generated utterance is complete.
- `input_chars`: input character count.
- `runtime_mode`: offline, streaming, batched, or other documented mode.
- `hardware`: CPU/GPU/NPU and relevant model-runtime environment.
- `environment_id`: documented benchmark environment profile, such as
  `R1-LOCAL-CPU-2026-10`.
- `engine_ref`: command, commit, model, or runtime identifier.
- `case_id`: matching benchmark case.

## Review Rubric

Human review should score or annotate:

- intelligibility;
- naturalness;
- expressiveness;
- prosody following;
- pacing;
- audio artifacts;
- speaker similarity when an authorized target voice is used;
- misuse/provenance concerns.

## Engine Invocation

`scripts/benchmark.py` can now run an external engine command once per benchmark
case and append structured JSONL results.

Example:

```bash
python3 scripts/benchmark.py \
  --engine-cmd 'python3 synth.py --case {case_json} --out {output_path}' \
  --engine-ref 'example-engine@commit-or-model' \
  --environment-id R1-LOCAL-CPU-2026-10 \
  --runtime-mode offline \
  --results artifacts/benchmark-runs/example-results.jsonl
```

Supported command placeholders:

- `{case_id}`: benchmark case ID.
- `{text}`: benchmark text.
- `{category}`: benchmark category.
- `{prosody_json}`: compact JSON object for the case prosody, or `{}`.
- `{case_json}`: path to a per-case JSON file written for the engine.
- `{output_path}`: suggested output WAV path under the run artifact directory.

Case-derived placeholder values are shell-quoted before the command runs.
Literal braces in the command template must be doubled because the harness uses
Python string formatting for placeholders.

The harness records:

- `run_id`;
- `case_id`;
- `environment_id`;
- `engine_ref`;
- `runtime_mode`;
- command template and rendered command;
- status, exit code, timeout flag, stdout/stderr tails;
- measured `full_utterance_ms`;
- nullable `first_audio_ms`;
- generated output path and per-case JSON path.

By default, raw run artifacts and JSONL results are written under ignored
`artifacts/` paths. Persist curated benchmark summaries under `benchmarks/` only
after checking artifact provenance and license constraints.

If `--parse-stdout-json` is set, the harness reads the last JSON object printed
by the engine command and stores it as `engine_report`. This lets wrappers report
fields such as `first_audio_ms` when an engine exposes streaming timing.

## Current Harness Scope

`scripts/benchmark.py` currently validates benchmark cases, summarizes dry-run
plans, invokes external engine commands, and records JSONL run metadata. It does
not judge audio quality or compute perceptual metrics.

The first R1 local benchmark profile is documented in
[`R1_BENCHMARK_ENVIRONMENT.md`](R1_BENCHMARK_ENVIRONMENT.md). The first planned
R1 cloud GPU profile is documented in
[`R1_CLOUD_GPU_PROFILE.md`](R1_CLOUD_GPU_PROFILE.md).
