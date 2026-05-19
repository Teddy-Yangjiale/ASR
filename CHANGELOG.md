# Changelog

All notable project changes will be recorded in this file.

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

