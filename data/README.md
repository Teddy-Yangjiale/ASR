# Data Directory

Raw audio and downloaded datasets are not committed.

Expected layout:

```text
data/
├── raw/
│   ├── wav/
│   │   └── utt0001.wav
│   └── transcripts.tsv
├── manifests/
│   └── asr_manifest.csv
└── kaldi/
    ├── train/
    ├── valid/
    └── test/
```

`transcripts.tsv` should contain at least:

```tsv
utt_id	text	split
utt0001	THE QUICK BROWN FOX	test
```

If audio filenames differ from `utt_id + ".wav"`, add a `wav_path` column.

