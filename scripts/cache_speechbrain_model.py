#!/usr/bin/env python3
"""Download/cache a SpeechBrain pretrained ASR model without running inference."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="speechbrain/asr-transformer-transformerlm-librispeech")
    parser.add_argument("--savedir", default="models/speechbrain_pretrained")
    args = parser.parse_args()

    try:
        from speechbrain.inference.ASR import EncoderDecoderASR

        EncoderDecoderASR.from_hparams(source=args.source, savedir=args.savedir)
    except Exception as exc:
        raise SystemExit(
            "Failed to cache SpeechBrain model. "
            "This usually means Hugging Face is unreachable from WSL, or the model cache is incomplete. "
            "Run `make hf-check`, verify proxy/VPN settings, or manually download the model into "
            f"{Path(args.savedir)}. Original error: {type(exc).__name__}: {exc}"
        ) from exc

    print(f"SpeechBrain model cached in {args.savedir}")


if __name__ == "__main__":
    main()
