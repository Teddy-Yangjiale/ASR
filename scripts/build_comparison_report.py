#!/usr/bin/env python3
"""Build a report-ready Markdown summary from ASR comparison outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def metric_row(system: str, metrics: dict[str, Any], runtime: dict[str, Any]) -> str:
    utterances = metrics.get("utterances_scored", 0)
    wer = metrics.get("wer")
    cer = metrics.get("cer")
    rtf = runtime.get("rtf")
    wer_text = f"{wer:.4f}" if isinstance(wer, (int, float)) else "N/A"
    cer_text = f"{cer:.4f}" if isinstance(cer, (int, float)) else "N/A"
    rtf_text = f"{rtf:.4f}" if isinstance(rtf, (int, float)) else "N/A"
    return f"| {system} | {utterances} | {wer_text} | {cer_text} | {rtf_text} |"


def format_errors(system: str, metrics: dict[str, Any]) -> list[str]:
    lines = [f"## {system} Error Examples", ""]
    examples = metrics.get("error_examples") or []
    if not examples:
        lines.append("No error examples recorded.")
        return lines

    for item in examples[:10]:
        lines.extend(
            [
                f"- `{item.get('utt_id', 'unknown')}`",
                f"  - REF: {item.get('ref', '')}",
                f"  - HYP: {item.get('hyp', '')}",
            ]
        )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--speechbrain-metrics", required=True, type=Path)
    parser.add_argument("--kaldi-metrics", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--speechbrain-runtime", type=Path, default=None)
    parser.add_argument("--kaldi-runtime", type=Path, default=None)
    args = parser.parse_args()

    speechbrain_metrics = load_json(args.speechbrain_metrics)
    kaldi_metrics = load_json(args.kaldi_metrics)
    speechbrain_runtime = load_json(args.speechbrain_runtime)
    kaldi_runtime = load_json(args.kaldi_runtime)

    lines = [
        "# ASR Comparison Report",
        "",
        "## Summary",
        "",
        "| System | Utterances | WER | CER | RTF |",
        "| --- | ---: | ---: | ---: | ---: |",
        metric_row("SpeechBrain", speechbrain_metrics, speechbrain_runtime),
        metric_row("Kaldi", kaldi_metrics, kaldi_runtime),
        "",
        "## Notes",
        "",
        "- Both systems must be scored against the same manifest split.",
        "- WER/CER values are only comparable when text normalization settings match.",
        "- RTF is optional until each pipeline exports runtime metadata.",
        "",
    ]
    lines.extend(format_errors("SpeechBrain", speechbrain_metrics))
    lines.append("")
    lines.extend(format_errors("Kaldi", kaldi_metrics))
    lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote comparison report to {args.output}")


if __name__ == "__main__":
    main()
