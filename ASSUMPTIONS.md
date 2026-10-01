# Assumptions

## Current Assumptions

- The project should be open source, with publication gated on licensing,
  safety, documentation, and release readiness.
- "Current Alexa" is a quality target, not a claim that proprietary Alexa
  internals, voices, datasets, or trademarks are available for use.
- Optional intonation information will likely need a structured prosody format,
  but the representation is not chosen yet.
- When explicit intonation is absent, the engine must infer prosody from text and
  context.
- Voice adaptation requires authorized samples. Consent, provenance, and misuse
  controls are product requirements.
- Sub-200 ms latency is the ultimate target for interactive use, not necessarily
  the first prototype target.
- The first useful product result is a measurable prototype and benchmark path,
  not a polished production voice.

## Unknowns

- First target surface: CLI, library, local API service, plugin, or embedded
  runtime.
- Initial hardware target for latency measurements.
- Dataset and model licensing strategy.
- Whether the first milestone should adapt an existing open stack or implement a
  minimal research engine from selected papers.
