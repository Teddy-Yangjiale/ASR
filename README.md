# SpeechBrain + Kaldi ASR Comparison

This project compares a modern end-to-end ASR pipeline built with SpeechBrain against a traditional Kaldi ASR baseline on the same speech data.

## Project Goal

Build a non-overlapping follow-up to previous audio analysis/training work by focusing on a complete automatic speech recognition pipeline:

- data preparation for speech-to-text experiments
- transcription manifests and Kaldi data directories
- SpeechBrain inference/fine-tuning path
- Kaldi baseline path
- unified WER/CER evaluation
- error analysis across clean/noisy speech

## Research Question

How do traditional ASR and end-to-end ASR differ in recognition accuracy, setup complexity, inference behavior, and noise robustness on a small controlled dataset?

## Planned Comparison

| Track | Toolkit | Modeling style | Main output |
| --- | --- | --- | --- |
| SpeechBrain | SpeechBrain | end-to-end pretrained ASR or fine-tuning | hypotheses + WER/CER |
| Kaldi | Kaldi | feature extraction + acoustic model + decoding | hypotheses + WER/CER |

## Repository Layout

```text
.
|-- baselines/
|   |-- kaldi/              # Kaldi recipe notes and runnable skeleton
|   `-- speechbrain/        # SpeechBrain experiment notes
|-- configs/                # Shared experiment configuration
|-- data/
|   |-- raw/                # Original audio, not committed
|   |-- manifests/          # CSV/JSONL manifests
|   `-- kaldi/              # Generated Kaldi data dirs
|-- docs/                   # Project goals, experiment plan, report notes
|-- results/                # Metrics, hypotheses, logs
`-- scripts/                # Shared preparation and evaluation utilities
```

## First Milestone

1. Choose a small dataset: LibriSpeech dev-clean subset, Common Voice subset, or self-recorded command/short-sentence data.
2. Normalize all audio to 16 kHz mono WAV.
3. Create one shared manifest with `utt_id`, `wav_path`, `duration`, `text`, and `split`.
4. Run SpeechBrain pretrained ASR as the first working recognizer.
5. Prepare equivalent Kaldi data directories.
6. Evaluate both tracks with the same WER/CER script.

## Quick Start

Create a Python environment and install the lightweight utilities:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the local smoke test without downloading any dataset:

```bash
make smoke
```

This generates a tiny synthetic dataset, builds the shared manifest, exports Kaldi data directories, creates sample hypotheses, and computes WER/CER. It verifies the project wiring before connecting real SpeechBrain/Kaldi experiments.

For a real LibriSpeech-style dataset, create and validate a manifest:

```bash
make librispeech-manifest
```

See `docs/dataset_guide.md` and `docs/runbook.md` for the full experiment flow.

Create a manifest from a transcript file:

```bash
python scripts/prepare_manifest.py \
  --audio-dir data/raw/wav \
  --transcripts data/raw/transcripts.tsv \
  --output data/manifests/asr_manifest.csv
```

Evaluate recognition output:

```bash
python scripts/evaluate_wer.py \
  --refs data/manifests/asr_manifest.csv \
  --hyps results/speechbrain/hypotheses.csv \
  --output results/speechbrain/metrics.json
```

## Status

Executable scaffold with local smoke-test utilities and LibriSpeech manifest support. The next implementation step is running the SpeechBrain baseline on a real test split and exporting the Kaldi baseline hypotheses.
