#!/usr/bin/env python3
"""Create the shared ASR manifest from a LibriSpeech-style directory."""

from __future__ import annotations

import argparse
import csv
import wave
from pathlib import Path


DEFAULT_SPLITS = [
    "train-clean-100:train",
    "dev-clean:valid",
    "test-clean:test",
]


def audio_duration(path: Path) -> float:
    if path.suffix.lower() == ".wav":
        with wave.open(str(path), "rb") as wav:
            return wav.getnframes() / float(wav.getframerate())

    try:
        import soundfile as sf
    except ImportError as exc:
        raise RuntimeError(f"Install soundfile to read duration for {path}") from exc

    info = sf.info(str(path))
    return info.frames / float(info.samplerate)


def parse_split_mapping(values: list[str]) -> list[tuple[str, str]]:
    mappings = []
    for value in values:
        if ":" not in value:
            raise ValueError(f"Split mapping must use source:target format: {value}")
        source, target = value.split(":", 1)
        mappings.append((source.strip(), target.strip()))
    return mappings


def find_audio_file(transcript_path: Path, utt_id: str) -> Path:
    for suffix in (".flac", ".wav"):
        candidate = transcript_path.parent / f"{utt_id}{suffix}"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Missing audio file for {utt_id} next to {transcript_path}")


def read_transcript_file(path: Path, split: str) -> list[dict[str, str]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                utt_id, text = line.split(" ", 1)
            except ValueError as exc:
                raise ValueError(f"{path}:{line_no}: expected '<utt_id> <text>'") from exc
            audio_path = find_audio_file(path, utt_id)
            speaker = utt_id.split("-")[0]
            rows.append(
                {
                    "utt_id": utt_id,
                    "wav_path": str(audio_path),
                    "duration": f"{audio_duration(audio_path):.3f}",
                    "text": text.strip(),
                    "split": split,
                    "speaker": speaker,
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Path containing LibriSpeech split directories.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--split",
        action="append",
        dest="splits",
        default=None,
        help="Split mapping in source:target form, for example dev-clean:valid. Can be repeated.",
    )
    args = parser.parse_args()

    split_mappings = parse_split_mapping(args.splits or DEFAULT_SPLITS)
    rows = []

    for source_split, target_split in split_mappings:
        split_dir = args.root / source_split
        if not split_dir.exists():
            raise FileNotFoundError(f"Missing LibriSpeech split directory: {split_dir}")
        transcript_files = sorted(split_dir.rglob("*.trans.txt"))
        if not transcript_files:
            raise FileNotFoundError(f"No *.trans.txt files found under {split_dir}")
        for transcript_file in transcript_files:
            rows.extend(read_transcript_file(transcript_file, target_split))

    rows.sort(key=lambda row: (row["split"], row["utt_id"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["utt_id", "wav_path", "duration", "text", "split", "speaker"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} LibriSpeech utterances to {args.output}")


if __name__ == "__main__":
    main()
