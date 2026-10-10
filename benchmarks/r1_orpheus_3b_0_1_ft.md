# R1 Orpheus 3B 0.1 Finetuned Benchmark

This records `SO-SPIKE-001-T08`: Orpheus install, smoke test, and local CPU
benchmark evidence. It is not a final model-selection decision.

## Verdict: BLOCKED LOCALLY

Question: Can Orpheus 3B 0.1 Finetuned be installed and run through the
AI Speech Lab R1 benchmark cases on the documented local CPU profile?

Evidence: The package installed in an isolated Python 3.11 environment, but the
selected Orpheus model, the package's default finetuned model alias, and the
pretrained tokenizer/model repository all required gated Hugging Face access.
The local R1 environment also has no CUDA device/driver, while the current
`orpheus-speech` package imports a SNAC decoder that hard-codes CUDA and uses
`vllm` for model inference.

Recommendation: keep Orpheus as a promising but currently blocked expressive
streaming/voice-cloning candidate. Do not score it against the completed local
CPU candidates until gated access has been approved, the access review in
`docs/R1_ORPHEUS_ACCESS_REVIEW.md` has been satisfied, and it is rerun on the
documented NVIDIA L4 profile or equivalent CUDA host.

## Candidate

- Candidate: Orpheus 3B 0.1 Finetuned.
- Selected model: `canopylabs/orpheus-3b-0.1-ft`.
- Package default finetuned model alias observed in examples/package:
  `canopylabs/orpheus-tts-0.1-finetune-prod`.
- Tokenizer/pretrained model repository: `canopylabs/orpheus-3b-0.1-pretrained`.
- SNAC decoder model: `hubertsiuzdak/snac_24khz`.
- Model/repository license metadata: `Apache-2.0`.
- Model gating: gated/conditional access; unauthenticated local access returned
  `GatedRepoError` for Orpheus model/config downloads.
- Access review: `docs/R1_ORPHEUS_ACCESS_REVIEW.md`.
- Python package: `orpheus-speech==0.1.0`.
- Runtime stack installed: `vllm==0.31.0`, `torch==2.13.0`, `snac==1.2.1`.
- Runtime: Python 3.11 virtual environment under ignored local artifacts.
- Device: no CUDA device available in `R1-LOCAL-CPU-2026-10`.
- Voice requested by adapter: `tara`.
- Output sample rate expected by upstream example: 24 kHz.
- Environment: `R1-LOCAL-CPU-2026-10`.
- Harness adapter: `scripts/r1_orpheus_engine.py`.
- Raw local results: ignored artifact path
  `artifacts/benchmark-runs/orpheus-3b-0.1-ft-results.jsonl`.
- Generated audio: none; smoke and harness runs stopped at preflight blockers.

## Install Notes

The package installed successfully in an isolated Python 3.11 environment:

```bash
virtualenv -p python3.11 artifacts/orpheus-venv
artifacts/orpheus-venv/bin/python -m pip install --upgrade pip
artifacts/orpheus-venv/bin/python -m pip install orpheus-speech
```

Setup notes:

- The virtual environment consumed about 8.3 GiB.
- Installing `orpheus-speech==0.1.0` pulled in `vllm==0.31.0`, Torch 2.13,
  CUDA userspace wheels, SNAC, Transformers, and related inference packages.
- The Orpheus Hugging Face cache remained small because gated Orpheus model
  downloads were denied before weight downloads began.
- The public SNAC config for `hubertsiuzdak/snac_24khz` was accessible.
- Importing `orpheus_tts` directly on this host failed before model generation
  with a CUDA driver error because the package decoder initializes SNAC on
  `cuda` at import time.

## Smoke Test

The smoke test used the harness adapter against a public-safe existing benchmark
case. It did not generate audio.

Result:

- status: blocked;
- `canopylabs/orpheus-3b-0.1-ft`: `GatedRepoError`;
- `canopylabs/orpheus-tts-0.1-finetune-prod`: `GatedRepoError`;
- `canopylabs/orpheus-3b-0.1-pretrained`: `GatedRepoError`;
- `hubertsiuzdak/snac_24khz`: config accessible;
- CUDA: unavailable, so local package import/runtime is not viable.

## Harness Run

Command shape:

```bash
python3 scripts/benchmark.py \
  --engine-cmd 'HF_HOME=$PWD/artifacts/orpheus-hf-cache artifacts/orpheus-venv/bin/python scripts/r1_orpheus_engine.py --case {case_json} --out {output_path}' \
  --engine-ref 'orpheus-speech==0.1.0; model=canopylabs/orpheus-3b-0.1-ft; package_model=canopylabs/orpheus-tts-0.1-finetune-prod; license=Apache-2.0; device=local-cpu-no-cuda; access=gated' \
  --environment-id R1-LOCAL-CPU-2026-10 \
  --runtime-mode local-cpu-blocker-preflight \
  --artifact-dir artifacts/benchmark-runs/orpheus-3b-0.1-ft \
  --results artifacts/benchmark-runs/orpheus-3b-0.1-ft-results.jsonl \
  --timeout-seconds 120 \
  --parse-stdout-json
```

Run summary:

- cases: 6;
- passed: 0;
- failed: 6;
- timed out: 0;
- total preflight wall time across cases: about 18.69 s.

| Case | Category | Input chars | Status | Full command ms | Blocker |
| --- | --- | ---: | --- | ---: | --- |
| `plain-001` | plain | 46 | failed | 2633.85 | gated Orpheus repos; no CUDA |
| `plain-002` | plain | 65 | failed | 2340.07 | gated Orpheus repos; no CUDA |
| `question-001` | question | 63 | failed | 2489.30 | gated Orpheus repos; no CUDA |
| `emphasis-001` | emphasis | 46 | failed | 3460.23 | gated Orpheus repos; no CUDA |
| `emotion-001` | emotion | 50 | failed | 3897.38 | gated Orpheus repos; no CUDA |
| `pace-001` | pace | 44 | failed | 3871.07 | gated Orpheus repos; no CUDA |

Aggregate:

- full preflight command wall time: min 2.34 s, median 3.05 s, max 3.90 s;
- audio generated: none;
- first-audio latency: unavailable;
- synthesis latency: unavailable.

## Fit Judgment

Orpheus remains a strategically relevant R1 candidate because its model card and
repository describe guided emotion/intonation tags, zero-shot voice cloning, and
streaming latency goals that match AI Speech Lab's target use case. The local
CPU profile, however, cannot produce meaningful runtime or quality evidence.

The current blocker is not a quality failure. It is a compound access/runtime
blocker: gated model access plus a CUDA/vLLM-oriented inference path. It should
therefore be deferred to the cloud NVIDIA profile after gated terms are reviewed
and accepted, rather than rejected from local CPU evidence.

## Follow-Up

- Complete the gated-access approval record described in
  `docs/R1_ORPHEUS_ACCESS_REVIEW.md` before any further Orpheus run.
- Rerun Orpheus on the documented `R1-CLOUD-NVIDIA-L4-2026-10` profile, or an
  equivalent CUDA host, before scoring latency or quality.
- Recheck the upstream package before the GPU rerun; the current package import
  path assumes CUDA for SNAC decoding.
