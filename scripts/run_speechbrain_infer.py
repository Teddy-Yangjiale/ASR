#!/usr/bin/env python3
"""Run pretrained SpeechBrain ASR on a manifest split."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--split", default="test")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source", default="speechbrain/asr-transformer-transformerlm-librispeech")
    parser.add_argument("--savedir", default="models/speechbrain_pretrained")
    args = parser.parse_args()

    from speechbrain.inference.ASR import EncoderDecoderASR

    asr_model = EncoderDecoderASR.from_hparams(source=args.source, savedir=args.savedir)

    rows = []
    with args.manifest.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["split"] != args.split:
                continue
            hyp = asr_model.transcribe_file(row["wav_path"])
            rows.append({"utt_id": row["utt_id"], "hyp_text": hyp})
            print(f"{row['utt_id']}\t{hyp}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["utt_id", "hyp_text"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} hypotheses to {args.output}")


if __name__ == "__main__":
    main()

