# R1 Chatterbox Turbo Benchmark

This records `SO-SPIKE-001-T05`: Chatterbox Turbo install, smoke test, and local
CPU benchmark evidence. It is not a final model-selection decision.

## Candidate

- Candidate: Chatterbox Turbo.
- Model: `ResembleAI/chatterbox-turbo`.
- Hugging Face snapshot: `749d1c1a46eb10492095d68fbcf55691ccf137cd`.
- Python package: `chatterbox-tts==0.1.7`.
- Runtime: Python 3.11 virtual environment under ignored local artifacts.
- Torch: `2.6.0+cu124`.
- Device: CPU, 8 Torch threads.
- Environment: `R1-LOCAL-CPU-2026-10`.
- Harness adapter: `scripts/r1_chatterbox_turbo_engine.py`.
- Raw local results: ignored artifact path
  `artifacts/benchmark-runs/chatterbox-turbo-results.jsonl`.
- Generated audio: ignored artifact path
  `artifacts/benchmark-runs/20261002T135540Z-c15410c7/audio/`.

## Install Notes

The package installed successfully in an isolated Python 3.11 environment:

```bash
python3.11 -m venv artifacts/chatterbox-venv
artifacts/chatterbox-venv/bin/python -m pip install chatterbox-tts
```

Setup is heavy for a CPU-only smoke test. The environment consumed about 6.2 GiB
for the virtual environment, and the model cache consumed about 3.8 GiB after
downloading `ResembleAI/chatterbox-turbo`.

The first model-load attempt failed because `resemble-perth` imports
`pkg_resources`, while the freshly upgraded `setuptools==84.0.0` no longer
provided it:

```text
TypeError: 'NoneType' object is not callable
```

The underlying import failure was:

```text
ModuleNotFoundError: No module named 'pkg_resources'
```

Pinning setuptools below the removal boundary fixed the issue:

```bash
artifacts/chatterbox-venv/bin/python -m pip install 'setuptools<81'
```

After that, `ChatterboxTurboTTS.from_pretrained("cpu")` loaded successfully.
The candidate should carry a setup-risk note until upstream removes the
deprecated `pkg_resources` dependency or the project pins the working
dependency range explicitly.

## Smoke Test

The smoke test generated one public-safe benchmark sentence to a local ignored
WAV artifact.

Result:

- status: pass;
- output sample rate: 24 kHz;
- generated audio duration: 2.48 s;
- model-load time: 10.50 s;
- synthesis time: 34.83 s;
- first-audio latency: unavailable; the adapter runs offline generation.

## Harness Run

Command shape:

```bash
artifacts/chatterbox-venv/bin/python scripts/benchmark.py \
  --engine-cmd 'HF_HOME=$PWD/artifacts/hf-cache XDG_CACHE_HOME=$PWD/artifacts/xdg-cache artifacts/chatterbox-venv/bin/python scripts/r1_chatterbox_turbo_engine.py --case {case_json} --out {output_path} --threads 8' \
  --engine-ref 'chatterbox-tts 0.1.7 / ResembleAI/chatterbox-turbo@749d1c1a46eb10492095d68fbcf55691ccf137cd / torch 2.6.0+cu124 / CPU' \
  --environment-id R1-LOCAL-CPU-2026-10 \
  --runtime-mode offline \
  --results artifacts/benchmark-runs/chatterbox-turbo-results.jsonl \
  --timeout-seconds 300 \
  --parse-stdout-json
```

Run summary:

- cases: 6;
- passed: 6;
- failed: 0;
- timed out: 0;
- total cold-process wall time across cases: 169.78 s.

| Case | Category | Input chars | Audio seconds | Model load ms | Synthesis ms | Full command ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `plain-001` | plain | 46 | 2.56 | 7674.52 | 13767.25 | 32074.26 |
| `plain-002` | plain | 69 | 3.76 | 8723.96 | 15008.57 | 31132.68 |
| `question-001` | question | 63 | 3.80 | 7124.90 | 14918.21 | 27427.71 |
| `emphasis-001` | emphasis | 46 | 3.08 | 6355.92 | 13179.15 | 25552.74 |
| `emotion-001` | emotion | 50 | 3.04 | 5854.94 | 16258.14 | 29686.57 |
| `pace-001` | pace | 44 | 2.56 | 7424.48 | 10875.24 | 23903.35 |

Aggregate:

- full command wall time: min 23.90 s, median 28.56 s, max 32.07 s;
- model load: min 5.85 s, median 7.27 s, max 8.72 s;
- synthesis: min 10.88 s, median 14.34 s, max 16.26 s;
- generated audio: min 2.56 s, median 3.06 s, max 3.80 s.

## Fit Judgment

Chatterbox Turbo is viable enough to keep in the R1 comparison. It installed,
loaded, and generated all six benchmark cases on the local CPU profile after a
small dependency pin.

The local CPU result is not an acceptable interactive-latency result. Even warm
synthesis was roughly 10.9-16.3 seconds for 2.6-3.8 seconds of generated audio,
and the current adapter does not expose first-audio latency. This should not be
used to reject Turbo outright because the candidate is intended for a more
accelerated neural TTS runtime than the local CPU profile.

Recommended status for R1:

- keep as a primary candidate;
- require a cloud NVIDIA L4 rerun before any negative latency decision;
- include setup risk for `resemble-perth`/`setuptools<81`;
- treat current prosody-hint support as unproven because the adapter passed raw
  text only and did not map AI Speech Lab prosody JSON into Chatterbox tags.

## Follow-Up

- Add Chatterbox Nano evidence separately if Nano remains the low-resource
  Chatterbox path.
- Reuse this adapter pattern for later candidates, but avoid comparing
  cold-process command time against any candidate with an in-process server or
  streaming API.
