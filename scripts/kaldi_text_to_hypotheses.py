#!/usr/bin/env python3
"""Convert Kaldi text-format hypotheses into the shared hypotheses CSV format."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_kaldi_text(path: Path) -> list[dict[str, str]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=1)
            if len(parts) == 1:
                utt_id, hyp_text = parts[0], ""
            else:
                utt_id, hyp_text = parts
            if not utt_id:
                raise ValueError(f"{path}:{line_no}: empty utterance id")
            rows.append({"utt_id": utt_id, "hyp_text": hyp_text})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Kaldi text output: '<utt_id> <hypothesis>'.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows = parse_kaldi_text(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["utt_id", "hyp_text"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} Kaldi hypotheses to {args.output}")


if __name__ == "__main__":
    main()
