#!/usr/bin/env python3
"""Run one benchmark case through F5-TTS v1 Base.

This is a thin R1 spike adapter for ``scripts/benchmark.py``. It uses the
public example reference clip bundled with F5-TTS and keeps generated audio and
model caches outside git-controlled paths.
"""

from __future__ import annotations

import argparse
import json
import time
from importlib.resources import files
from pathlib import Path

import torch

from f5_tts.api import F5TTS


REF_TEXT = "Some call me nature, others call me mother nature."


def load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--hf-cache-dir", default="artifacts/f5tts-hf-cache")
    args = parser.parse_args()

    torch.set_num_threads(args.threads)
    case = load_case(args.case)
    ref_audio = files("f5_tts").joinpath("infer/examples/basic/basic_ref_en.wav")

    load_start = time.perf_counter()
    model = F5TTS(
        model="F5TTS_v1_Base",
        device=args.device,
        hf_cache_dir=args.hf_cache_dir,
    )
    load_ms = (time.perf_counter() - load_start) * 1000

    args.out.parent.mkdir(parents=True, exist_ok=True)
    synth_start = time.perf_counter()
    wav, sr, _ = model.infer(
        ref_file=str(ref_audio),
        ref_text=REF_TEXT,
        gen_text=case["text"],
        file_wave=str(args.out),
        seed=20261002,
    )
    synth_ms = (time.perf_counter() - synth_start) * 1000

    print(
        json.dumps(
            {
                "candidate": "f5-tts-v1-base",
                "model_id": "SWivid/F5-TTS/F5TTS_v1_Base/model_1250000.safetensors",
                "package": "f5-tts",
                "device": args.device,
                "torch_threads": args.threads,
                "sample_rate_hz": sr,
                "audio_seconds": round(len(wav) / sr, 3),
                "model_load_ms": round(load_ms, 3),
                "synthesis_ms": round(synth_ms, 3),
                "first_audio_ms": None,
                "reference_audio": "f5_tts bundled basic_ref_en.wav",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
