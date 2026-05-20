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


def remote_content_length(url: str, timeout: float) -> int:
    request = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return int(response.headers.get("Content-Length") or 0)


def should_skip_existing(url: str, output: Path, timeout: float, force: bool) -> bool:
    if force or not output.exists() or output.stat().st_size <= 0:
        return False

    local_size = output.stat().st_size
    try:
        remote_size = remote_content_length(url, timeout)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"Cannot verify remote size for {output}; keeping existing file. Reason: {exc}")
        return True

    if remote_size and local_size != remote_size:
        print(
            f"Existing file size mismatch, re-downloading: {output} "
            f"local={local_size} remote={remote_size}"
        )
        return False

    print(f"Already exists and size matches, skipping: {output}")
    return True


def download_file(url: str, output: Path, timeout: float, force: bool, retries: int) -> None:
    if should_skip_existing(url, output, timeout, force):
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = output.with_suffix(output.suffix + ".part")
    request = urllib.request.Request(url)

    for attempt in range(1, retries + 1):
        print(f"Downloading {url} (attempt {attempt}/{retries})")
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
                            print(
                                f"\r  {downloaded / 1024 / 1024:.1f}/"
                                f"{total / 1024 / 1024:.1f} MB ({percent:.1f}%)",
                                end="",
                            )
                        else:
                            print(f"\r  {downloaded / 1024 / 1024:.1f} MB", end="")
                print()
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == retries:
                raise RuntimeError(f"failed to download {url}: {exc}") from exc
            print(f"Download attempt failed: {exc}")
            continue

        if total and downloaded != total:
            message = f"incomplete download for {url}: downloaded={downloaded} expected={total}"
            if attempt == retries:
                raise RuntimeError(message)
            print(message)
            continue

        temp_output.replace(output)
        print(f"Wrote {output}")
        return

    raise RuntimeError(f"failed to download {url}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--savedir", type=Path, default=Path("models/speechbrain_pretrained"))
    parser.add_argument("--endpoint", default=os.environ.get("HF_ENDPOINT", "https://huggingface.co"))
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--retries", type=int, default=3)
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
                args.retries,
            )
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            failures.append(filename)

    if failures:
        raise SystemExit(f"Failed to download: {', '.join(failures)}")

    print(f"SpeechBrain model files are available in {args.savedir}")


if __name__ == "__main__":
    main()
