# First Prototype Acceptance Criteria

The first AI Speech Lab prototype is accepted when it proves the project can measure
the hard parts honestly: text input, optional prosody input, generated speech,
latency, quality evidence, and safety boundaries.

It does not need to meet final Alexa-class naturalness or sub-200 ms latency.
It must make progress measurable.

## Required Capabilities

- A1: Accept plain text input.
- A2: Accept optional structured prosody metadata for at least some cases.
- A3: Generate an audio file or streamable audio artifact for each benchmark
  case.
- A4: Produce timing measurements that distinguish first-audio latency from full
  utterance completion time when the runtime makes that possible.
- A5: Report the engine path, model/runtime identity, hardware profile, and
  benchmark case set used for each run.
- A6: Document which final-goal capabilities are absent, stubbed, or not yet
  evaluated.

## Quality Evidence

- Q1: Include at least five plain-text cases and at least three prosody-marked
  cases.
- Q2: Include a short human review rubric for intelligibility, naturalness,
  expressiveness, prosody following, artifacts, and overall acceptability.
- Q3: Keep generated samples tied to the exact benchmark case, engine version,
  model/runtime identity, and run metadata.
- Q4: Avoid claiming Alexa-class quality until comparative evidence exists.

## Latency Evidence

- L1: Record first-audio latency when measurable.
- L2: Record full-utterance completion latency.
- L3: Record text length, approximate output duration if known, runtime mode,
  hardware, and whether generation is streaming or offline.
- L4: Treat sub-200 ms as the final interactive target, not the first prototype
  acceptance gate.

## Safety And Provenance

- S1: Use only public-safe text prompts and synthetic or authorized voices.
- S2: Do not include private voice samples, celebrity imitation targets, or
  identity-sensitive material in the benchmark pack.
- S3: Record dataset, model, and voice provenance before sharing generated
  examples outside the development environment.

## First Prototype Definition Of Done

- D1: `scripts/benchmark.py --dry-run` validates the benchmark case set.
- D2: A prototype engine command can be run against the case set.
- D3: The benchmark run writes machine-readable results.
- D4: At least one generated audio artifact exists for each required case.
- D5: A short review note summarizes latency, quality, missing capabilities, and
  next research risks.

