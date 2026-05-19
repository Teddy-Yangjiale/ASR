# Implementation Roadmap

## Target Outcome

The final project should answer one concrete question:

> Given the same speech dataset and scoring rules, how does a SpeechBrain end-to-end recognizer compare with a Kaldi traditional ASR baseline?

The target implementation is not just a demo. It should produce comparable artifacts:

- `results/speechbrain/hypotheses.csv`
- `results/speechbrain/metrics.json`
- `results/kaldi/hypotheses.csv`
- `results/kaldi/metrics.json`
- a short analysis table comparing accuracy, runtime, setup complexity, and typical errors

## Milestone 1: Shared Dataset Layer

Deliverables:

- `data/raw/wav/*.wav`
- `data/raw/transcripts.tsv`
- `data/manifests/asr_manifest.csv`

Acceptance criteria:

- every utterance has an id, audio path, transcript, duration, and split
- all audio is 16 kHz mono WAV
- `scripts/prepare_manifest.py` succeeds

## Milestone 2: Shared Evaluation Layer

Deliverables:

- `scripts/evaluate_wer.py`
- one sample `hypotheses.csv`
- one `metrics.json`

Acceptance criteria:

- WER and CER are computed from the same reference manifest
- missing and extra hypotheses are reported
- error examples are saved for qualitative analysis

## Milestone 3: SpeechBrain Baseline

Deliverables:

- pretrained ASR inference over the test split
- `results/speechbrain/hypotheses.csv`
- `results/speechbrain/metrics.json`

Acceptance criteria:

- the script runs on the shared manifest
- output format matches the shared evaluator
- no manual transcript copying is needed

## Milestone 4: Kaldi Data Preparation

Deliverables:

- `data/kaldi/train`
- `data/kaldi/valid`
- `data/kaldi/test`

Acceptance criteria:

- each split has `wav.scp`, `text`, `utt2spk`, and `spk2utt`
- Kaldi validation scripts can check the directories once Kaldi is installed

## Milestone 5: Kaldi Baseline

Deliverables:

- runnable Kaldi recipe under `baselines/kaldi/egs/asr_compare/s5`
- decoded test hypotheses
- `results/kaldi/metrics.json`

Acceptance criteria:

- Kaldi decodes the same test split as SpeechBrain
- decoded text is exported to `utt_id,hyp_text` CSV
- scoring uses the same `scripts/evaluate_wer.py`

## Milestone 6: Comparison Report

Deliverables:

- final result table
- error examples
- conclusion on tradeoffs

Recommended comparison dimensions:

- WER
- CER
- inference time
- setup complexity
- robustness under optional noise augmentation
- representative substitution/deletion/insertion errors

