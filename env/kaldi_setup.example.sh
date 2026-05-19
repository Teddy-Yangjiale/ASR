#!/usr/bin/env bash
set -euo pipefail

# Edit this path after installing or locating Kaldi.
export KALDI_ROOT="${KALDI_ROOT:-/path/to/kaldi}"

if [[ ! -d "$KALDI_ROOT" ]]; then
  echo "KALDI_ROOT does not exist: $KALDI_ROOT" >&2
  return 1 2>/dev/null || exit 1
fi

export PATH="$KALDI_ROOT/src/bin:$KALDI_ROOT/tools/openfst/bin:$PATH"
echo "KALDI_ROOT=$KALDI_ROOT"

