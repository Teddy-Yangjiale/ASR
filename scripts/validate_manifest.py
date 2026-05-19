#!/usr/bin/env python3
"""Validate the shared ASR manifest before running toolkit-specific pipelines."""

from __future__ import annotations

import argparse
import csv
import sys
import wave
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = {"utt_id", "wav_path", "duration", "text", "split"}
SUPPORTED_SPLITS = {"train", "valid", "dev", "test"}


def validate_wav(path: Path, expected_sample_rate: int) -> list[str]:
    errors = []
    if not path.exists():
        return [f"missing wav: {path}"]
    try:
        with wave.open(str(path), "rb") as wav:
            if wav.getnchannels() != 1:
                errors.append(f"{path}: expected mono audio, got {wav.getnchannels()} channels")
            if wav.getframerate() != expected_sample_rate:
                errors.append(f"{path}: expected {expected_sample_rate} Hz, got {wav.getframerate()} Hz")
            if wav.getnframes() == 0:
                errors.append(f"{path}: empty wav file")
    except wave.Error as exc:
        errors.append(f"{path}: invalid wav file ({exc})")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--sample-rate", type=int, default=16000)
    args = parser.parse_args()

    errors = []
    split_counts: Counter[str] = Counter()
    seen_ids: set[str] = set()

    with args.manifest.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Manifest is missing columns: {sorted(missing)}")

        for line_no, row in enumerate(reader, start=2):
            utt_id = row["utt_id"].strip()
            wav_path = Path(row["wav_path"].strip())
            text = row["text"].strip()
            split = row["split"].strip()

            if not utt_id:
                errors.append(f"line {line_no}: empty utt_id")
            elif utt_id in seen_ids:
                errors.append(f"line {line_no}: duplicate utt_id {utt_id}")
            seen_ids.add(utt_id)

            if not text:
                errors.append(f"line {line_no}: empty transcript for {utt_id}")
            if split not in SUPPORTED_SPLITS:
                errors.append(f"line {line_no}: unsupported split '{split}' for {utt_id}")
            split_counts[split] += 1
            errors.extend(f"line {line_no}: {err}" for err in validate_wav(wav_path, args.sample_rate))

    if errors:
        print("Manifest validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Manifest OK: {len(seen_ids)} utterances")
    for split, count in sorted(split_counts.items()):
        print(f"- {split}: {count}")


if __name__ == "__main__":
    main()
