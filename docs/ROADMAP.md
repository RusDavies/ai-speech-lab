# Roadmap

AI Speech Lab is an early-stage open-source TTS research project. The roadmap is
evidence-first: compare existing systems, preserve voice consent/provenance
boundaries, and only then choose the first implementation path.

## R1: Candidate Comparison

Goal: compare the strongest existing open-source or open-weight TTS candidates
before selecting a base model, integration strategy, or custom implementation
path.

Primary candidates:

- Chatterbox Turbo/Nano;
- F5-TTS;
- Kokoro;
- Orpheus;
- optional OpenVoice component spike.

Expected outputs:

- install/setup notes;
- license and provenance notes;
- benchmark runs or blocker evidence;
- fit judgment for each candidate;
- recommendation to build on, reject, defer, or use as a baseline/component.

## Prototype Foundations

Goal: make the first prototype measurable before promising final quality.

Expected outputs:

- first supported interface decision;
- prosody metadata format decision;
- candidate-wrapper command contracts for the benchmark harness;
- benchmark summaries that distinguish first-audio latency and full-utterance
  latency;
- a first acceptable prototype latency target before the final sub-200 ms goal.

## Safety And Provenance

Goal: make voice adaptation possible without treating any available sample as
authorized for cloning.

Expected outputs:

- consent and provenance rules for voice samples;
- generated-audio artifact policy;
- disclosure and misuse boundaries;
- model, dataset, and generated-output license tracking.

## Architecture

Goal: split the product into understandable components once the R1 evidence
selects an implementation path.

Expected outputs:

- text/prosody input format;
- prosody synthesis strategy when no explicit prosody is supplied;
- voice-adaptation strategy;
- runtime architecture for local CLI/API use;
- latency measurement and optimization plan.

## Public Release Readiness

Goal: publish the product repository without private management history or
channel provenance.

Expected outputs:

- clean public-facing history;
- public README and project status;
- license, contribution, conduct, and security docs;
- public-safe roadmap;
- final public-readiness scan before repository visibility changes.
