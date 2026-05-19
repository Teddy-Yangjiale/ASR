# Experiment Runbook

This runbook defines the intended command order for a real experiment.

## 1. Sanity Check the Local Pipeline

```bash
make smoke
```

This does not test ASR accuracy. It verifies the local data, Kaldi export, and scoring utilities.

## 2. Build a Real Manifest

For LibriSpeech:

```bash
python3 scripts/prepare_librispeech_manifest.py \
  --root data/raw/LibriSpeech \
  --split dev-clean:valid \
  --split test-clean:test \
  --output data/manifests/librispeech_manifest.csv
```

Validate:

```bash
python3 scripts/validate_manifest.py \
  --manifest data/manifests/librispeech_manifest.csv
```

## 3. Run SpeechBrain Baseline

```bash
python3 scripts/run_speechbrain_infer.py \
  --manifest data/manifests/librispeech_manifest.csv \
  --split test \
  --output results/speechbrain/hypotheses.csv
```

Score:

```bash
python3 scripts/evaluate_wer.py \
  --refs data/manifests/librispeech_manifest.csv \
  --hyps results/speechbrain/hypotheses.csv \
  --split test \
  --output results/speechbrain/metrics.json
```

## 4. Prepare Kaldi Inputs

```bash
python3 scripts/manifest_to_kaldi.py \
  --manifest data/manifests/librispeech_manifest.csv \
  --output-root data/kaldi/librispeech
```

The Kaldi recipe should read from `data/kaldi/librispeech/test` for the same test split.

## 5. Compare Metrics

After Kaldi decoding exports `results/kaldi/hypotheses.csv` and scoring creates `results/kaldi/metrics.json`:

```bash
python3 scripts/compare_metrics.py \
  --speechbrain results/speechbrain/metrics.json \
  --kaldi results/kaldi/metrics.json
```

If Kaldi produces plain text hypotheses in `<utt_id> <hypothesis>` format, convert them first:

```bash
python3 scripts/kaldi_text_to_hypotheses.py \
  --input exp/decode_test/scoring_kaldi/test_filt.txt \
  --output results/kaldi/hypotheses.csv
```

## 6. Report Minimum Content

The report should include:

- dataset and split sizes
- SpeechBrain WER/CER
- Kaldi WER/CER
- setup/runtime notes
- at least five representative error cases
- explanation of where the systems differ

Generate a Markdown report draft after both systems have metrics:

```bash
make report
```
