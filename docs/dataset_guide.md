# Dataset Guide

## Recommended First Dataset

Use a small LibriSpeech subset first. It is a good first target because:

- SpeechBrain has LibriSpeech-compatible pretrained ASR models.
- Kaldi has mature LibriSpeech recipes and assumptions.
- Transcripts and speaker ids are already structured.
- Audio is clean enough for debugging the comparison pipeline.

Recommended split mapping:

| LibriSpeech split | Project split |
| --- | --- |
| `train-clean-100` | `train` |
| `dev-clean` | `valid` |
| `test-clean` | `test` |

For a faster first pass, use only:

| LibriSpeech split | Project split |
| --- | --- |
| `dev-clean` | `valid` |
| `test-clean` | `test` |

## Manifest Creation

If the dataset is already in LibriSpeech format:

```bash
python3 scripts/prepare_librispeech_manifest.py \
  --root data/raw/LibriSpeech \
  --split dev-clean:valid \
  --split test-clean:test \
  --output data/manifests/librispeech_manifest.csv
```

Then validate it:

```bash
python3 scripts/validate_manifest.py \
  --manifest data/manifests/librispeech_manifest.csv
```

## Kaldi Data Export

Convert the same manifest into Kaldi data directories:

```bash
python3 scripts/manifest_to_kaldi.py \
  --manifest data/manifests/librispeech_manifest.csv \
  --output-root data/kaldi/librispeech
```

This creates project splits such as:

```text
data/kaldi/librispeech/valid
data/kaldi/librispeech/test
```

## SpeechBrain Inference

Run pretrained SpeechBrain ASR on the test split:

```bash
python3 scripts/run_speechbrain_infer.py \
  --manifest data/manifests/librispeech_manifest.csv \
  --split test \
  --output results/speechbrain/hypotheses.csv
```

Then score it:

```bash
python3 scripts/evaluate_wer.py \
  --refs data/manifests/librispeech_manifest.csv \
  --hyps results/speechbrain/hypotheses.csv \
  --output results/speechbrain/metrics.json
```

## Dataset Rule

Both toolchains must use the same manifest and the same test split. Do not compare SpeechBrain and Kaldi results from different subsets, transcript normalization rules, or filtering decisions.
