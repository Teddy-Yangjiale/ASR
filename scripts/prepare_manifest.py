#!/usr/bin/env python3
"""Create a shared ASR manifest from transcript metadata."""

from __future__ import annotations

import argparse
import csv
import wave
from pathlib import Path


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def read_transcripts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters="\t,")
        reader = csv.DictReader(f, dialect=dialect)
        rows = list(reader)

    required = {"utt_id", "text", "split"}
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"Transcript file is missing columns: {sorted(missing)}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-dir", required=True, type=Path)
    parser.add_argument("--transcripts", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows = []
    for item in read_transcripts(args.transcripts):
        utt_id = item["utt_id"].strip()
        text = item["text"].strip()
        split = item["split"].strip()
        wav_path = Path(item.get("wav_path") or args.audio_dir / f"{utt_id}.wav")
        if not wav_path.is_absolute():
            wav_path = wav_path
        if not wav_path.exists():
            raise FileNotFoundError(f"Missing audio for {utt_id}: {wav_path}")
        rows.append(
            {
                "utt_id": utt_id,
                "wav_path": str(wav_path),
                "duration": f"{wav_duration(wav_path):.3f}",
                "text": text,
                "split": split,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["utt_id", "wav_path", "duration", "text", "split"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} utterances to {args.output}")


if __name__ == "__main__":
    main()

