# SpeechBrain Track

Goal: build the end-to-end ASR side of the comparison.

Initial baseline:

1. Load a pretrained SpeechBrain ASR model.
2. Run inference on the shared `test` split.
3. Save `results/speechbrain/hypotheses.csv`.
4. Score with `scripts/evaluate_wer.py`.

Recommended first model:

```text
speechbrain/asr-transformer-transformerlm-librispeech
```

This baseline is intentionally inference-first. Fine-tuning should be added only after the shared evaluation path is working.

