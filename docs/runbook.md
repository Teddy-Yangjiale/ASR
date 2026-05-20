# Experiment Runbook

This runbook defines the intended command order for a real experiment.

Commands that require local downloads or system packages are also summarized in `docs/user_actions.md`.

## 1. Sanity Check the Local Pipeline

```bash
make install-python-deps
make env-check
make hf-check
make cache-speechbrain-model-direct
make smoke
```

This does not test ASR accuracy. It verifies the local data, Kaldi export, and scoring utilities.

## 2. Download a Small Real Dataset

For the first real run, download LibriSpeech `dev-clean` and `test-clean`:

```bash
make download-librispeech-small
```

This extracts data under `data/raw/LibriSpeech`.

## 3. Build a Real Manifest

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

Or use the Makefile target:

```bash
make librispeech-manifest
```

## 4. Run SpeechBrain Baseline

```bash
python3 scripts/run_speechbrain_infer.py \
  --manifest data/manifests/librispeech_manifest.csv \
  --split test \
  --limit 20 \
  --output results/speechbrain/hypotheses.csv \
  --metadata-output results/speechbrain/runtime.json
```

Score:

```bash
python3 scripts/evaluate_wer.py \
  --refs data/manifests/librispeech_manifest.csv \
  --hyps results/speechbrain/hypotheses.csv \
  --split test \
  --output results/speechbrain/metrics.json
```

Or use:

```bash
make speechbrain-smoke
```

Run the full test split after the small run is working:

```bash
make speechbrain-test
```

If the model has already been cached and you want to avoid any Hugging Face access during inference:

```bash
USE_LOCAL_CACHE=1 make speechbrain-smoke
```

## 5. Prepare Kaldi Inputs

```bash
python3 scripts/manifest_to_kaldi.py \
  --manifest data/manifests/librispeech_manifest.csv \
  --output-root data/kaldi/librispeech
```

The Kaldi recipe should read from `data/kaldi/librispeech/test` for the same test split.

## 6. Compare Metrics

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

## 7. Report Minimum Content

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
