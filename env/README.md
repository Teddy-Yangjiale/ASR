# Environment Notes

## Python / SpeechBrain

Use a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

SpeechBrain inference may download pretrained models into `models/`.

## Kaldi

Kaldi is normally installed outside this repository. After installation, set:

```bash
export KALDI_ROOT=/path/to/kaldi
```

You can copy or source `env/kaldi_setup.example.sh` after editing the path.

