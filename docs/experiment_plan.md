# Experiment Plan

## Phase 1: Dataset

Candidate datasets:

- LibriSpeech small subset: best for English ASR compatibility.
- Mozilla Common Voice subset: more speaker variation, more cleanup.
- Self-recorded command/short-sentence dataset: best for controlled scope.

Initial recommendation: use a small LibriSpeech or Common Voice English subset first, then optionally add self-recorded audio for domain shift testing.

## Phase 2: Shared Manifest

Use one canonical CSV manifest:

```csv
utt_id,wav_path,duration,text,split
utt0001,data/raw/wav/utt0001.wav,2.31,THE QUICK BROWN FOX,test
```

The same manifest must feed both SpeechBrain and Kaldi conversion.

## Phase 3: SpeechBrain Track

Baseline:

- run pretrained SpeechBrain ASR
- save one hypothesis per utterance
- compute WER/CER

Extension:

- fine-tune on `train`
- validate on `valid`
- evaluate on `test`

## Phase 4: Kaldi Track

Baseline:

- generate Kaldi `wav.scp`, `text`, `utt2spk`, `spk2utt`
- build a small recipe under `baselines/kaldi/egs/asr_compare/s5`
- decode the same `test` split
- export hypotheses to the shared CSV format

Extension:

- compare MFCC-based traditional decoding with the SpeechBrain model
- add noise conditions and re-score

## Phase 5: Evaluation

Core metrics:

- WER: word error rate
- CER: character error rate
- decoding time / real-time factor
- setup complexity notes

Error analysis:

- substitutions
- deletions
- insertions
- examples under clean speech
- examples under noisy speech

