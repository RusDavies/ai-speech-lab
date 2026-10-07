# Knowledge Index

## Current Intent

AI Speech Lab is an open source text-to-speech engine aiming for expressive,
natural, low-latency speech generation with optional prosody control and
authorized voice adaptation.

Primary target:

- text input;
- optional intonation/prosody input;
- synthesized prosody when no prosody is supplied;
- Alexa-class expressive naturalness;
- authorized voice adaptation from a sample;
- ultimate interactive latency below 200 ms.

## Pages

- `sources.md`: external papers, repositories, datasets, benchmarks, and source
  evaluations.
- `decisions.md`: architecture, data, model, runtime, safety, and release
  decisions.
- `ingest-log.md`: what has been reviewed, when, and why it matters.
- `../docs/TECHNOLOGY_OPTIONS.md`: current open-source/open-weight TTS options
  and their fit to AI Speech Lab.
- `../docs/R1_CANDIDATE_SET.md`: exact model/project variants selected for the
  R1 comparison spike.
- `../docs/R1_LICENSE_PREFLIGHT.md`: license/provenance preflight for confirmed
  R1 candidates.
- `../docs/R1_BENCHMARK_ENVIRONMENT.md`: local hardware/runtime profile and
  measurement rules for the R1 comparison spike.
- `../docs/R1_CLOUD_GPU_PROFILE.md`: first planned cloud NVIDIA GPU profile for
  R1 candidate comparisons.
- `../benchmarks/r1_chatterbox_turbo.md`: Chatterbox Turbo install, smoke test,
  and local CPU benchmark evidence.
- `../benchmarks/r1_f5tts_v1_base.md`: F5-TTS v1 Base install, smoke test, and
  local CPU benchmark evidence.
- `../benchmarks/r1_kokoro_82m.md`: Kokoro 82M install, smoke test, and local
  CPU benchmark evidence.
- `../benchmarks/r1_orpheus_3b_0_1_ft.md`: Orpheus install, local preflight
  blocker evidence, and deferred benchmark recommendation.
- `../docs/ROADMAP.md`: public-safe product roadmap.

## Current Open Questions

- Which existing open TTS stacks deserve the first comparison?
- What prosody metadata format should be supported first?
- What public datasets and licenses are acceptable?
- When should the first R1 candidate be rerun on the cloud NVIDIA L4 profile?
- When should the product repository be made public after clean-history release
  preparation?
- When should Orpheus gated access be reviewed and rerun on the cloud NVIDIA L4
  profile?
