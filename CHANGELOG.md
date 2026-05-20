# Changelog

All notable project changes will be recorded in this file.

## 2026-05-20

### Added

- Added `scripts/check_huggingface.py` and `make hf-check` to diagnose Hugging Face connectivity before SpeechBrain inference.
- Added `scripts/cache_speechbrain_model.py` and `make cache-speechbrain-model` to pre-cache the SpeechBrain pretrained model.
- Added `scripts/check_environment.py` and `make env-check` for dependency checks before real experiments.
- Added `scripts/download_librispeech.py` and `make download-librispeech-small` for downloading LibriSpeech `dev-clean` and `test-clean`.
- Added `make speechbrain-test` to run SpeechBrain inference and scoring on the LibriSpeech test split.
- Added `make install-python-deps` and `docs/setup.md` for reproducible local dependency setup.
- Added `docs/user_actions.md` to separate user-required downloads, package installs, and long-running commands from repository automation.
- Added `docs/gap_analysis.md` to clarify project goals, current gaps, implementation order, and done criteria.
- Added `scripts/build_comparison_report.py` and `make report` to generate a report-ready Markdown summary from SpeechBrain and Kaldi metrics.
- Added `scripts/kaldi_text_to_hypotheses.py` to convert Kaldi text-format decoding output into the shared hypotheses CSV format.
- Added optional runtime metadata and utterance limiting to `scripts/run_speechbrain_infer.py`.

### Changed

- Split SpeechBrain execution into `make speechbrain-smoke` for limited test runs and `make speechbrain-test` for the full test split.
- Updated `scripts/download_librispeech.py` to skip already extracted LibriSpeech splits unless forced.
- Improved SpeechBrain model load errors with actionable Hugging Face/cache troubleshooting guidance.
- Updated `scripts/evaluate_wer.py` to support split-specific scoring and report reference/hypothesis counts.
- Updated `scripts/manifest_to_kaldi.py` to emit FLAC decode pipes in `wav.scp`, which is safer for LibriSpeech-style Kaldi inputs.
- Updated README, runbook, and Makefile scoring commands to score only the intended `test` split.
- Updated `.gitignore` to exclude generated comparison result artifacts.
- Updated runbook and gap analysis with the real-data download and SpeechBrain baseline flow.
- Documented the required Python packages and Ubuntu `flac` package for LibriSpeech/Kaldi work.
- Hardened LibriSpeech archive extraction to reject tar members that escape the target extraction directory.

## 2026-05-19

### Added

- Added `scripts/prepare_librispeech_manifest.py` for LibriSpeech-style datasets.
- Added `docs/dataset_guide.md` with the recommended dataset path and manifest workflow.
- Added `docs/runbook.md` with the intended end-to-end experiment command order.
- Added `make librispeech-manifest` to generate and validate a LibriSpeech manifest.

### Changed

- Extended manifest preparation and validation to handle FLAC or WAV audio through `soundfile`.
- Updated `README.md` to point to the LibriSpeech workflow.
- Updated `.gitignore` to exclude generated LibriSpeech manifests.

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
