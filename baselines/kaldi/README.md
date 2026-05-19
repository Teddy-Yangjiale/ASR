# Kaldi Track

Goal: build the traditional ASR side of the comparison.

Initial baseline:

1. Convert the shared manifest into Kaldi data directories.
2. Use Kaldi feature extraction and decoding.
3. Export decoded hypotheses to `results/kaldi/hypotheses.csv`.
4. Score with `scripts/evaluate_wer.py`.

Kaldi expects `KALDI_ROOT` to point to a working Kaldi checkout.

```bash
export KALDI_ROOT=/path/to/kaldi
```

The recipe skeleton is under:

```text
baselines/kaldi/egs/asr_compare/s5
```

