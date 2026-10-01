# R1 License And Provenance Preflight

This document records `SO-SPIKE-001-T02`: license and provenance preflight for
the confirmed R1 candidates. It is not legal advice. It is an engineering
preflight to decide what may be installed, benchmarked, or considered as a
future product base.

## Summary

- Chatterbox Turbo/Nano: acceptable for R1 benchmarking and plausible product
  base, subject to dependency and generated-output checks.
- F5-TTS v1 Base: acceptable for local research benchmarking, but selected
  weights are CC-BY-NC-4.0; treat as non-commercial/reference unless a different
  license path is selected.
- Kokoro 82M: acceptable for R1 benchmarking and plausible fixed-voice baseline.
- Orpheus 3B 0.1 Finetuned: acceptable for R1 benchmarking after gated-model
  access review; plausible product candidate only after model terms and
  acceptable-use constraints are reviewed.
- OpenVoice V2: acceptable optional component candidate, subject to dependency
  and generated-output checks.

## Candidate Findings

### R1-C1: Chatterbox Turbo

- Variant: `ResembleAI/chatterbox-turbo`.
- Model metadata license: MIT.
- Repository license: MIT.
- Model metadata notes: text-to-speech, voice-cloning, English.
- Gating: not gated in model metadata.
- Preflight status: pass for R1 benchmark.
- Product-base status: plausible, pending dependency audit and generated-output
  policy.
- Primary evidence:
  - <https://huggingface.co/api/models/ResembleAI/chatterbox-turbo>
  - <https://raw.githubusercontent.com/resemble-ai/chatterbox/master/LICENSE>

### R1-C2: Chatterbox Nano

- Variant: `ResembleAI/chatterbox-nano`.
- Model metadata license: MIT.
- Repository license: MIT.
- Model metadata notes: text-to-speech, voice-cloning, English.
- Gating: not gated in model metadata.
- Preflight status: pass for R1 benchmark.
- Product-base status: plausible, pending dependency audit and generated-output
  policy.
- Primary evidence:
  - <https://huggingface.co/api/models/ResembleAI/chatterbox-nano>
  - <https://raw.githubusercontent.com/resemble-ai/chatterbox/master/LICENSE>

### R1-C3: F5-TTS v1 Base

- Variant: `SWivid/F5-TTS`, checkpoint family `F5TTS_v1_Base`.
- Model metadata license: CC-BY-NC-4.0.
- Repository code license: MIT.
- Dataset metadata noted by model card: `amphion/Emilia-Dataset`.
- Gating: not gated in model metadata.
- Preflight status: pass for local research benchmark only.
- Product-base status: blocked for commercial/product use unless the
  non-commercial weight license is acceptable or a differently licensed
  checkpoint is selected.
- Primary evidence:
  - <https://huggingface.co/api/models/SWivid/F5-TTS>
  - <https://raw.githubusercontent.com/SWivid/F5-TTS/main/LICENSE>

### R1-C4: Kokoro 82M

- Variant: `hexgrad/Kokoro-82M`.
- Model metadata license: Apache-2.0.
- Repository license checked: Apache-2.0.
- Model metadata notes: fixed-voice text-to-speech model; base model references
  StyleTTS2-LJSpeech.
- Gating: not gated in model metadata.
- Preflight status: pass for R1 benchmark.
- Product-base status: plausible as fixed-voice baseline/component, not as the
  full voice-cloning engine.
- Primary evidence:
  - <https://huggingface.co/api/models/hexgrad/Kokoro-82M>
  - <https://raw.githubusercontent.com/hexgrad/kokoro/main/LICENSE>

### R1-C5: Orpheus 3B 0.1 Finetuned

- Variant: `canopylabs/orpheus-3b-0.1-ft`.
- Model metadata license: Apache-2.0.
- Repository license checked: Apache-2.0.
- Model metadata notes: based on `canopylabs/orpheus-3b-0.1-pretrained`.
- Gating: `auto` in model metadata.
- Model-card acceptable-use note: do not use for impersonation without consent,
  misinformation, deception, illegal, or harmful activity.
- Preflight status: conditional pass for R1 benchmark after access/terms review.
- Product-base status: plausible only after gated access terms, model-card
  restrictions, dependencies, and output policy are reviewed.
- Primary evidence:
  - <https://huggingface.co/api/models/canopylabs/orpheus-3b-0.1-ft>
  - <https://huggingface.co/canopylabs/orpheus-3b-0.1-ft>
  - <https://raw.githubusercontent.com/canopyai/Orpheus-TTS/main/LICENSE>

### R1-O1: OpenVoice V2

- Variant: OpenVoice V2 from `myshell-ai/OpenVoice`.
- Repository license: MIT.
- Repository notes: V1 and V2 are MIT licensed and free for commercial/research
  use; V2 adds better quality and native multilingual support.
- Gating: not applicable for the source repository.
- Preflight status: pass as optional R1 component candidate.
- Product-base status: plausible component, not complete engine by itself.
- Primary evidence:
  - <https://github.com/myshell-ai/OpenVoice>
  - <https://raw.githubusercontent.com/myshell-ai/OpenVoice/main/LICENSE>

## Provisional Spike Policy

- Do not use private, celebrity, customer, or identity-sensitive voice samples
  during R1.
- Use only synthetic/public-safe reference clips or engine-provided examples
  unless a separate consent/provenance record is created.
- Do not commit generated bulk audio to git.
- Store benchmark run metadata separately from generated audio artifacts.
- Treat F5-TTS output and derived artifacts as non-commercial/research-only
  unless the weight-license issue is resolved.
- Treat Orpheus as gated/conditional until access terms are explicitly recorded.

## Follow-Up

`SO-SPIKE-001-T03` should define the local benchmark environment and hardware
profile. `SO-SPIKE-001-T04` should add engine-command invocation and result
capture to the benchmark harness before any candidate benchmark run.

