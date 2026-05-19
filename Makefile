.PHONY: help smoke validate kaldi-data score compare clean-generated

MANIFEST := data/manifests/toy_manifest.csv
TOY_HYPS := results/toy/hypotheses.csv
TOY_METRICS := results/toy/metrics.json

help:
	@echo "Available targets:"
	@echo "  make smoke          Generate toy data and run the full local utility pipeline"
	@echo "  make validate       Validate $(MANIFEST)"
	@echo "  make kaldi-data     Convert $(MANIFEST) into Kaldi data directories"
	@echo "  make score          Score toy hypotheses with WER/CER"
	@echo "  make clean-generated Remove generated toy artifacts"

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
		--output $(TOY_METRICS)

validate:
	python3 scripts/validate_manifest.py --manifest $(MANIFEST)

kaldi-data:
	python3 scripts/manifest_to_kaldi.py --manifest $(MANIFEST) --output-root data/kaldi/toy

score:
	python3 scripts/evaluate_wer.py --refs $(MANIFEST) --hyps $(TOY_HYPS) --output $(TOY_METRICS)

compare:
	python3 scripts/compare_metrics.py \
		--speechbrain results/speechbrain/metrics.json \
		--kaldi results/kaldi/metrics.json

clean-generated:
	rm -rf data/raw/toy_wav data/raw/toy_transcripts.tsv data/manifests/toy_manifest.csv data/kaldi/toy results/toy
