# Project Goals

## Positioning

This project is designed as a step beyond audio analysis and generic audio model training. The core contribution is a complete ASR comparison workflow, not another audio classification or visualization project.

## Main Objectives

1. Build one shared speech-to-text dataset format.
2. Implement a SpeechBrain end-to-end ASR track.
3. Implement a Kaldi traditional ASR baseline track.
4. Evaluate both systems with identical metrics.
5. Analyze recognition errors and noise robustness.

## What This Project Should Demonstrate

- Understanding of ASR-specific data preparation.
- Ability to use a pretrained end-to-end ASR model.
- Ability to prepare Kaldi-style data directories.
- Fair comparison through shared test splits and shared scoring.
- Practical evaluation with WER, CER, speed, and error examples.

## What This Project Should Avoid

- Repeating simple audio classification.
- Only plotting audio features.
- Only calling one pretrained model without evaluation.
- Comparing tools on different datasets or different text normalization.

## Target Deliverables

- Reproducible project repository.
- Dataset manifest and Kaldi data directory generator.
- SpeechBrain inference or fine-tuning script.
- Kaldi recipe skeleton with documented setup.
- Unified evaluation outputs in `results/`.
- Final report section comparing accuracy, complexity, and robustness.

