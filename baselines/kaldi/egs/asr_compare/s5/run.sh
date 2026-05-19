#!/usr/bin/env bash
set -euo pipefail

stage=0
stop_stage=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stage) stage="$2"; shift 2 ;;
    --stop-stage) stop_stage="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "${KALDI_ROOT:-}" ]]; then
  echo "KALDI_ROOT is not set. Export KALDI_ROOT before running this recipe." >&2
  exit 1
fi

echo "Kaldi recipe skeleton."
echo "stage=${stage}, stop_stage=${stop_stage}"
echo "Next implementation: source Kaldi path.sh/cmd.sh, validate data dirs, extract MFCC, train/decode baseline."

