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

## Main Gaps

1. Real ASR results are not produced yet.
   The SpeechBrain script exists, but it still needs to run on a real test split and save results.

2. Kaldi decoding is still a skeleton.
   Kaldi data directories can be generated, but the recipe does not yet train or decode.

3. Experiment scoring needs split isolation.
   Scoring should normally evaluate only the `test` split to avoid counting train/valid utterances as missing hypotheses.

4. Kaldi output needs a standard conversion step.
   Kaldi text output must be converted to the shared `utt_id,hyp_text` CSV format before scoring.

5. Runtime comparison is limited.
   SpeechBrain now records per-utterance decode time, but Kaldi runtime metadata still needs to be captured later.

## Implementation Order

1. Keep the local smoke test passing after every change.
2. Build or download a small LibriSpeech-compatible dataset subset.
3. Run SpeechBrain inference on the test split.
4. Export Kaldi data directories from the same manifest.
5. Implement Kaldi decode and convert output to shared CSV.
6. Score both systems with the same evaluator.
7. Generate a final comparison table and qualitative error examples.

## Definition of Done

The project is complete when the repository can produce:

- `results/speechbrain/hypotheses.csv`
- `results/speechbrain/metrics.json`
- `results/kaldi/hypotheses.csv`
- `results/kaldi/metrics.json`
- a report-ready comparison table
- representative error examples from both systems
