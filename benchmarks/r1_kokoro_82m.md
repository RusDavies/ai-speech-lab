# R1 Kokoro 82M Benchmark

This records `SO-SPIKE-001-T07`: Kokoro 82M install, smoke test, and local CPU
benchmark evidence. It is not a final model-selection decision.

## Verdict: VALIDATED

Question: Can Kokoro 82M be installed and run through the AI Speech Lab R1
benchmark cases on the documented local CPU profile?

Evidence: The package installed, the model and voice weights downloaded, and all
six benchmark cases generated WAV artifacts without timeout. Local CPU latency
is materially better than the previously measured voice-cloning candidates, and
the model/repository license is Apache-2.0.

Recommendation: keep Kokoro 82M as the R1 fixed-voice low-latency baseline and
possible runtime/component candidate. Do not treat it as a full voice-cloning
solution by itself, because this benchmark used a bundled fixed voice rather
than authorized speaker adaptation from a sample.

## Candidate

- Candidate: Kokoro 82M.
- Model: `hexgrad/Kokoro-82M`.
- Hugging Face snapshot: `f3ff3571791e39611d31c381e3a41a3af07b4987`.
- Model/repository license: `Apache-2.0`.
- Python package: `kokoro==0.9.4`.
- Runtime: Python 3.11 virtual environment under ignored local artifacts.
- Torch: `2.14.1+cu130`.
- Device: CPU, 8 Torch threads for harness runs.
- Voice: `af_heart`.
- Language: American English, `a`.
- Output sample rate: 24 kHz.
- Environment: `R1-LOCAL-CPU-2026-10`.
- Harness adapter: `scripts/r1_kokoro_engine.py`.
- Raw local results: ignored artifact path
  `artifacts/benchmark-runs/kokoro-82m-results.jsonl`.
- Generated audio: ignored artifact path
  `artifacts/benchmark-runs/kokoro-82m/20261003T030644Z-e57c1f03/audio/`.

## Install Notes

The package installed successfully in an isolated Python 3.11 environment:

```bash
python3.11 -m venv artifacts/kokoro-venv
artifacts/kokoro-venv/bin/python -m pip install --upgrade pip
artifacts/kokoro-venv/bin/python -m pip install kokoro soundfile
```

Setup notes:

- The virtual environment consumed about 5.9 GiB. This is mostly the PyTorch
  stack, including CUDA packages from the selected wheel even though this run
  used CPU.
- The Hugging Face cache for `hexgrad/Kokoro-82M` consumed about 313 MiB.
- The XDG cache consumed about 13 MiB after the package installed spaCy's
  `en_core_web_sm==3.8.0` model on first use.
- Hugging Face downloads used unauthenticated access.
- First use emitted Torch deprecation/runtime warnings from upstream modules;
  none blocked generation.

## Smoke Test

The smoke test generated one public-safe sentence through the package CLI, then
the harness adapter generated one wrapper smoke sentence.

Wrapper smoke result:

- status: pass;
- output sample rate: 24 kHz;
- generated audio duration: 2.85 s;
- model-load time: 1.52 s;
- first generated chunk: 1.49 s;
- synthesis time: 1.49 s;
- chunks: 1.

## Harness Run

Command shape:

```bash
python3 scripts/benchmark.py \
  --engine-cmd 'HF_HOME=$PWD/artifacts/kokoro-hf-cache XDG_CACHE_HOME=$PWD/artifacts/kokoro-xdg-cache artifacts/kokoro-venv/bin/python scripts/r1_kokoro_engine.py --case {case_json} --out {output_path} --device cpu --threads 8' \
  --engine-ref 'kokoro==0.9.4; model=hexgrad/Kokoro-82M; voice=af_heart; license=Apache-2.0; device=cpu; torch_threads=8' \
  --environment-id R1-LOCAL-CPU-2026-10 \
  --runtime-mode local-cpu \
  --artifact-dir artifacts/benchmark-runs/kokoro-82m \
  --results artifacts/benchmark-runs/kokoro-82m-results.jsonl \
  --timeout-seconds 120 \
  --parse-stdout-json
```

Run summary:

- cases: 6;
- passed: 6;
- failed: 0;
- timed out: 0;
- total cold-process wall time across cases: 45.76 s.

| Case | Category | Input chars | Audio seconds | Model load ms | First chunk ms | Synthesis ms | Full command ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `plain-001` | plain | 46 | 2.85 | 1396.48 | 1379.14 | 1379.17 | 6390.14 |
| `plain-002` | plain | 65 | 4.75 | 1422.86 | 2442.98 | 2443.02 | 7855.68 |
| `question-001` | question | 63 | 4.38 | 1541.49 | 2216.28 | 2216.32 | 7489.50 |
| `emphasis-001` | emphasis | 46 | 3.35 | 1456.66 | 1648.75 | 1648.80 | 7052.62 |
| `emotion-001` | emotion | 50 | 3.38 | 1875.33 | 1797.24 | 1797.29 | 8510.67 |
| `pace-001` | pace | 44 | 3.33 | 1739.40 | 2129.86 | 2129.90 | 7956.85 |

Aggregate:

- full command wall time: min 6.39 s, median 7.67 s, max 8.51 s;
- model load: min 1.40 s, median 1.47 s, max 1.88 s;
- first generated chunk: min 1.38 s, median 1.96 s, max 2.44 s;
- synthesis: min 1.38 s, median 1.96 s, max 2.44 s;
- generated audio: min 2.85 s, median 3.36 s, max 4.75 s.

## Fit Judgment

Kokoro 82M is a strong R1 fixed-voice baseline. It installed cleanly, generated
all benchmark cases, and produced CPU synthesis times near or faster than
real-time for these short cases. Its Apache-2.0 license also makes it cleaner
for open-core/product experimentation than the non-commercial F5-TTS checkpoint.

This benchmark does not validate AI Speech Lab's authorized voice-adaptation
goal. It uses Kokoro's `af_heart` fixed voice, so the right product role is
baseline, component, or fallback voice runtime unless paired with a separate
voice adaptation path.

The adapter records first generated chunk timing from `KPipeline` iteration.
That is useful evidence for chunked generation, but it is not equivalent to an
end-to-end server streaming first-audio measurement.

## Follow-Up

- Keep Kokoro 82M in the R1 scorecard as the fixed-voice latency and license
  baseline.
- Compare future candidates against Kokoro's CPU result, but avoid scoring
  voice adaptation candidates as worse merely because they solve a harder
  problem.
- If Kokoro remains part of the runtime plan, add a separate server/warm-model
  benchmark to measure true first-audio latency outside cold subprocess startup.
