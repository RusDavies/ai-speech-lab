# Technology Options

AI Speech Lab should not begin as a from-scratch neural TTS training effort. The
initial strategy is to benchmark and integrate existing open or open-weight TTS
systems, then decide whether to adapt, wrap, optimize, or replace specific
components.

No single reviewed option currently satisfies the whole product goal by itself:
Alexa-class expressiveness, authorized arbitrary voice adaptation, explicit and
synthesized prosody, clean product-friendly licensing, and sub-200 ms
interactive latency. Several are close enough to deserve comparison.

## Evaluation Axes

- Naturalness and expressiveness.
- Voice adaptation or cloning from an authorized sample.
- Prosody and emotion control.
- First-audio latency and full-utterance latency.
- Hardware/runtime practicality.
- License suitability for an open-source product.
- Maintenance health and integration complexity.
- Safety/provenance hooks for voice samples and generated outputs.

## Primary Comparison Candidates

### T1: Chatterbox

Role: leading practical candidate for the first comparison spike.

Fit:

- Zero-shot voice cloning.
- Expressive controls such as exaggeration and paralinguistic tags.
- English, multilingual, low-latency Turbo, and smaller Nano variants.
- Claims MIT licensing and product-oriented packaging.

Risks:

- Need local verification of latency and quality.
- Need to distinguish open model behavior from provider-hosted performance
  claims.
- Need to test hallucination/repetition behavior on AI Speech Lab benchmark cases.

Initial use:

- Benchmark Turbo/Nano for first-audio latency, prosody tags, and voice
  adaptation quality.

Source: <https://github.com/resemble-ai/chatterbox>

### T2: F5-TTS

Role: strong research/product candidate for zero-shot TTS and optimized runtime
comparison.

Fit:

- Modern flow-matching TTS with zero-shot voice-cloning style workflows.
- Repo documents optimized Triton/TensorRT-LLM deployment paths.
- Reported optimized client-server latency around 253 ms on one L20 setup.

Risks:

- Need local install and license verification.
- May need substantial runtime work to reach AI Speech Lab's final sub-200 ms target.
- Product ergonomics may require wrapping.

Initial use:

- Benchmark as a serious voice-adaptation and runtime-optimization candidate.

Source: <https://github.com/SWivid/F5-TTS>

### T3: Kokoro

Role: fast fixed-voice baseline and possible low-latency component reference.

Fit:

- Small 82M open-weight model.
- Apache-licensed weights.
- Strong speed/cost profile.
- Useful as a known-fast quality and latency baseline.

Risks:

- No arbitrary voice cloning.
- Limited direct prosody control relative to AI Speech Lab's goal.

Initial use:

- Benchmark for low-latency fixed-voice TTS and compare other candidates against
  its speed.

Source: <https://huggingface.co/hexgrad/Kokoro-82M>

### T4: Orpheus

Role: expressive low-latency candidate worth benchmarking.

Fit:

- Llama-based open-weight TTS.
- Zero-shot voice cloning.
- Guided emotion and intonation tags.
- Streaming latency claims around 200 ms, with lower claims for input streaming.

Risks:

- License and model-weight terms need careful review.
- Likely heavier deployment profile than Kokoro or Piper.
- Need local confirmation of tag controllability and output stability.

Initial use:

- Benchmark expressive tags, streaming behavior, and setup complexity.

Source: <https://github.com/canopyai/Orpheus-TTS>

### T5: OpenVoice

Role: possible voice-adaptation or voice-conversion component.

Fit:

- MIT-licensed project.
- Designed around instant voice cloning and tone-color transfer.
- Useful if AI Speech Lab separates base speech generation from target-voice
  adaptation.

Risks:

- Not a complete answer to expressive TTS by itself.
- Needs pairing with a base TTS system and quality testing.

Initial use:

- Scout as a component after primary engine candidates are benchmarked.

Source: <https://github.com/myshell-ai/OpenVoice>

## Baselines And References

### B1: Piper

Role: fast local CPU/offline baseline.

Fit:

- Fast, local neural TTS.
- Useful for CPU and embedded latency comparison.

Risks:

- Original repository is archived.
- Fixed-voice orientation; no arbitrary voice cloning.
- Not expressive enough for the full AI Speech Lab goal.

Source: <https://github.com/rhasspy/piper>

### B2: XTTS-v2

Role: voice-cloning benchmark and reference, not an obvious product base.

Fit:

- Voice cloning from short reference audio.
- Cross-language cloning and multilingual support.
- Better prosody and audio quality than earlier XTTS versions.

Risks:

- Coqui Public Model License is not a clean permissive open-source model license.
- Long-term maintenance risk after Coqui's corporate shutdown.
- Prosody control may be less explicit than AI Speech Lab needs.

Source: <https://huggingface.co/coqui/XTTS-v2>

### B3: StyleTTS2

Role: research baseline for naturalness, style modeling, and architecture ideas.

Fit:

- Strong human-level naturalness claims in the paper/repo.
- Style diffusion and speaker adaptation ideas are directly relevant.

Risks:

- More research-code-oriented than product-engine-oriented.
- Low-latency deployment and safety/provenance layers would need significant
  work.

Source: <https://github.com/yl4579/StyleTTS2>

### B4: Dia

Role: expressive-dialogue reference.

Fit:

- Realistic dialogue generation.
- Emotion/tone conditioning and nonverbal tags.
- Audio-prompt conditioning for speaker consistency.

Risks:

- Large 1.6B model.
- English-focused at the reviewed point.
- Not obviously a low-latency general TTS base.

Source: <https://github.com/nari-labs/dia>

### B5: Fish Speech / Fish Audio S2

Role: frontier reference, not current product base.

Fit:

- Rich emotion/prosody tag control.
- Multilingual, multi-speaker, and high-quality claims.

Risks:

- Research license, large model size, and more complicated product/legal story.
- Heavier than needed for the first prototype.

Source: <https://github.com/fishaudio/fish-speech>

## Scout-Later Candidates

- Spark-TTS: promising Qwen-based single-stream TTS with voice cloning and
  prosody control claims. Needs primary-source license and benchmark review.
- NeuTTS Air: promising on-device voice cloning claims. Needs primary-source
  review and hardware verification.
- Qwen3-TTS: attractive public claims around voice cloning and latency. Needs
  official source/license verification before being treated as a candidate.

## Current Recommendation

Run a bounded comparison spike before selecting an architecture.

Initial comparison set:

- `R1-C1` Chatterbox Turbo;
- `R1-C2` Chatterbox Nano;
- `R1-C3` F5-TTS v1 Base;
- `R1-C4` Kokoro 82M;
- `R1-C5` Orpheus 3B 0.1 Finetuned;
- optional `R1-O1` OpenVoice V2 component test.

Exact variants for the comparison spike are tracked in
[`R1_CANDIDATE_SET.md`](R1_CANDIDATE_SET.md).

License and provenance preflight for the confirmed variants is tracked in
[`R1_LICENSE_PREFLIGHT.md`](R1_LICENSE_PREFLIGHT.md).

The comparison should use the existing AI Speech Lab benchmark cases and report:

- install/setup friction;
- license fit;
- first-audio latency;
- full-utterance latency;
- output naturalness;
- prosody controllability;
- voice adaptation quality where supported;
- artifacts, hallucinations, or off-prompt speech;
- hardware and runtime requirements.

Do not start a from-scratch model until existing systems have failed in a
specific, measured way.
