#!/usr/bin/env python3
"""Run one benchmark case through Chatterbox Turbo.

This is a thin R1 spike adapter for ``scripts/benchmark.py``. It intentionally
keeps generated audio and model caches outside git-controlled paths.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import soundfile as sf
import torch

from chatterbox.tts_turbo import ChatterboxTurboTTS


def load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--threads", type=int, default=8)
    args = parser.parse_args()

    torch.set_num_threads(args.threads)
    case = load_case(args.case)

    load_start = time.perf_counter()
    model = ChatterboxTurboTTS.from_pretrained(args.device)
    load_ms = (time.perf_counter() - load_start) * 1000

    synth_start = time.perf_counter()
    wav = model.generate(case["text"])
    synth_ms = (time.perf_counter() - synth_start) * 1000

    args.out.parent.mkdir(parents=True, exist_ok=True)
    audio = wav.squeeze(0).detach().cpu().numpy()
    sf.write(args.out, audio, model.sr)

    print(
        json.dumps(
            {
                "candidate": "chatterbox-turbo",
                "model_id": "ResembleAI/chatterbox-turbo",
                "package": "chatterbox-tts",
                "device": args.device,
                "torch_threads": args.threads,
                "sample_rate_hz": model.sr,
                "audio_seconds": round(len(audio) / model.sr, 3),
                "model_load_ms": round(load_ms, 3),
                "synthesis_ms": round(synth_ms, 3),
                "first_audio_ms": None,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
