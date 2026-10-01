# Contributing

AI Speech Lab is early-stage research software. Contributions are welcome, but the
project is not yet a stable TTS engine or API.

## Useful Contributions

- Reproducible benchmark results for documented candidate engines.
- Public-safe test cases for prosody, latency, and quality evaluation.
- Documentation improvements with primary sources.
- Candidate wrappers that plug existing TTS systems into `scripts/benchmark.py`.
- Safety, consent, provenance, and misuse-boundary improvements.

## Boundaries

- Do not submit private voice samples.
- Do not submit generated audio from voices you are not authorized to use.
- Do not submit celebrity, public-figure, customer, or identity-sensitive voice
  cloning examples.
- Do not submit model weights, datasets, or generated artifacts unless their
  license and provenance are documented.
- Do not add dependencies whose licenses conflict with public open-source use
  without calling that out clearly.

## Issues

Good issues include:

- the exact engine/model/runtime being discussed;
- hardware and environment details;
- reproduction commands;
- benchmark case IDs;
- license or provenance evidence when relevant;
- expected behavior and observed behavior.

For vulnerability reports, use the process in `SECURITY.md` instead of opening
a public issue.

## Pull Requests

Before opening a pull request:

- run `./scripts/check.sh`;
- keep generated audio and model artifacts out of git;
- keep private operational notes out of product docs;
- update relevant docs or knowledge files when changing project decisions,
  benchmark assumptions, or candidate evidence.

By contributing, you agree that your contribution is submitted under the
Apache-2.0 license used by this repository.
