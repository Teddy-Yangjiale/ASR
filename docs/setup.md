# Setup Guide

## Python Environment

Use a virtual environment from the repository root:

```bash
cd ~/ASR
python3 -m venv .venv
source .venv/bin/activate
make install-python-deps
```

Check the environment:

```bash
make env-check
```

## System Dependencies

LibriSpeech audio is distributed as FLAC. Python can inspect FLAC through `soundfile`, but Kaldi `wav.scp` entries use the `flac` command-line decoder.

On Ubuntu/WSL:

```bash
sudo apt-get update
sudo apt-get install -y flac
```

## Minimal Validation

Before downloading real data:

```bash
make smoke
```

Before running SpeechBrain on LibriSpeech:

```bash
make env-check
make hf-check
make download-librispeech-small
make librispeech-manifest
make speechbrain-smoke
```

See `docs/user_actions.md` for the exact commands that require local downloads or system package installation.

## Notes

- `make env-check` requires `soundfile`, `speechbrain`, `torch`, and `torchaudio`.
- `make hf-check` confirms the SpeechBrain model metadata is reachable before inference starts.
- If `asr.ckpt` stalls at 0%, cache the model with `make cache-speechbrain-model-direct`; use `HF_ENDPOINT=https://hf-mirror.com` if Hugging Face is unreachable from WSL.
- `flac` is marked as a warning because SpeechBrain can still run without Kaldi, but Kaldi FLAC decoding needs it.
- Kaldi itself is not installed by this repository. Set `KALDI_ROOT` before running Kaldi-specific recipe work.
