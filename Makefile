.PHONY: help install-python-deps env-check smoke validate kaldi-data score compare report download-librispeech-small librispeech-manifest speechbrain-test clean-generated

MANIFEST := data/manifests/toy_manifest.csv
TOY_HYPS := results/toy/hypotheses.csv
TOY_METRICS := results/toy/metrics.json
LIBRISPEECH_ROOT := data/raw/LibriSpeech
LIBRISPEECH_MANIFEST := data/manifests/librispeech_manifest.csv

help:
	@echo "Available targets:"
	@echo "  make install-python-deps Install Python dependencies from requirements.txt"
	@echo "  make env-check      Check local Python and optional ASR dependencies"
	@echo "  make smoke          Generate toy data and run the full local utility pipeline"
	@echo "  make validate       Validate $(MANIFEST)"
	@echo "  make kaldi-data     Convert $(MANIFEST) into Kaldi data directories"
	@echo "  make score          Score toy hypotheses with WER/CER"
	@echo "  make compare        Compare SpeechBrain and Kaldi metrics"
	@echo "  make report         Build a Markdown comparison report"
	@echo "  make download-librispeech-small Download dev-clean and test-clean"
	@echo "  make librispeech-manifest Build a LibriSpeech manifest from $(LIBRISPEECH_ROOT)"
	@echo "  make speechbrain-test Run SpeechBrain on the LibriSpeech test split"
	@echo "  make clean-generated Remove generated toy artifacts"

env-check:
	python3 scripts/check_environment.py --require-speechbrain

install-python-deps:
	python3 -m pip install -r requirements.txt

smoke: clean-generated
	python3 scripts/generate_toy_dataset.py \
		--audio-dir data/raw/toy_wav \
		--transcripts data/raw/toy_transcripts.tsv \
		--hypotheses $(TOY_HYPS)
	python3 scripts/prepare_manifest.py \
		--audio-dir data/raw/toy_wav \
		--transcripts data/raw/toy_transcripts.tsv \
		--output $(MANIFEST)
	python3 scripts/validate_manifest.py --manifest $(MANIFEST)
	python3 scripts/manifest_to_kaldi.py \
		--manifest $(MANIFEST) \
		--output-root data/kaldi/toy
	python3 scripts/evaluate_wer.py \
		--refs $(MANIFEST) \
		--hyps $(TOY_HYPS) \
		--split test \
		--output $(TOY_METRICS)

validate:
	python3 scripts/validate_manifest.py --manifest $(MANIFEST)

kaldi-data:
	python3 scripts/manifest_to_kaldi.py --manifest $(MANIFEST) --output-root data/kaldi/toy

score:
	python3 scripts/evaluate_wer.py --refs $(MANIFEST) --hyps $(TOY_HYPS) --split test --output $(TOY_METRICS)

compare:
	python3 scripts/compare_metrics.py \
		--speechbrain results/speechbrain/metrics.json \
		--kaldi results/kaldi/metrics.json

report:
	python3 scripts/build_comparison_report.py \
		--speechbrain-metrics results/speechbrain/metrics.json \
		--kaldi-metrics results/kaldi/metrics.json \
		--speechbrain-runtime results/speechbrain/runtime.json \
		--output results/comparison_report.md

download-librispeech-small:
	python3 scripts/download_librispeech.py \
		--split dev-clean \
		--split test-clean

librispeech-manifest:
	python3 scripts/prepare_librispeech_manifest.py \
		--root $(LIBRISPEECH_ROOT) \
		--split dev-clean:valid \
		--split test-clean:test \
		--output $(LIBRISPEECH_MANIFEST)
	python3 scripts/validate_manifest.py --manifest $(LIBRISPEECH_MANIFEST)

speechbrain-test:
	python3 scripts/check_environment.py \
		--manifest $(LIBRISPEECH_MANIFEST) \
		--require-speechbrain
	python3 scripts/run_speechbrain_infer.py \
		--manifest $(LIBRISPEECH_MANIFEST) \
		--split test \
		--limit $${LIMIT:-20} \
		--output results/speechbrain/hypotheses.csv \
		--metadata-output results/speechbrain/runtime.json
	python3 scripts/evaluate_wer.py \
		--refs $(LIBRISPEECH_MANIFEST) \
		--hyps results/speechbrain/hypotheses.csv \
		--split test \
		--output results/speechbrain/metrics.json

clean-generated:
	rm -rf data/raw/toy_wav data/raw/toy_transcripts.tsv data/manifests/toy_manifest.csv data/kaldi/toy results/toy
