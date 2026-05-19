#!/usr/bin/env python3
"""Run pretrained SpeechBrain ASR on a manifest split."""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--split", default="test")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source", default="speechbrain/asr-transformer-transformerlm-librispeech")
    parser.add_argument("--savedir", default="models/speechbrain_pretrained")
    parser.add_argument("--limit", type=int, default=None, help="Optional utterance limit for smoke runs.")
    parser.add_argument("--metadata-output", type=Path, default=None, help="Optional JSON runtime metadata output.")
    args = parser.parse_args()

    from speechbrain.inference.ASR import EncoderDecoderASR

    asr_model = EncoderDecoderASR.from_hparams(source=args.source, savedir=args.savedir)

    rows = []
    total_audio_seconds = 0.0
    started_at = time.perf_counter()
    with args.manifest.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["split"] != args.split:
                continue
            if args.limit is not None and len(rows) >= args.limit:
                break
            item_started_at = time.perf_counter()
            hyp = asr_model.transcribe_file(row["wav_path"])
            elapsed = time.perf_counter() - item_started_at
            duration = float(row.get("duration") or 0.0)
            total_audio_seconds += duration
            rows.append({"utt_id": row["utt_id"], "hyp_text": hyp, "decode_seconds": f"{elapsed:.3f}"})
            print(f"{row['utt_id']}\t{hyp}\tdecode_seconds={elapsed:.3f}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["utt_id", "hyp_text", "decode_seconds"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} hypotheses to {args.output}")

    if args.metadata_output:
        total_decode_seconds = time.perf_counter() - started_at
        metadata = {
            "source": args.source,
            "split": args.split,
            "utterances": len(rows),
            "audio_seconds": total_audio_seconds,
            "decode_seconds": total_decode_seconds,
            "rtf": total_decode_seconds / total_audio_seconds if total_audio_seconds else None,
        }
        args.metadata_output.parent.mkdir(parents=True, exist_ok=True)
        args.metadata_output.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        print(f"Wrote runtime metadata to {args.metadata_output}")


if __name__ == "__main__":
    main()
