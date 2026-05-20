#!/usr/bin/env python3
"""Download/cache a SpeechBrain pretrained ASR model without running inference."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="speechbrain/asr-transformer-transformerlm-librispeech")
    parser.add_argument("--savedir", default="models/speechbrain_pretrained")
    parser.add_argument("--timeout", type=int, default=60, help="Per-request Hugging Face timeout in seconds.")
    parser.add_argument("--local-files-only", action="store_true", help="Do not access the network.")
    args = parser.parse_args()

    os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", str(args.timeout))
    os.environ.setdefault("HF_HUB_ETAG_TIMEOUT", str(args.timeout))

    try:
        from huggingface_hub import snapshot_download

        snapshot_download(
            repo_id=args.source,
            local_dir=args.savedir,
            local_dir_use_symlinks=False,
            resume_download=True,
            local_files_only=args.local_files_only,
        )
    except Exception as exc:
        raise SystemExit(
            "Failed to cache SpeechBrain model. "
            "If the download stalls at `asr.ckpt: 0%`, Hugging Face large-file transfer is not working "
            "from this WSL environment. Run `make hf-check`, try a VPN/proxy, set `HF_ENDPOINT` to a "
            "reachable mirror, or manually download the repository files into "
            f"{Path(args.savedir)}. Original error: {type(exc).__name__}: {exc}"
        ) from exc

    print(f"SpeechBrain model cached in {args.savedir}")


if __name__ == "__main__":
    main()
