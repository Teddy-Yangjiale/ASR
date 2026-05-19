#!/usr/bin/env python3
"""Generate a tiny synthetic dataset for local pipeline smoke tests."""

from __future__ import annotations

import argparse
import csv
import math
import wave
from pathlib import Path


SAMPLE_RATE = 16000
UTTERANCES = [
    ("spk1-utt001", "HELLO WORLD", "train", 440.0),
    ("spk1-utt002", "SPEECH RECOGNITION TEST", "valid", 554.37),
    ("spk2-utt003", "KALDI AND SPEECHBRAIN", "test", 659.25),
]


def write_tone(path: Path, frequency: float, seconds: float = 0.35) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    total = int(SAMPLE_RATE * seconds)
    amplitude = 12000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for idx in range(total):
            sample = int(amplitude * math.sin(2 * math.pi * frequency * idx / SAMPLE_RATE))
            frames.extend(sample.to_bytes(2, byteorder="little", signed=True))
        wav.writeframes(frames)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-dir", required=True, type=Path)
    parser.add_argument("--transcripts", required=True, type=Path)
    parser.add_argument("--hypotheses", required=True, type=Path)
    args = parser.parse_args()

    args.audio_dir.mkdir(parents=True, exist_ok=True)
    args.transcripts.parent.mkdir(parents=True, exist_ok=True)
    args.hypotheses.parent.mkdir(parents=True, exist_ok=True)

    with args.transcripts.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["utt_id", "speaker", "text", "split"], delimiter="\t")
        writer.writeheader()
        for utt_id, text, split, frequency in UTTERANCES:
            write_tone(args.audio_dir / f"{utt_id}.wav", frequency)
            writer.writerow({"utt_id": utt_id, "speaker": utt_id.split("-")[0], "text": text, "split": split})

    with args.hypotheses.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["utt_id", "hyp_text"])
        writer.writeheader()
        writer.writerow({"utt_id": "spk2-utt003", "hyp_text": "KALDI SPEECHBRAIN"})

    print(f"Wrote toy audio to {args.audio_dir}")
    print(f"Wrote transcripts to {args.transcripts}")
    print(f"Wrote sample hypotheses to {args.hypotheses}")


if __name__ == "__main__":
    main()
