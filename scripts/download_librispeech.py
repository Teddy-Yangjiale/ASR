#!/usr/bin/env python3
"""Download selected LibriSpeech archives from OpenSLR."""

from __future__ import annotations

import argparse
import tarfile
import urllib.request
from pathlib import Path


BASE_URL = "https://www.openslr.org/resources/12"
KNOWN_SPLITS = {
    "dev-clean": "dev-clean.tar.gz",
    "test-clean": "test-clean.tar.gz",
    "train-clean-100": "train-clean-100.tar.gz",
}


def download(url: str, output: Path, force: bool) -> None:
    if output.exists() and not force:
        print(f"Archive already exists, skipping: {output}")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, output)
    print(f"Wrote {output}")


def safe_members(tar: tarfile.TarFile, output_root: Path) -> list[tarfile.TarInfo]:
    output_root = output_root.resolve()
    members = []
    for member in tar.getmembers():
        target = (output_root / member.name).resolve()
        if not str(target).startswith(str(output_root)):
            raise RuntimeError(f"Refusing to extract path outside output root: {member.name}")
        members.append(member)
    return members


def extract(archive: Path, output_root: Path) -> None:
    print(f"Extracting {archive} to {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(output_root, members=safe_members(tar, output_root))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download-root", type=Path, default=Path("downloads/librispeech"))
    parser.add_argument("--extract-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--split", action="append", choices=sorted(KNOWN_SPLITS), default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-extract", action="store_true")
    args = parser.parse_args()

    splits = args.split or ["dev-clean", "test-clean"]
    for split in splits:
        filename = KNOWN_SPLITS[split]
        archive = args.download_root / filename
        download(f"{BASE_URL}/{filename}", archive, args.force)
        if not args.no_extract:
            extract(archive, args.extract_root)

    print("Done.")
    print(f"Expected LibriSpeech root: {args.extract_root / 'LibriSpeech'}")


if __name__ == "__main__":
    main()
