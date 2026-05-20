#!/usr/bin/env python3
"""Directly download known SpeechBrain ASR model files over plain HTTP."""

from __future__ import annotations

import argparse
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_SOURCE = "speechbrain/asr-transformer-transformerlm-librispeech"
MODEL_FILES = [
    "hyperparams.yaml",
    "asr.ckpt",
    "lm.ckpt",
    "normalizer.ckpt",
    "tokenizer.ckpt",
    "config.json",
]


def file_url(endpoint: str, source: str, filename: str) -> str:
    return f"{endpoint.rstrip('/')}/{source}/resolve/main/{filename}"


def download_file(url: str, output: Path, timeout: float, force: bool) -> None:
    if output.exists() and output.stat().st_size > 0 and not force:
        print(f"Already exists, skipping: {output}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = output.with_suffix(output.suffix + ".part")
    request = urllib.request.Request(url)

    print(f"Downloading {url}")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            total = int(response.headers.get("Content-Length") or 0)
            downloaded = 0
            with temp_output.open("wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        percent = downloaded * 100 / total
                        print(f"\r  {downloaded / 1024 / 1024:.1f}/{total / 1024 / 1024:.1f} MB ({percent:.1f}%)", end="")
                    else:
                        print(f"\r  {downloaded / 1024 / 1024:.1f} MB", end="")
            print()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"failed to download {url}: {exc}") from exc

    temp_output.replace(output)
    print(f"Wrote {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--savedir", type=Path, default=Path("models/speechbrain_pretrained"))
    parser.add_argument("--endpoint", default=os.environ.get("HF_ENDPOINT", "https://huggingface.co"))
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    failures = []
    for filename in MODEL_FILES:
        try:
            download_file(
                file_url(args.endpoint, args.source, filename),
                args.savedir / filename,
                args.timeout,
                args.force,
            )
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            failures.append(filename)

    if failures:
        raise SystemExit(f"Failed to download: {', '.join(failures)}")

    print(f"SpeechBrain model files are available in {args.savedir}")


if __name__ == "__main__":
    main()
