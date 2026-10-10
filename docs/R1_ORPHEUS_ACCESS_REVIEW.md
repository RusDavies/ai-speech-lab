# R1 Orpheus Gated Access Review

This records `SO-SPIKE-001-T08A`: review Orpheus gated-model access terms before
any further Orpheus benchmark run. It is not legal advice.

## Verdict: CONDITIONAL R1 ACCESS ONLY

Question: Should AI Speech Lab request and use gated Hugging Face access for
Orpheus 3B 0.1 Finetuned in the R1 comparison?

Decision: yes, for bounded R1 benchmarking only, after an authorized maintainer
accepts the Hugging Face gated-model conditions with the project account that
will run the benchmark. Do not treat this as product-base approval yet.

Rationale:

- The selected Orpheus finetuned and pretrained repositories are public model
  pages but require gated Hugging Face access before files can be downloaded.
- The visible Hugging Face model card reports `apache-2.0` metadata for the
  selected finetuned model and asks the user to share contact information before
  accessing files.
- The visible model-card misuse terms prohibit impersonation without consent,
  misinformation, deception, illegal activity, and harmful activity.
- The visible model tree identifies `meta-llama/Llama-3.2-3B-Instruct` as an
  upstream base model. That means product-base approval must also account for
  the Llama 3.2 Community License and Acceptable Use Policy, not only the
  Orpheus Apache-2.0 metadata.
- The local R1 run already showed that unauthenticated access is blocked and
  that this host is not an appropriate CUDA/vLLM benchmark environment.

## Access Conditions To Record Before The GPU Run

Before `SO-SPIKE-001-T08B`, record:

- the accepting Hugging Face account or organization;
- the date access was accepted;
- the exact Orpheus repositories approved, at minimum
  `canopylabs/orpheus-3b-0.1-ft` and
  `canopylabs/orpheus-3b-0.1-pretrained`;
- whether the package default model
  `canopylabs/orpheus-tts-0.1-finetune-prod` is separately approved;
- the visible gated-access conditions shown during acceptance;
- whether Llama 3.2 terms were accepted by the same responsible account;
- the cloud/CUDA environment profile used for the rerun.

Do not commit Hugging Face tokens, approval screenshots, private account
details, generated bulk audio, or voice material.

## R1 Usage Boundaries

Allowed for the R1 comparison:

- install Orpheus in an isolated environment;
- download approved model files using a token supplied outside git;
- run the public-safe benchmark cases already used for other R1 candidates;
- use built-in/sample Orpheus voices such as `tara`;
- record setup, latency, quality notes, blocker evidence, and fit judgment.

Not allowed without a separate consent/provenance task:

- private, customer, celebrity, family, or identity-sensitive voice samples;
- impersonation tests;
- deception, fraud, misinformation, robocall, or undisclosed synthetic-voice
  scenarios;
- committing generated audio or model/cache artifacts to git;
- treating Orpheus as product-approved solely because the R1 benchmark ran.

## Product-Base Implications

Orpheus remains a plausible expressive/streaming candidate, but it is still
conditional as a product base. A later product-base decision must verify:

- Orpheus gated terms accepted and preserved in a private approval record;
- Llama 3.2 license and acceptable-use obligations are compatible with the
  intended AI Speech Lab distribution and service model;
- attribution, notice, naming, and "Built with Llama" style obligations are
  handled if applicable;
- voice-consent and synthetic-speech disclosure policy exists;
- dependency, deployment, and output-provenance reviews are complete.

## Sources Checked

- Hugging Face model page, `canopylabs/orpheus-3b-0.1-ft`, checked
  2026-10-09: gated access is required, license metadata is `apache-2.0`,
  model card lists Orpheus capabilities and misuse restrictions, and the visible
  model tree includes `meta-llama/Llama-3.2-3B-Instruct`.
- Hugging Face API, `canopylabs/orpheus-3b-0.1-ft`, checked 2026-10-09:
  `gated` is `auto`, `private` is `false`, `disabled` is `false`, and card
  data reports `license: apache-2.0`.
- Hugging Face API, `canopylabs/orpheus-3b-0.1-pretrained`, checked
  2026-10-09: `gated` is `auto`, `private` is `false`, `disabled` is `false`,
  and card data reports `license: apache-2.0`.
- Orpheus GitHub repository, checked 2026-10-09: repository is public,
  Apache-2.0 licensed, documents vLLM-based inference, Baseten deployment, no-GPU
  implementation notes, voice names, emotion tags, and fine-tuning notes.
- Meta Llama 3.2 Hugging Face model page, checked 2026-10-09: model license is
  `llama3.2`; visible terms include contact-information sharing for access,
  redistribution/attribution requirements, acceptable-use-policy compliance,
  and the 700M monthly-active-user commercial-license threshold.
