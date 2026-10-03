#!/usr/bin/env python3
"""Run one benchmark case through Kokoro 82M.

This is a thin R1 spike adapter for ``scripts/benchmark.py``. It keeps model
caches and generated audio outside git-controlled paths.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from importlib import metadata
from pathlib import Path


SAMPLE_RATE_HZ = 24000


def load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument("--language", default="a")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--hf-cache-dir", default="artifacts/kokoro-hf-cache")
    parser.add_argument("--xdg-cache-dir", default="artifacts/kokoro-xdg-cache")
    args = parser.parse_args()

    os.environ.setdefault("HF_HOME", args.hf_cache_dir)
    os.environ.setdefault("XDG_CACHE_HOME", args.xdg_cache_dir)

    import numpy as np
    import soundfile as sf
    import torch
    from kokoro import KPipeline

    torch.set_num_threads(args.threads)
    case = load_case(args.case)

    load_start = time.perf_counter()
    pipeline = KPipeline(
        lang_code=args.language,
        repo_id="hexgrad/Kokoro-82M",
        device=args.device,
    )
    load_ms = (time.perf_counter() - load_start) * 1000

    args.out.parent.mkdir(parents=True, exist_ok=True)

    synth_start = time.perf_counter()
    chunks: list[np.ndarray] = []
    chunk_details: list[dict[str, object]] = []
    first_audio_ms = None
    for result in pipeline(
        case["text"],
        voice=args.voice,
        speed=args.speed,
        split_pattern=r"\n+",
    ):
        if result.audio is None:
            continue
        if first_audio_ms is None:
            first_audio_ms = (time.perf_counter() - synth_start) * 1000
        audio = result.audio.detach().cpu().numpy()
        chunks.append(audio)
        chunk_details.append(
            {
                "chars": len(result.graphemes),
                "phonemes": len(result.phonemes),
                "audio_seconds": round(len(audio) / SAMPLE_RATE_HZ, 3),
            }
        )
    synth_ms = (time.perf_counter() - synth_start) * 1000

    if not chunks:
        raise RuntimeError("Kokoro produced no audio chunks")

    audio = np.concatenate(chunks)
    sf.write(args.out, audio, SAMPLE_RATE_HZ)

    print(
        json.dumps(
            {
                "candidate": "kokoro-82m",
                "model_id": "hexgrad/Kokoro-82M",
                "package": f"kokoro=={metadata.version('kokoro')}",
                "device": args.device,
                "torch_threads": args.threads,
                "sample_rate_hz": SAMPLE_RATE_HZ,
                "audio_seconds": round(len(audio) / SAMPLE_RATE_HZ, 3),
                "model_load_ms": round(load_ms, 3),
                "synthesis_ms": round(synth_ms, 3),
                "first_audio_ms": round(first_audio_ms, 3) if first_audio_ms is not None else None,
                "voice": args.voice,
                "language": args.language,
                "speed": args.speed,
                "chunk_count": len(chunks),
                "chunk_details": chunk_details,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
