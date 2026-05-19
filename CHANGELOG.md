# Changelog

All notable project changes will be recorded in this file.

## 2026-05-19

### Added

- Added a `Makefile` with local smoke-test, validation, Kaldi export, scoring, comparison, and cleanup targets.
- Added `scripts/generate_toy_dataset.py` to create a tiny synthetic dataset for pipeline smoke tests.
- Added `scripts/validate_manifest.py` to check manifest schema, duplicate utterance ids, split names, audio existence, sample rate, channel count, and empty WAV files.
- Added optional evaluation normalization switches to `scripts/evaluate_wer.py`.

### Changed

- Updated `README.md` with the smoke-test workflow and ASCII-safe repository tree.
- Improved `scripts/prepare_manifest.py` to preserve optional speaker metadata and resolve relative `wav_path` values against the audio directory.
- Updated `.gitignore` to exclude generated toy smoke-test artifacts.

## 2026-05-19

### Added

- Initialized the SpeechBrain + Kaldi ASR comparison project.
- Added project documentation:
  - `README.md`
  - `docs/project_goals.md`
  - `docs/experiment_plan.md`
  - `docs/implementation_roadmap.md`
- Added shared configuration in `configs/project.yaml`.
- Added data, result, SpeechBrain, Kaldi, and environment directory notes.
- Added utility scripts:
  - `scripts/prepare_manifest.py`
  - `scripts/manifest_to_kaldi.py`
  - `scripts/run_speechbrain_infer.py`
  - `scripts/evaluate_wer.py`
  - `scripts/compare_metrics.py`
- Added a Kaldi recipe skeleton at `baselines/kaldi/egs/asr_compare/s5/run.sh`.
- Added `requirements.txt` for the Python/SpeechBrain baseline environment.
- Added `.gitignore` for virtual environments, generated caches, model files, raw data, and experiment outputs.
