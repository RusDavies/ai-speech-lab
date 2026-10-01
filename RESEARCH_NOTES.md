# Research Notes

## Initial Research Direction

AI Speech Lab is a research/software project for an open source TTS engine with:

- text input;
- optional intonation or prosody input;
- synthesized prosody when intonation is absent;
- Alexa-class expressive naturalness as the quality target;
- authorized voice adaptation from a sample;
- ultimate latency target below 200 ms.

## Early Research Questions

- Which existing open neural TTS stacks provide the best starting point for
  expressive prosody and low latency?
- What representation should optional intonation/prosody metadata use?
- Can speaker adaptation be separated cleanly from content/prosody modeling?
- What quality benchmark can stand in for "current Alexa" without depending on
  proprietary implementation details?
- What runtime architecture could realistically reach sub-200 ms interactive
  latency?
- What consent, watermarking, disclosure, or provenance controls should be part
  of the open source design from the start?
