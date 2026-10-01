# AI Speech Lab

AI Speech Lab is an early-stage open-source text-to-speech research project. The goal
is expressive, natural speech generation with optional prosody control,
authorized voice adaptation, and eventually interactive low latency.

This repository is not yet a production TTS engine. It currently contains the
project requirements, benchmark cases, benchmark harness, candidate research,
and R1 comparison plan.

## Goals

AI Speech Lab should eventually:

- convert text into speech;
- Accept optional intonation/prosody information.
- Synthesize appropriate prosody when none is provided.
- Approach current Alexa-class naturalness and expressiveness.
- Adapt to an authorized target voice from a voice sample.
- Ultimately support interactive latency below 200 ms.

## Current Status

Current work is focused on R1 candidate comparison:

- exact candidate variants are documented in `docs/R1_CANDIDATE_SET.md`;
- license/provenance preflight is documented in
  `docs/R1_LICENSE_PREFLIGHT.md`;
- local and cloud benchmark environment profiles are documented in
  `docs/R1_BENCHMARK_ENVIRONMENT.md` and `docs/R1_CLOUD_GPU_PROFILE.md`;
- benchmark cases live in `benchmarks/prototype_cases.jsonl`;
- `scripts/benchmark.py` validates cases and can invoke external engine command
  wrappers while recording JSONL timing metadata.

## Quick Check

```bash
./scripts/check.sh
```

This validates docs hygiene, compiles the benchmark harness, validates benchmark
cases, and runs a dummy engine invocation across the seed cases.

## Roadmap

See `docs/ROADMAP.md`.

## Safety Boundary

Voice adaptation must be designed around consent, provenance, and misuse
resistance. A sample being technically available is not the same thing as a
voice being authorized for cloning or synthesis.

Do not submit private voice samples, celebrity imitation targets,
identity-sensitive voice material, or generated audio without documented rights
and provenance.

## License

AI Speech Lab is licensed under Apache-2.0. See `LICENSE`.
