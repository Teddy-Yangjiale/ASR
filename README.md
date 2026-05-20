# SpeechBrain + Kaldi ASR Comparison

This repository builds a reproducible automatic speech recognition (ASR) comparison pipeline. It compares a modern end-to-end recognizer built with SpeechBrain against a traditional Kaldi-style ASR baseline, using the same dataset, the same transcript references, and the same WER/CER evaluation scripts.

## Project Goal

The goal is to move beyond generic audio analysis or audio classification and build a complete speech-to-text experiment workflow.

The project is designed to answer:

> Given the same speech data and scoring rules, how do SpeechBrain end-to-end ASR and Kaldi traditional ASR differ in accuracy, setup complexity, runtime behavior, and recognition errors?

The expected final outputs are:

- SpeechBrain hypotheses and metrics.
- Kaldi hypotheses and metrics.
- A shared WER/CER comparison.
- Runtime metadata where available.
- Representative recognition error examples.
- A report-ready Markdown summary.

## Tools Used

| Tool | Role in this project |
| --- | --- |
| SpeechBrain | Runs the end-to-end pretrained ASR baseline. |
| Kaldi | Provides the traditional ASR baseline path and data directory format. |
| LibriSpeech | Starter real-world English ASR dataset. |
| Hugging Face / hf-mirror | Source for SpeechBrain pretrained model files. |
| Python | Data preparation, manifest conversion, evaluation, and reporting scripts. |
| Make | One-command workflow entry points. |

## How It Works

The pipeline uses one shared manifest as the center of the experiment.

```text
LibriSpeech or custom audio
        |
        v
shared manifest CSV
        |
        |-- SpeechBrain inference --> results/speechbrain/hypotheses.csv
        |
        `-- Kaldi data export -----> data/kaldi/<split>/
                                      |
                                      `-- Kaldi decoding --> results/kaldi/hypotheses.csv

shared evaluator:
  hypotheses.csv + manifest.csv --> metrics.json
```

The shared manifest contains:

```csv
utt_id,wav_path,duration,text,split,speaker
```

Both ASR systems must use the same `test` split and the same reference text. This keeps the comparison fair.

## Repository Layout

```text
.
|-- baselines/
|   |-- kaldi/              # Kaldi baseline notes and recipe skeleton
|   `-- speechbrain/        # SpeechBrain baseline notes
|-- configs/                # Shared project configuration
|-- data/
|   |-- raw/                # Downloaded or original audio, ignored by Git
|   |-- manifests/          # Generated manifest CSV files
|   `-- kaldi/              # Generated Kaldi data directories
|-- docs/                   # Setup, runbook, dataset guide, and gap analysis
|-- models/                 # Downloaded SpeechBrain model cache, ignored by Git
|-- results/                # Hypotheses, metrics, runtime, reports, ignored by Git
|-- scripts/                # Data, inference, evaluation, and reporting utilities
|-- Makefile                # Main workflow commands
`-- requirements.txt        # Python dependencies
```

## Current Status

Implemented:

- Local toy smoke test.
- LibriSpeech `dev-clean` / `test-clean` download workflow.
- LibriSpeech manifest generation and validation.
- SpeechBrain pretrained model download helpers.
- SpeechBrain inference script with runtime metadata.
- Kaldi data directory export.
- Kaldi text hypothesis to CSV converter.
- Shared WER/CER evaluator.
- Markdown comparison report generator.

Still in progress:

- Full Kaldi training/decoding recipe.
- Final SpeechBrain vs Kaldi result table.
- Noise robustness experiment.

## Quick Start

Run commands from WSL Ubuntu:

```bash
cd ~/ASR
source .venv/bin/activate
```

Install Python dependencies:

```bash
make install-python-deps
```

Check the environment:

```bash
make env-check
```

Run the local smoke test. This does not require external data or pretrained models:

```bash
make smoke
```

## Real Data Workflow

Download the small LibriSpeech starter set:

```bash
make download-librispeech-small
```

Generate and validate the shared manifest:

```bash
make librispeech-manifest
```

This creates:

```text
data/manifests/librispeech_manifest.csv
```

## SpeechBrain Baseline

First check Hugging Face or mirror connectivity:

```bash
export HF_ENDPOINT=https://hf-mirror.com
make hf-check
```

Download the SpeechBrain model files directly:

```bash
make cache-speechbrain-model-direct
```

Validate the local checkpoint files:

```bash
make validate-speechbrain-model
```

Run a small 20-utterance SpeechBrain test from the local cache:

```bash
USE_LOCAL_CACHE=1 make speechbrain-smoke
```

Run the full LibriSpeech `test-clean` split after the smoke run works:

```bash
USE_LOCAL_CACHE=1 make speechbrain-test
```

SpeechBrain outputs:

```text
results/speechbrain/hypotheses.csv
results/speechbrain/metrics.json
results/speechbrain/runtime.json
```

## Kaldi Baseline

Export the shared manifest into Kaldi data directories:

```bash
python3 scripts/manifest_to_kaldi.py \
  --manifest data/manifests/librispeech_manifest.csv \
  --output-root data/kaldi/librispeech
```

Expected Kaldi files per split:

```text
wav.scp
text
utt2spk
spk2utt
```

If Kaldi decoding produces text output in this format:

```text
utt_id recognized words
```

convert it to the shared CSV format:

```bash
python3 scripts/kaldi_text_to_hypotheses.py \
  --input exp/decode_test/scoring_kaldi/test_filt.txt \
  --output results/kaldi/hypotheses.csv
```

Score Kaldi with the same evaluator:

```bash
python3 scripts/evaluate_wer.py \
  --refs data/manifests/librispeech_manifest.csv \
  --hyps results/kaldi/hypotheses.csv \
  --split test \
  --output results/kaldi/metrics.json
```

## Evaluation

The evaluator reports:

- WER: word error rate.
- CER: character error rate.
- missing or extra hypotheses.
- representative error examples.
- text normalization settings.

Example:

```bash
python3 scripts/evaluate_wer.py \
  --refs data/manifests/librispeech_manifest.csv \
  --hyps results/speechbrain/hypotheses.csv \
  --split test \
  --output results/speechbrain/metrics.json
```

Generate a Markdown comparison report after both systems have metrics:

```bash
make report
```

Output:

```text
results/comparison_report.md
```

## Common Issue: `asr.ckpt` Stalls or Is Corrupt

If model download stalls at `asr.ckpt: 0%`, use the direct downloader:

```bash
export HF_ENDPOINT=https://hf-mirror.com
make cache-speechbrain-model-direct
make validate-speechbrain-model
```

If validation says `asr.ckpt` is invalid, delete it and re-download:

```bash
rm models/speechbrain_pretrained/asr.ckpt
make cache-speechbrain-model-direct
make validate-speechbrain-model
```

Then run:

```bash
USE_LOCAL_CACHE=1 make speechbrain-smoke
```

## Useful Commands

```bash
make help
make smoke
make env-check
make download-librispeech-small
make librispeech-manifest
make cache-speechbrain-model-direct
make validate-speechbrain-model
USE_LOCAL_CACHE=1 make speechbrain-smoke
USE_LOCAL_CACHE=1 make speechbrain-test
make report
```

## Documentation

- `docs/setup.md`: environment setup.
- `docs/user_actions.md`: commands that require local downloads or system packages.
- `docs/dataset_guide.md`: dataset and manifest workflow.
- `docs/runbook.md`: end-to-end experiment order.
- `docs/gap_analysis.md`: current strengths, gaps, and done criteria.
- `docs/project_goals.md`: project positioning and deliverables.
