# Decisions

## Pending

- Select first prototype interface.
- Select initial TTS stack or research implementation path.
- Select first prosody metadata representation.
- Select voice-sample consent and provenance model.
- Decide when candidate evidence justifies a paid cloud GPU run.
- Make the product repository public only after clean-history/public-readiness
  checks pass.
- Run the remaining R1 technology comparison tasks across the strongest
  candidates.
- Record explicit Orpheus and Llama gated-access acceptance before spending a
  cloud NVIDIA GPU run on Orpheus.

## 2026-10-01: First Prototype Acceptance And Harness Scope

Decision: define acceptance around measurable prototype evidence, not final
quality. The benchmark harness validates public-safe text/prosody cases, can
invoke an external engine command per case, and records structured JSONL run
metadata.

Rationale: the model/runtime path is not selected yet, so the harness stays
engine-agnostic. Candidate-specific wrappers can adapt model CLIs or APIs into a
common command-template contract.

## 2026-10-01: Technology Strategy

Decision: do not start AI Speech Lab as a from-scratch model-training project.
Evaluate existing open-source and open-weight TTS systems first, then build
AI Speech Lab as a benchmarked integration/adaptation engine around the strongest
candidate or combination of candidates.

Recommended first comparison set:

- Chatterbox Turbo or Nano;
- F5-TTS;
- Kokoro;
- Orpheus;
- optional OpenVoice component test.

Rationale: no reviewed option satisfies every AI Speech Lab requirement by itself,
but several are close enough to make integration and measurement the fastest
credible path.

## 2026-10-01: R1 Candidate Variants

Decision: confirm the first comparison spike variants as Chatterbox Turbo,
Chatterbox Nano, F5-TTS v1 Base, Kokoro 82M, Orpheus 3B 0.1 Finetuned, and
optional OpenVoice V2.

Rationale: these variants cover the key trade-space for AI Speech Lab: low-latency
voice agents, CPU/on-device operation, zero-shot voice adaptation, fixed-voice
latency baseline, expressive tag control, and optional tone-color transfer.

## 2026-10-01: R1 License Preflight

Decision: allow R1 benchmarking for Chatterbox Turbo, Chatterbox Nano, Kokoro
82M, and OpenVoice V2; allow Orpheus 3B 0.1 Finetuned only after gated access
terms are recorded; allow F5-TTS v1 Base only as non-commercial/research
benchmark evidence unless its selected weight-license issue is resolved.

Rationale: Chatterbox metadata and repository license are MIT; Kokoro metadata
and repository license are Apache-2.0; OpenVoice is MIT; Orpheus metadata and
repository license are Apache-2.0 but the model is gated and has explicit misuse
warnings; F5-TTS code is MIT but selected model weights are CC-BY-NC-4.0.

## 2026-10-01: R1 Benchmark Environment

Decision: use `R1-LOCAL-CPU-2026-10` as the first R1 comparison environment.
It is a CPU-only x86_64 local profile with 16 visible Linux threads, 15 GiB RAM,
Podman available, and no CUDA/ROCm accelerator available. This is not a hard
hardware constraint on AI Speech Lab.

Candidate runs should use isolated Python 3.10 or 3.11 environments, preferably
Podman for heavy stacks, rather than the host Python 3.14 runtime.

Rationale: the first comparison needs repeatable local evidence before GPU or
deployment-specific optimization. CPU-only results will expose setup pain,
baseline latency, and low-resource viability without conflating that evidence
with accelerator-specific tuning. Promising candidates that expect accelerator
runtime should be evaluated again on a documented cloud NVIDIA GPU profile
before any rejection based on latency.

## 2026-10-01: R1 Harness Engine Invocation

Decision: add command-template engine invocation to `scripts/benchmark.py`.
The harness writes per-case JSON files, passes a suggested output path, measures
full process time as `full_utterance_ms`, optionally parses engine-reported JSON
from stdout, and appends JSONL results under ignored artifacts by default.

Rationale: R1 candidates have different CLIs and APIs. A command-template
boundary keeps the harness stable while allowing thin candidate wrappers to
normalize invocation, timing, and output capture.

## 2026-10-01: R1 Cloud GPU Profile

Decision: define `R1-CLOUD-NVIDIA-L4-2026-10` as the first cloud accelerator
benchmark profile. The preferred shape is a single NVIDIA L4 with 24 GB VRAM,
using Google Compute Engine `g2-standard-8` or an equivalent cloud VM with at
least 8 vCPU, 32 GB RAM, and 200 GB storage.

Rationale: L4 is modern enough to be representative for CUDA-oriented neural
TTS inference, widely available, and less financially silly than jumping
straight to H100-class hardware. It provides a fairer latency profile for
Chatterbox, F5-TTS, Orpheus, or similar candidates before negative latency
judgments are made.

## 2026-10-01: Product License

Decision: use Apache-2.0 for the AI Speech Lab product repository.

Rationale: Apache-2.0 is permissive enough for open-source adoption while
including an explicit patent license and termination clause. That is a better
default for a TTS/runtime project than MIT while the eventual implementation,
model integration, and contributor surface are still forming.

## 2026-10-07: Orpheus Local R1 Deferral

Decision: record Orpheus 3B 0.1 Finetuned as locally blocked rather than failed.
Keep it in the R1 comparison only as a gated/CUDA candidate until access terms
are reviewed and it can be run on the documented NVIDIA L4 profile or equivalent
CUDA host.

Rationale: `orpheus-speech==0.1.0` installed, but the selected Orpheus model,
the package's default finetuned model alias, and the tokenizer/pretrained model
repository all returned gated-access errors from Hugging Face in the local run.
The current local R1 profile also has no CUDA driver/device, while the upstream
package imports a SNAC decoder that initializes on CUDA and uses `vllm` for
inference.

## 2026-10-09: Orpheus Gated Access Review

Decision: allow Orpheus to proceed to a bounded R1 cloud/CUDA benchmark only
after an authorized maintainer accepts and records the relevant Hugging Face
gated access conditions. Do not treat R1 access as product-base approval.

Rationale: the visible Orpheus model page and API report Apache-2.0 metadata,
but the selected finetuned and pretrained repositories are gated and require
contact-information sharing before file access. The visible model card also
prohibits impersonation without consent, deception, misinformation, illegal
activity, and harmful use. The visible model tree names
`meta-llama/Llama-3.2-3B-Instruct` as an upstream base, so any product-base
decision must separately satisfy Llama 3.2 license and acceptable-use
obligations.

## 2026-10-01: Public Release Route

Decision: prepare a clean-history public release candidate for the product
repository before any visibility change. The current private product repo is the
working source of truth, but its early bootstrap history contains channel
provenance, so publication should use an orphan-reset or equivalent clean export
instead of simply flipping the existing history public.

Rationale: the current working tree is product-oriented and public-safe after
readiness edits, but public Git history should not expose channel or
management-provenance artifacts.
