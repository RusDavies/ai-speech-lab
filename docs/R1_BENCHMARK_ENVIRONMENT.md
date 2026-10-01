# R1 Benchmark Environment

This document records `SO-SPIKE-001-T03`: the local environment and hardware
profile for the R1 technology comparison spike.

The R1 comparison should answer whether each candidate is worth deeper AI Speech Lab
integration work. The profile below is the first repeatable local baseline, not
a hard constraint on the project. If a candidate is promising but CPU-bound, or
if the comparison needs realistic neural-TTS throughput, the project should add
a cloud VM profile with a modern NVIDIA GPU and run the same cases there.

## Environment ID

`R1-LOCAL-CPU-2026-10`

Use this ID in benchmark result metadata when a run uses the environment defined
here.

## Hardware Profile

- CPU: Intel Core i7-1260P class laptop CPU.
- CPU threads visible to Linux: 16.
- CPU cores reported by Linux: 12.
- Architecture: x86_64.
- RAM: 15 GiB total, with approximately 8 GiB available at capture time.
- Accelerator: no CUDA or ROCm GPU available in this local profile.
- Storage headroom at capture time: approximately 113 GiB free in the working
  filesystem.

Rationale: this is a useful first CPU-only baseline. It can expose setup pain,
basic integration issues, and any plausible low-resource path before GPU
tuning. It must not be used to reject a candidate whose intended operating mode
expects a modern NVIDIA GPU.

## Future Accelerator Profile

If CPU-only results are too slow, inconclusive, or unrepresentative for a
candidate, add a second benchmark environment before making a final fit call.
The expected next profile is a cloud VM with a modern NVIDIA GPU.

The first planned cloud GPU profile is documented in
[`R1_CLOUD_GPU_PROFILE.md`](R1_CLOUD_GPU_PROFILE.md) as
`R1-CLOUD-NVIDIA-L4-2026-10`.

That profile should document:

- cloud provider and VM instance family;
- GPU model and VRAM;
- NVIDIA driver version;
- CUDA toolkit/runtime version;
- container base image or VM image;
- CPU, RAM, and storage;
- whether model weights are cached before timing starts;
- hourly cost at run time, where available.

Suggested environment ID pattern:

`R1-CLOUD-NVIDIA-<GPU>-YYYY-MM`

Do not compare CPU-only and GPU results as if they measure the same deployment
class. Use the local profile for low-resource viability and integration smoke
tests; use the cloud NVIDIA profile for serious neural TTS throughput and
latency assessment.

## Operating System And Runtime

- OS family: Fedora Linux.
- Kernel family at capture time: Linux 7.1 x86_64.
- Container runtime: Podman 5.8 available.
- Host Python observed at capture time: Python 3.14.

Candidate runs should use isolated environments, not the host Python directly.
Several TTS and ML packages are likely to lag current Python releases, so the
default candidate runtime should be Python 3.10 or 3.11 inside a project-local
virtual environment or Podman container.

## Measurement Rules

Each candidate run should record:

- `environment_id`: `R1-LOCAL-CPU-2026-10`.
- CPU thread count used by the candidate runtime.
- whether any GPU/accelerator was used; for this environment the expected value
  is `none`.
- Python version, package manager, and whether the run used Podman or a virtual
  environment.
- candidate source repository, commit, package version, model identifier, and
  model revision where available.
- benchmark case ID from `benchmarks/prototype_cases.jsonl`.
- first-audio latency when the engine supports streaming or incremental audio.
- full-utterance latency for every runnable case.
- cold-start notes separately from steady-state synthesis timings.
- audio artifact path outside git, if audio is generated.
- blocker notes when installation, model access, license, or runtime support
  prevents a run.

Do not mix CPU-only and accelerated results under the same environment ID. A GPU
or NPU profile must get its own environment ID and document its hardware,
drivers, runtime, and cost assumptions before recording results.

## Candidate Execution Policy

- Prefer Podman for heavy or messy candidate stacks.
- Use project-local virtual environments only when the dependency set is small
  and unlikely to interfere with other candidates.
- Keep downloaded models, generated audio, and bulky run artifacts out of git.
- Keep generated sample provenance with the benchmark metadata.
- Do not use private, celebrity, customer, or identity-sensitive voice samples
  during R1.
- Treat F5-TTS results as research-only unless the selected weight-license issue
  is resolved.
- Treat Orpheus as conditional until gated-model terms are recorded.

## Result Location

R1 benchmark result summaries should live in a documented text or JSON artifact
under `benchmarks/` once `SO-SPIKE-001-T04` adds engine invocation and result
capture. Large audio/model artifacts should remain under ignored local
`artifacts/` paths and should not be committed.

## Follow-Up

`SO-SPIKE-001-T04` should extend the benchmark harness so it can invoke an
external engine command and record structured result metadata using explicit
environment IDs.

`SO-SPIKE-001-T03A` is recorded in
[`R1_CLOUD_GPU_PROFILE.md`](R1_CLOUD_GPU_PROFILE.md).
