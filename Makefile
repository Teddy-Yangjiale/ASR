.PHONY: help install-python-deps env-check hf-check cache-speechbrain-model cache-speechbrain-model-direct validate-speechbrain-model smoke validate kaldi-data score compare report download-librispeech-small librispeech-manifest speechbrain-smoke speechbrain-test clean-generated

MANIFEST := data/manifests/toy_manifest.csv
TOY_HYPS := results/toy/hypotheses.csv
TOY_METRICS := results/toy/metrics.json
LIBRISPEECH_ROOT := data/raw/LibriSpeech
LIBRISPEECH_MANIFEST := data/manifests/librispeech_manifest.csv

help:
	@echo "Available targets:"
	@echo "  make install-python-deps Install Python dependencies from requirements.txt"
	@echo "  make env-check      Check local Python and optional ASR dependencies"
	@echo "  make hf-check       Check Hugging Face connectivity for the SpeechBrain model"
	@echo "  make cache-speechbrain-model Download/cache the SpeechBrain pretrained model"
	@echo "  make cache-speechbrain-model-direct Direct HTTP fallback for SpeechBrain model files"
	@echo "  make validate-speechbrain-model Validate local SpeechBrain checkpoint files"
	@echo "  make smoke          Generate toy data and run the full local utility pipeline"
	@echo "  make validate       Validate $(MANIFEST)"
	@echo "  make kaldi-data     Convert $(MANIFEST) into Kaldi data directories"
	@echo "  make score          Score toy hypotheses with WER/CER"
	@echo "  make compare        Compare SpeechBrain and Kaldi metrics"
	@echo "  make report         Build a Markdown comparison report"
	@echo "  make download-librispeech-small Download dev-clean and test-clean"
	@echo "  make librispeech-manifest Build a LibriSpeech manifest from $(LIBRISPEECH_ROOT)"
	@echo "  make speechbrain-smoke Run SpeechBrain on LIMIT test utterances, default LIMIT=20"
	@echo "  make speechbrain-test Run SpeechBrain on the full LibriSpeech test split"
	@echo "  make clean-generated Remove generated toy artifacts"

env-check:
	python3 scripts/check_environment.py --require-speechbrain

install-python-deps:
	python3 -m pip install -r requirements.txt

hf-check:
	python3 scripts/check_huggingface.py

cache-speechbrain-model:
	python3 scripts/cache_speechbrain_model.py

cache-speechbrain-model-local-check:
	python3 scripts/cache_speechbrain_model.py --local-files-only

cache-speechbrain-model-direct:
	python3 scripts/direct_download_speechbrain_model.py

validate-speechbrain-model:
	python3 scripts/validate_speechbrain_model.py

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

speechbrain-smoke:
	python3 scripts/check_environment.py \
		--manifest $(LIBRISPEECH_MANIFEST) \
		--require-speechbrain
	if [ -z "$${USE_LOCAL_CACHE:-}" ]; then python3 scripts/check_huggingface.py; fi
	python3 scripts/run_speechbrain_infer.py \
		--manifest $(LIBRISPEECH_MANIFEST) \
		--split test \
		--limit $${LIMIT:-20} \
		$${USE_LOCAL_CACHE:+--use-local-cache} \
		--output results/speechbrain/hypotheses.csv \
		--metadata-output results/speechbrain/runtime.json
	python3 scripts/evaluate_wer.py \
		--refs $(LIBRISPEECH_MANIFEST) \
		--hyps results/speechbrain/hypotheses.csv \
		--split test \
		--output results/speechbrain/metrics.json

speechbrain-test:
	python3 scripts/check_environment.py \
		--manifest $(LIBRISPEECH_MANIFEST) \
		--require-speechbrain
	python3 scripts/run_speechbrain_infer.py \
		--manifest $(LIBRISPEECH_MANIFEST) \
		--split test \
		$${USE_LOCAL_CACHE:+--use-local-cache} \
		--output results/speechbrain/hypotheses.csv \
		--metadata-output results/speechbrain/runtime.json
	python3 scripts/evaluate_wer.py \
		--refs $(LIBRISPEECH_MANIFEST) \
		--hyps results/speechbrain/hypotheses.csv \
		--split test \
		--output results/speechbrain/metrics.json

clean-generated:
	rm -rf data/raw/toy_wav data/raw/toy_transcripts.tsv data/manifests/toy_manifest.csv data/kaldi/toy results/toy
