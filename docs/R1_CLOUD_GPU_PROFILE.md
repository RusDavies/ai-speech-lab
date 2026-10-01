# R1 Cloud GPU Benchmark Profile

This document records `SO-SPIKE-001-T03A`: the first cloud NVIDIA GPU benchmark
profile for R1 candidate comparisons.

The local CPU environment is useful for smoke tests, setup pain, and
low-resource viability. It is not a hard project constraint and must not be used
as the final latency basis for models whose intended runtime is CUDA.

## Environment ID

`R1-CLOUD-NVIDIA-L4-2026-10`

Use this ID in benchmark metadata only when the run matches the profile below.

## Chosen Profile

- Accelerator class: NVIDIA L4.
- GPU VRAM: 24 GB GDDR6.
- GPU count: 1.
- Preferred VM shape: Google Compute Engine `g2-standard-8`.
- Preferred VM CPU/RAM: 8 vCPU, 32 GB RAM.
- Alternate minimum VM shape: any cloud VM with one NVIDIA L4, at least 8 vCPU,
  32 GB RAM, and 200 GB boot/data storage.
- Operating system target: Ubuntu 22.04 LTS or Ubuntu 24.04 LTS GPU image.
- Container/runtime target: Podman with NVIDIA Container Toolkit CDI support,
  or a CUDA-ready VM environment where Podman is not practical.
- CUDA target: CUDA 12.x runtime compatible with the selected candidate stack.
- Storage target: at least 200 GB available for model weights, build caches,
  generated audio, and benchmark artifacts.

## Cost Policy

Do not bake a fixed hourly rate into benchmark results. Cloud GPU pricing varies
by provider, region, reservation/spot mode, and date.

Before any billable run, record:

- provider;
- region/zone;
- VM shape;
- accelerator model/count;
- on-demand, spot, reserved, or marketplace mode;
- quoted hourly VM cost;
- quoted hourly GPU cost when itemized separately;
- expected maximum runtime budget for the run.

Store that cost capture with the benchmark run metadata or comparison notes.

## When To Use This Profile

Use `R1-CLOUD-NVIDIA-L4-2026-10` when:

- CPU-only results are too slow to be informative;
- CPU-only results are inconclusive;
- a candidate's documented runtime expects CUDA;
- local setup succeeds but latency is not representative;
- a candidate is promising enough that GPU evidence is worth paid runtime.

Do not use this profile merely to hide poor integration quality. Installation
failures, missing model access, license blockers, and broken candidate wrappers
should still be recorded as blockers.

## Measurement Rules

Each GPU run should record everything required by
[`BENCHMARK_HARNESS.md`](BENCHMARK_HARNESS.md), plus:

- GPU model and VRAM observed by `nvidia-smi`;
- NVIDIA driver version;
- CUDA runtime/toolkit version;
- container image digest or VM image identifier;
- `nvidia-container-toolkit` version when using containers;
- whether model weights were pre-downloaded before timing;
- whether the first measured case includes cold model load;
- GPU memory peak when easy to collect;
- GPU utilization summary when easy to collect.

Cold-start and steady-state timings must be separated. The first synthesis after
install/model download should not be blended into steady-state latency.

## Comparison Rules

- Compare CPU and GPU results as separate deployment classes.
- Use CPU results for low-resource viability and smoke-test evidence.
- Use L4 GPU results for serious neural TTS throughput and latency evidence.
- Do not reject a CUDA-oriented candidate on latency until either this GPU
  profile has run or a specific non-latency blocker has been recorded.
- Do not treat an L4 pass as proof of the final sub-200 ms goal. It is R1
  evidence, not the final runtime architecture.

## Provisioning Notes

Provisioning is intentionally out of scope for this document. This profile does
not authorize creating cloud resources. When a benchmark run is approved, create
or use a disposable GPU VM, capture the machine facts, run the benchmark harness,
copy back only provenance-safe summaries, and tear down the VM promptly.

Primary setup references:

- Google Compute Engine GPU documentation for G2 machine series with NVIDIA L4.
- NVIDIA Container Toolkit installation documentation, including Podman CDI
  support.
