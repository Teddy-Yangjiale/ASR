#!/usr/bin/env python3
"""Print a compact comparison table from ASR metric JSON files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--speechbrain", required=True, type=Path)
    parser.add_argument("--kaldi", required=True, type=Path)
    args = parser.parse_args()

    rows = [
        ("SpeechBrain", load(args.speechbrain)),
        ("Kaldi", load(args.kaldi)),
    ]
    print("| System | Utterances | WER | CER |")
    print("| --- | ---: | ---: | ---: |")
    for name, metrics in rows:
        print(
            f"| {name} | {metrics.get('utterances_scored', 0)} | "
            f"{metrics.get('wer', 0.0):.4f} | {metrics.get('cer', 0.0):.4f} |"
        )


if __name__ == "__main__":
    main()

