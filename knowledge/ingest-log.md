# Ingest Log

## 2026-10-01

- Recorded initial owner brief into product docs and knowledge entrypoint.
- Added first prototype acceptance criteria, benchmark harness scope, and seed
  benchmark cases.
- Documented open-source/open-weight TTS technology options and current
  recommendation in `docs/TECHNOLOGY_OPTIONS.md`.
- Confirmed exact R1 candidate variants in `docs/R1_CANDIDATE_SET.md`.
- Recorded R1 license/provenance preflight in `docs/R1_LICENSE_PREFLIGHT.md`.
- Defined the first R1 local benchmark environment in
  `docs/R1_BENCHMARK_ENVIRONMENT.md`.
- Added engine-command invocation and JSONL result capture to
  `scripts/benchmark.py`, with usage documented in `docs/BENCHMARK_HARNESS.md`.
- Defined the first R1 cloud NVIDIA GPU benchmark profile in
  `docs/R1_CLOUD_GPU_PROFILE.md`.
- Added public-release readiness docs: Apache-2.0 license, contribution,
  security, conduct, issue guidance, public README, and public roadmap.

## 2026-10-02

- Ran the Chatterbox Turbo install, smoke test, and local CPU benchmark for
  `SO-SPIKE-001-T05`; recorded curated evidence in
  `benchmarks/r1_chatterbox_turbo.md`.
- Ran the F5-TTS v1 Base install, smoke test, and local CPU benchmark for
  `SO-SPIKE-001-T06`; recorded curated evidence in
  `benchmarks/r1_f5tts_v1_base.md`.
- Ran the Kokoro 82M install, smoke test, and local CPU benchmark for
  `SO-SPIKE-001-T07`; recorded curated evidence in
  `benchmarks/r1_kokoro_82m.md`.

## 2026-10-07

- Ran the Orpheus install and local preflight benchmark for
  `SO-SPIKE-001-T08`; recorded gated-access and no-CUDA blocker evidence in
  `benchmarks/r1_orpheus_3b_0_1_ft.md`.

## 2026-10-09

- Reviewed current visible Orpheus gated-access, model-card, GitHub, and
  Llama 3.2 base-model terms for `SO-SPIKE-001-T08A`; recorded the conditional
  benchmark decision in `docs/R1_ORPHEUS_ACCESS_REVIEW.md`.
