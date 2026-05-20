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

Check whether WSL can reach Hugging Face for the SpeechBrain model:

```bash
make hf-check
```

If this fails with a network error, fix WSL networking/proxy/VPN first or set `HF_ENDPOINT` to a reachable Hugging Face mirror.

If model download stalls at `asr.ckpt: 0%`, stop it with `Ctrl+C` and try:

```bash
export HF_ENDPOINT=https://hf-mirror.com
make hf-check
make cache-speechbrain-model-direct
```

After the model is cached, run inference from the local cache:

```bash
USE_LOCAL_CACHE=1 make speechbrain-smoke
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
make speechbrain-smoke
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

## Your Current Log

Your `make librispeech-manifest` run succeeded and produced 5323 utterances, so LibriSpeech is already usable. The earlier `make download-librispeech-small` failure happened while re-extracting files that were already present. The downloader now skips already extracted splits unless `--force` is used.

Your SpeechBrain run failed because Hugging Face was unreachable from WSL. Run:

```bash
make hf-check
```

before running SpeechBrain again.
