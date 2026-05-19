#!/usr/bin/env python3
"""Create a shared ASR manifest from transcript metadata."""

from __future__ import annotations

import argparse
import csv
import wave
from pathlib import Path


def audio_duration(path: Path) -> float:
    if path.suffix.lower() == ".wav":
        with wave.open(str(path), "rb") as wav:
            return wav.getnframes() / float(wav.getframerate())

    try:
        import soundfile as sf
    except ImportError as exc:
        raise RuntimeError(f"Install soundfile to read duration for non-WAV audio: {path}") from exc

    info = sf.info(str(path))
    return info.frames / float(info.samplerate)


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


def resolve_wav_path(item: dict[str, str], audio_dir: Path, utt_id: str) -> Path:
    raw_path = item.get("wav_path", "").strip()
    if raw_path:
        wav_path = Path(raw_path)
        return wav_path if wav_path.is_absolute() else audio_dir / wav_path
    return audio_dir / f"{utt_id}.wav"


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
        wav_path = resolve_wav_path(item, args.audio_dir, utt_id)
        if not wav_path.exists():
            raise FileNotFoundError(f"Missing audio for {utt_id}: {wav_path}")
        output_row = {
                "utt_id": utt_id,
                "wav_path": str(wav_path),
                "duration": f"{audio_duration(wav_path):.3f}",
                "text": text,
                "split": split,
            }
        if item.get("speaker"):
            output_row["speaker"] = item["speaker"].strip()
        rows.append(output_row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["utt_id", "wav_path", "duration", "text", "split"]
    if any("speaker" in row for row in rows):
        fieldnames.append("speaker")
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} utterances to {args.output}")


if __name__ == "__main__":
    main()
