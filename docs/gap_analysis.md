# Gap Analysis

## Current Goal

The project goal is to build a fair ASR comparison between:

- SpeechBrain end-to-end pretrained or fine-tuned ASR.
- Kaldi traditional ASR baseline.

The comparison must use the same dataset split, the same reference transcripts, the same text normalization rules, and the same WER/CER scoring code.

## Current Strengths

- The repository has a clear project structure.
- A local smoke test verifies manifest generation, Kaldi data export, and scoring.
- LibriSpeech-style data can be converted into the shared manifest.
- The same manifest can feed both SpeechBrain and Kaldi paths.
- A small LibriSpeech download target and SpeechBrain test target now reduce the manual setup needed for the first real run.

## Main Gaps

1. Real ASR results are not committed or reproduced yet.
   The SpeechBrain command path exists, but it still needs to be run on a downloaded real test split.

2. Kaldi decoding is still a skeleton.
   Kaldi data directories can be generated, but the recipe does not yet train or decode.

3. Experiment scoring needs split isolation.
   Scoring should normally evaluate only the `test` split to avoid counting train/valid utterances as missing hypotheses.

4. Kaldi output needs a standard conversion step.
   Kaldi text output must be converted to the shared `utt_id,hyp_text` CSV format before scoring.

5. Runtime comparison is limited.
   SpeechBrain records per-utterance decode time, but Kaldi runtime metadata still needs to be captured later.

6. Dependency management is now documented but still local-machine dependent.
   Python packages can be installed with `make install-python-deps`; FLAC and Kaldi still depend on system setup.

## Implementation Order

1. Keep the local smoke test passing after every change.
2. Run `make install-python-deps` and `make env-check`.
3. Build or download a small LibriSpeech-compatible dataset subset.
4. Run SpeechBrain inference on the test split.
5. Export Kaldi data directories from the same manifest.
6. Implement Kaldi decode and convert output to shared CSV.
7. Score both systems with the same evaluator.
8. Generate a final comparison table and qualitative error examples.

## Definition of Done

The project is complete when the repository can produce:

- `results/speechbrain/hypotheses.csv`
- `results/speechbrain/metrics.json`
- `results/kaldi/hypotheses.csv`
- `results/kaldi/metrics.json`
- a report-ready comparison table
- representative error examples from both systems
