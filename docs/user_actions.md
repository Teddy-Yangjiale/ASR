# User Actions

This project can prepare the pipeline, but several actions must happen on your machine because they require downloads, local packages, or long-running ASR inference.

## Required Before Real Experiments

Run from WSL Ubuntu:

```bash
cd ~/ASR
source .venv/bin/activate
```

Install Python dependencies:

```bash
make install-python-deps
```

Install the FLAC command-line decoder for Kaldi-compatible `wav.scp` entries:

```bash
sudo apt-get update
sudo apt-get install -y flac
```

Check the environment:

```bash
make env-check
```

## Required Data Download

Download the small LibriSpeech starter set:

```bash
make download-librispeech-small
```

This downloads and extracts:

- `dev-clean`
- `test-clean`

The data will live under:

```text
data/raw/LibriSpeech
```

These files are intentionally ignored by Git.

## First Real SpeechBrain Run

Build the manifest:

```bash
make librispeech-manifest
```

Run a small SpeechBrain test first:

```bash
LIMIT=20 make speechbrain-test
```

If that works, run the full test split:

```bash
make speechbrain-test
```

## What I Can Do After That

After you run the real-data commands, I can inspect:

- `data/manifests/librispeech_manifest.csv`
- `results/speechbrain/hypotheses.csv`
- `results/speechbrain/metrics.json`
- `results/speechbrain/runtime.json`

Then I can continue with the Kaldi baseline and the comparison report.
