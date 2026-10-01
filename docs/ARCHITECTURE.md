# Architecture

## Initial Architecture Sketch

The final architecture is not selected yet. The first architecture work should
compare existing open TTS stacks against a minimal research implementation path.

Expected subsystems:

- Text normalization and linguistic preprocessing.
- Optional prosody/intonation input parser.
- Prosody synthesis or prediction when no explicit prosody is supplied.
- Acoustic/model layer for speech generation.
- Speaker adaptation layer for authorized target voices.
- Vocoder or waveform generation layer.
- Streaming/runtime layer for low-latency output.
- Benchmark and evaluation harness.
- Provenance, consent, and safety metadata handling.

## Latency Model

Sub-200 ms interactive latency likely requires streaming or incremental
generation, careful model/runtime selection, and hardware-specific optimization.
The project should measure first-audio latency separately from total utterance
completion time.

## Architecture Decisions Pending

- Use an existing open stack as the base, build from selected papers, or run both
  as a bounded spike.
- Choose a first prosody metadata representation.
- Choose an initial model family and vocoder/runtime path.
- Define the consent/provenance mechanism for voice samples.

## Benchmark Harness Position

The first benchmark harness is intentionally engine-agnostic. It defines
public-safe benchmark cases and validates case metadata before a model/runtime is
chosen. Engine invocation and result capture become architecture work once the
first prototype command surface exists.
