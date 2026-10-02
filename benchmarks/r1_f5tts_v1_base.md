# R1 F5-TTS v1 Base Benchmark

This records `SO-SPIKE-001-T06`: F5-TTS v1 Base install, smoke test, and local
CPU benchmark evidence. It is not a final model-selection decision.

## Verdict: PARTIAL

Question: Can F5-TTS v1 Base be installed and run through the AI Speech Lab R1
benchmark cases on the documented local CPU profile?

Evidence: The package installed, the selected model weights downloaded, and all
six benchmark cases generated WAV artifacts without timeout. Local CPU latency
is far outside the interactive target, and the selected weights remain
`CC-BY-NC-4.0`, so this is research-only benchmark evidence unless a different
license path is selected.

Recommendation: keep F5-TTS in the R1 comparison as a strong research/reference
candidate and rerun on the documented NVIDIA L4 profile before making a latency
decision. Do not treat the selected weights as a product base for commercial or
open-core downstream use.

## Candidate

- Candidate: F5-TTS v1 Base.
- Model: `SWivid/F5-TTS`, checkpoint family `F5TTS_v1_Base`.
- Hugging Face snapshot: `84e5a410d9cead4de2f847e7c9369a6440bdfaca`.
- Checkpoint: `F5TTS_v1_Base/model_1250000.safetensors`.
- Weight license: `CC-BY-NC-4.0`.
- Python package: `f5-tts==1.1.22`.
- Runtime: Python 3.10 virtual environment under ignored local artifacts.
- Torch: `2.14.1+cu130`.
- Device: CPU, 8 Torch threads for harness runs.
- Environment: `R1-LOCAL-CPU-2026-10`.
- Harness adapter: `scripts/r1_f5tts_engine.py`.
- Reference audio: bundled F5-TTS public example `basic_ref_en.wav`.
- Raw local results: ignored artifact path
  `artifacts/benchmark-runs/f5tts-v1-base-results.jsonl`.
- Generated audio: ignored artifact path
  `artifacts/benchmark-runs/20261002T141450Z-29bd33d8/audio/`.

## Install Notes

The package installed successfully in an isolated Python 3.10 environment:

```bash
python3.10 -m venv artifacts/f5tts-venv
artifacts/f5tts-venv/bin/python -m pip install 'pip<26' 'setuptools<81' wheel
artifacts/f5tts-venv/bin/python -m pip install f5-tts
```

Setup is heavy for a CPU-only spike. The virtual environment consumed about
6.6 GiB, and the model/vocoder cache consumed about 1.4 GiB after downloading
the selected checkpoint and Vocos dependencies.

Runtime notes:

- Inference emitted a Python 3.10 support warning from `google.api_core`; this
  is not an immediate blocker, but a future local environment should move to
  Python 3.11 if F5-TTS remains in active use.
- Hugging Face downloads used unauthenticated access.
- The selected model weights are non-commercial; benchmark artifacts from this
  run should be treated as research/reference evidence.

## Smoke Test

The smoke test generated one public-safe benchmark sentence using the bundled
F5-TTS English reference clip and transcript.

Result:

- status: pass;
- output sample rate: 24 kHz;
- generated audio duration: 4.37 s;
- model-load time: 22.23 s during the first smoke run;
- synthesis time: 253.56 s during the first smoke run;
- first-audio latency: unavailable; the adapter runs offline generation.

## Harness Run

Command shape:

```bash
python3 scripts/benchmark.py \
  --engine-cmd 'HF_HOME=$PWD/artifacts/f5tts-hf-cache XDG_CACHE_HOME=$PWD/artifacts/f5tts-xdg-cache artifacts/f5tts-venv/bin/python scripts/r1_f5tts_engine.py --case {case_json} --out {output_path} --threads 8 --hf-cache-dir artifacts/f5tts-hf-cache' \
  --engine-ref 'f5-tts 1.1.22 / SWivid/F5-TTS F5TTS_v1_Base@84e5a410d9cead4de2f847e7c9369a6440bdfaca / torch 2.14.1+cu130 / CPU / CC-BY-NC-4.0 weights' \
  --environment-id R1-LOCAL-CPU-2026-10 \
  --runtime-mode offline \
  --results artifacts/benchmark-runs/f5tts-v1-base-results.jsonl \
  --timeout-seconds 600 \
  --parse-stdout-json
```

Run summary:

- cases: 6;
- passed: 6;
- failed: 0;
- timed out: 0;
- total cold-process wall time across cases: 1433.18 s.

| Case | Category | Input chars | Audio seconds | Model load ms | Synthesis ms | Full command ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `plain-001` | plain | 46 | 4.37 | 4973.97 | 266704.21 | 290452.66 |
| `plain-002` | plain | 65 | 6.19 | 2874.18 | 262873.13 | 276372.42 |
| `question-001` | question | 63 | 6.00 | 1835.93 | 240778.34 | 250387.64 |
| `emphasis-001` | emphasis | 46 | 4.37 | 2166.67 | 200334.67 | 209162.05 |
| `emotion-001` | emotion | 50 | 4.76 | 1996.54 | 198840.05 | 207414.60 |
| `pace-001` | pace | 44 | 4.18 | 1848.43 | 190687.78 | 199394.27 |

Aggregate:

- full command wall time: min 199.39 s, median 229.77 s, max 290.45 s;
- model load: min 1.84 s, median 2.08 s, max 4.97 s;
- synthesis: min 190.69 s, median 220.56 s, max 266.70 s;
- generated audio: min 4.18 s, median 4.57 s, max 6.19 s.

## Fit Judgment

F5-TTS v1 Base is technically runnable in the local CPU R1 environment, but this
profile is not useful for interactive latency judgment. All cases completed, yet
synthesis took roughly 191-267 seconds for about 4-6 seconds of generated audio.
This is evidence that the CPU baseline is feasible for integration smoke only,
not for performance conclusions.

The model remains interesting because it is a strong zero-shot/reference
candidate with documented optimized deployment paths. It should be rerun on the
documented `R1-CLOUD-NVIDIA-L4-2026-10` profile before latency scoring.

License status is the larger product constraint: the selected weights are
`CC-BY-NC-4.0`, so this exact checkpoint should be treated as non-commercial
research/reference evidence unless a differently licensed checkpoint or model
path is selected.

## Follow-Up

- Add an explicit F5 cloud L4 rerun task before final scoring.
- Keep F5 generated artifacts out of git and mark them research-only while the
  selected weight license is non-commercial.
- If F5 remains a serious contender, investigate its optimized deployment path
  separately from the simple offline API wrapper used here.
