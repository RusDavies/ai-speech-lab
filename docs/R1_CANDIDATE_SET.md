# R1 Candidate Set

This document confirms the exact model/project variants for
`SO-SPIKE-001-T01`. It does not approve any candidate as the product base. It
defines what the R1 comparison spike should test first.

## Primary Candidates

### R1-C1: Chatterbox Turbo

- Project: Chatterbox.
- Variant: `ResembleAI/chatterbox-turbo`.
- Package path: `chatterbox-tts`, class `ChatterboxTurboTTS`.
- Reason to test: low-latency English voice-agent variant, 350M parameters,
  native paralinguistic tags, reference-clip voice generation.
- Benchmark role: primary expressive voice-cloning candidate.
- Source: <https://huggingface.co/ResembleAI/chatterbox-turbo>

### R1-C2: Chatterbox Nano

- Project: Chatterbox.
- Variant: `ResembleAI/chatterbox-nano`.
- Package path: `chatterbox-tts`, class `ChatterboxTurboTTS` with `nano=True`.
- Reason to test: 110M CPU/on-device variant, claimed to run 3x faster than
  realtime on 8 CPU cores.
- Benchmark role: low-resource Chatterbox comparison against Turbo.
- Source: <https://huggingface.co/ResembleAI/chatterbox-nano>

### R1-C3: F5-TTS v1 Base

- Project: F5-TTS.
- Variant: `SWivid/F5-TTS`, checkpoint family `F5TTS_v1_Base`.
- Checkpoint file: `model_1250000.safetensors`.
- Reason to test: strong zero-shot TTS candidate with documented optimized
  deployment paths.
- Benchmark role: primary voice-adaptation and optimized-runtime candidate.
- Source: <https://huggingface.co/SWivid/F5-TTS>

### R1-C4: Kokoro 82M

- Project: Kokoro.
- Variant: `hexgrad/Kokoro-82M`, v1.0 model family.
- Reason to test: small Apache-licensed fixed-voice model with strong speed and
  deployment characteristics.
- Benchmark role: low-latency fixed-voice baseline.
- Source: <https://huggingface.co/hexgrad/Kokoro-82M>

### R1-C5: Orpheus 3B 0.1 Finetuned

- Project: Orpheus TTS.
- Variant: `canopylabs/orpheus-3b-0.1-ft`.
- Reason to test: Llama-based expressive TTS with guided emotion/intonation tags
  and zero-shot voice cloning claims.
- Benchmark role: expressive streaming/voice-cloning candidate.
- Source: <https://huggingface.co/canopylabs/orpheus-3b-0.1-ft>

## Optional Component Candidate

### R1-O1: OpenVoice V2

- Project: OpenVoice.
- Variant: OpenVoice V2 from `myshell-ai/OpenVoice`.
- Reason to test: MIT-licensed tone-color cloning and style-control component.
- Benchmark role: optional voice-adaptation component if it can pair cleanly with
  a base TTS engine.
- Source: <https://github.com/myshell-ai/OpenVoice>

## Reference-Only Candidates

These are not primary R1 installs unless a primary candidate blocks early or the
spike has spare time.

- `rhasspy/piper`: CPU/offline fixed-voice baseline; original repo archived.
- `coqui/XTTS-v2`: useful cloning reference, but model license needs special
  scrutiny.
- `yl4579/StyleTTS2`: research baseline for style diffusion and naturalness.
- `nari-labs/dia`: dialogue/nonverbal expressiveness reference.
- `fishaudio/fish-speech`: frontier-style expressive reference with research
  license and heavier runtime implications.

## Explicit Deferrals

- Spark-TTS, NeuTTS Air, and Qwen3-TTS remain scout-later items. They need
  primary-source license and model-availability verification before joining the
  primary comparison set.

## Next Task

`SO-SPIKE-001-T02` is recorded in
[`R1_LICENSE_PREFLIGHT.md`](R1_LICENSE_PREFLIGHT.md). `SO-SPIKE-001-T03` is
recorded in
[`R1_BENCHMARK_ENVIRONMENT.md`](R1_BENCHMARK_ENVIRONMENT.md). The next task is
`SO-SPIKE-001-T04`, adding external engine-command invocation and result capture
to the benchmark harness.
