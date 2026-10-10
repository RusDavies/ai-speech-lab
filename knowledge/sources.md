# Sources

No external technical sources have been ingested yet.

Initial project intent source:

- Owner brief, 2026-10-01: the project is an open source TTS engine that accepts
  text, may accept or synthesize intonation, should sound as expressive and
  natural as current Alexa, can adapt to an authorized speaker from a voice
  sample, and ultimately targets latency below 200 ms.

Local benchmark environment source:

- Local system capture, 2026-10-01: `uname -a`, `lscpu`, `free -h`, filesystem
  free-space check, accelerator probes, `python3 --version`, and
  `podman --version`.

## Technology Option Sources

- Chatterbox source and model-family notes: <https://github.com/resemble-ai/chatterbox>
- Chatterbox Turbo model card: <https://huggingface.co/ResembleAI/chatterbox-turbo>
- Chatterbox Turbo model metadata: <https://huggingface.co/api/models/ResembleAI/chatterbox-turbo>
- Chatterbox Nano model card: <https://huggingface.co/ResembleAI/chatterbox-nano>
- Chatterbox Nano model metadata: <https://huggingface.co/api/models/ResembleAI/chatterbox-nano>
- Chatterbox license: <https://raw.githubusercontent.com/resemble-ai/chatterbox/master/LICENSE>
- F5-TTS source and runtime notes: <https://github.com/SWivid/F5-TTS>
- F5-TTS model card: <https://huggingface.co/SWivid/F5-TTS>
- F5-TTS model metadata: <https://huggingface.co/api/models/SWivid/F5-TTS>
- F5-TTS code license: <https://raw.githubusercontent.com/SWivid/F5-TTS/main/LICENSE>
- Kokoro model card: <https://huggingface.co/hexgrad/Kokoro-82M>
- Kokoro model metadata: <https://huggingface.co/api/models/hexgrad/Kokoro-82M>
- Kokoro license: <https://raw.githubusercontent.com/hexgrad/kokoro/main/LICENSE>
- Orpheus source and model notes: <https://github.com/canopyai/Orpheus-TTS>
- Orpheus 3B finetuned model card: <https://huggingface.co/canopylabs/orpheus-3b-0.1-ft>
- Orpheus 3B finetuned model metadata: <https://huggingface.co/api/models/canopylabs/orpheus-3b-0.1-ft>
- Orpheus 3B pretrained model metadata: <https://huggingface.co/api/models/canopylabs/orpheus-3b-0.1-pretrained>
- Orpheus code license: <https://raw.githubusercontent.com/canopyai/Orpheus-TTS/main/LICENSE>
- Llama 3.2 3B Instruct model card and license text:
  <https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct>
- OpenVoice source: <https://github.com/myshell-ai/OpenVoice>
- OpenVoice license: <https://raw.githubusercontent.com/myshell-ai/OpenVoice/main/LICENSE>
- Piper source archive: <https://github.com/rhasspy/piper>
- XTTS-v2 model card: <https://huggingface.co/coqui/XTTS-v2>
- StyleTTS2 source and paper link: <https://github.com/yl4579/StyleTTS2>
- Dia source and model notes: <https://github.com/nari-labs/dia>
- Fish Speech source and model notes: <https://github.com/fishaudio/fish-speech>

## Benchmark Environment Sources

- Google Compute Engine GPU documentation, G2 machine series with NVIDIA L4:
  <https://cloud.google.com/compute/docs/gpus>
- Google Compute Engine GPU VM creation notes, including GPU VM images with
  NVIDIA drivers and CUDA Toolkit:
  <https://cloud.google.com/compute/docs/gpus/create-vm-with-gpus>
- NVIDIA Container Toolkit installation documentation, including Podman/CDI
  support:
  <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>

## Benchmark Run Sources

- Chatterbox Turbo local CPU run, 2026-10-02:
  `benchmarks/r1_chatterbox_turbo.md`.
- F5-TTS v1 Base local CPU run, 2026-10-02:
  `benchmarks/r1_f5tts_v1_base.md`.
- Kokoro 82M local CPU run, 2026-10-02:
  `benchmarks/r1_kokoro_82m.md`.
- Orpheus 3B 0.1 Finetuned local preflight run, 2026-10-07:
  `benchmarks/r1_orpheus_3b_0_1_ft.md`.
- Orpheus gated-access review, 2026-10-09:
  `docs/R1_ORPHEUS_ACCESS_REVIEW.md`.
