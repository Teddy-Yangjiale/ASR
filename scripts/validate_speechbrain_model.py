#!/usr/bin/env python3
"""Validate locally cached SpeechBrain model files before running inference."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_FILES = [
    "hyperparams.yaml",
    "asr.ckpt",
    "lm.ckpt",
    "normalizer.ckpt",
    "tokenizer.ckpt",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--savedir", type=Path, default=Path("models/speechbrain_pretrained"))
    args = parser.parse_args()

    missing = [name for name in REQUIRED_FILES if not (args.savedir / name).exists()]
    if missing:
        raise SystemExit(f"Missing model files in {args.savedir}: {', '.join(missing)}")

    try:
        import torch
    except ImportError as exc:
        raise SystemExit("Install torch before validating checkpoint files.") from exc

    for name in ["asr.ckpt", "lm.ckpt", "normalizer.ckpt", "tokenizer.ckpt"]:
        path = args.savedir / name
        try:
            torch.load(path, map_location="cpu")
        except Exception as exc:
            raise SystemExit(
                f"Invalid checkpoint file: {path}. "
                "Delete it and rerun `make cache-speechbrain-model-direct`. "
                f"Original error: {type(exc).__name__}: {exc}"
            ) from exc
        print(f"Checkpoint OK: {path}")

    print(f"SpeechBrain model cache is valid: {args.savedir}")


if __name__ == "__main__":
    main()
