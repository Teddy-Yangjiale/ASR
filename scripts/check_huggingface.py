#!/usr/bin/env python3
"""Check whether the SpeechBrain model metadata is reachable on Hugging Face."""

from __future__ import annotations

import argparse
import os
import urllib.error
import urllib.request


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="speechbrain/asr-transformer-transformerlm-librispeech")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    endpoint = os.environ.get("HF_ENDPOINT", "https://huggingface.co").rstrip("/")
    url = f"{endpoint}/{args.source}/resolve/main/hyperparams.yaml"
    request = urllib.request.Request(url, method="HEAD")

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            print(f"Hugging Face reachable: {url}")
            print(f"HTTP status: {response.status}")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Hugging Face returned HTTP {exc.code}: {url}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(
            "Cannot reach Hugging Face model metadata. "
            "Check WSL networking, proxy/VPN settings, or set HF_ENDPOINT to a reachable mirror. "
            f"URL: {url}. Error: {exc.reason}"
        ) from exc


if __name__ == "__main__":
    main()
