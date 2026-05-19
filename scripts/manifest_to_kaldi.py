#!/usr/bin/env python3
"""Convert the shared ASR manifest to Kaldi data directories."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def kaldi_wav_command(path: str) -> str:
    audio_path = Path(path)
    suffix = audio_path.suffix.lower()
    if suffix == ".flac":
        return f"flac -c -d -s {audio_path} |"
    return str(audio_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    by_split: dict[str, list[dict[str, str]]] = defaultdict(list)
    with args.manifest.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            by_split[row["split"]].append(row)

    for split, rows in by_split.items():
        out_dir = args.output_root / split
        out_dir.mkdir(parents=True, exist_ok=True)

        wav_scp = []
        text = []
        utt2spk = []
        speakers: dict[str, list[str]] = defaultdict(list)

        for row in sorted(rows, key=lambda r: r["utt_id"]):
            utt_id = row["utt_id"]
            speaker = row.get("speaker") or utt_id.split("-")[0] or "spk1"
            wav_scp.append(f"{utt_id} {kaldi_wav_command(row['wav_path'])}\n")
            text.append(f"{utt_id} {row['text']}\n")
            utt2spk.append(f"{utt_id} {speaker}\n")
            speakers[speaker].append(utt_id)

        (out_dir / "wav.scp").write_text("".join(wav_scp), encoding="utf-8")
        (out_dir / "text").write_text("".join(text), encoding="utf-8")
        (out_dir / "utt2spk").write_text("".join(utt2spk), encoding="utf-8")
        (out_dir / "spk2utt").write_text(
            "".join(f"{spk} {' '.join(utts)}\n" for spk, utts in sorted(speakers.items())),
            encoding="utf-8",
        )
        print(f"Wrote Kaldi data dir for split '{split}' with {len(rows)} utterances: {out_dir}")


if __name__ == "__main__":
    main()
