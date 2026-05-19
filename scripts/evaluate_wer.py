#!/usr/bin/env python3
"""Evaluate ASR hypotheses with WER and CER."""

from __future__ import annotations

import argparse
import csv
import json
import re
import string
from pathlib import Path


def normalize(text: str, lowercase: bool = True, remove_punctuation: bool = True) -> str:
    if lowercase:
        text = text.lower()
    if remove_punctuation:
        text = text.translate(str.maketrans("", "", string.punctuation))
    return re.sub(r"\s+", " ", text).strip()


def edit_distance(ref: list[str], hyp: list[str]) -> int:
    prev = list(range(len(hyp) + 1))
    for i, ref_token in enumerate(ref, start=1):
        curr = [i]
        for j, hyp_token in enumerate(hyp, start=1):
            cost = 0 if ref_token == hyp_token else 1
            curr.append(min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost))
        prev = curr
    return prev[-1]


def load_refs(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return {row["utt_id"]: row["text"] for row in csv.DictReader(f)}


def load_hyps(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        hyp_col = "hyp_text" if "hyp_text" in (reader.fieldnames or []) else "text"
        return {row["utt_id"]: row[hyp_col] for row in reader}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refs", required=True, type=Path)
    parser.add_argument("--hyps", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    refs = load_refs(args.refs)
    hyps = load_hyps(args.hyps)
    common_ids = sorted(set(refs) & set(hyps))
    if not common_ids:
        raise ValueError("No matching utt_id values between references and hypotheses.")

    word_edits = 0
    ref_words = 0
    char_edits = 0
    ref_chars = 0
    examples = []

    for utt_id in common_ids:
        ref = normalize(refs[utt_id])
        hyp = normalize(hyps[utt_id])
        ref_word_tokens = ref.split()
        hyp_word_tokens = hyp.split()
        word_edits += edit_distance(ref_word_tokens, hyp_word_tokens)
        ref_words += len(ref_word_tokens)
        char_edits += edit_distance(list(ref), list(hyp))
        ref_chars += len(ref)
        if ref != hyp and len(examples) < 10:
            examples.append({"utt_id": utt_id, "ref": ref, "hyp": hyp})

    metrics = {
        "utterances_scored": len(common_ids),
        "missing_hypotheses": sorted(set(refs) - set(hyps)),
        "extra_hypotheses": sorted(set(hyps) - set(refs)),
        "wer": word_edits / ref_words if ref_words else 0.0,
        "cer": char_edits / ref_chars if ref_chars else 0.0,
        "error_examples": examples,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

