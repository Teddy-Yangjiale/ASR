#!/usr/bin/env python3
"""Check local prerequisites for the ASR comparison workflow."""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import sys
from pathlib import Path


PYTHON_PACKAGES = ["soundfile", "speechbrain", "torch", "torchaudio"]


def check_python_packages(required_speechbrain: bool) -> list[str]:
    issues = []
    packages = PYTHON_PACKAGES if required_speechbrain else ["soundfile"]
    for package in packages:
        if importlib.util.find_spec(package) is None:
            issues.append(f"missing Python package: {package}")
    return issues


def check_command(name: str, required: bool = True) -> list[str]:
    if shutil.which(name):
        return []
    level = "missing command" if required else "optional command not found"
    return [f"{level}: {name}"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--require-speechbrain", action="store_true")
    parser.add_argument("--require-kaldi", action="store_true")
    args = parser.parse_args()

    issues = []
    warnings = []
    issues.extend(check_python_packages(args.require_speechbrain))
    warnings.extend(check_command("flac", required=False))

    if args.require_kaldi:
        kaldi_root = os.environ.get("KALDI_ROOT")
        if not kaldi_root:
            issues.append("KALDI_ROOT is not set")
        elif not Path(kaldi_root).exists():
            issues.append(f"KALDI_ROOT does not exist: {kaldi_root}")

    if args.manifest and not args.manifest.exists():
        issues.append(f"manifest not found: {args.manifest}")

    print(f"Python: {sys.version.split()[0]}")
    print(f"Working directory: {Path.cwd()}")
    if args.manifest:
        print(f"Manifest: {args.manifest}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if issues:
        print("\nEnvironment check failed:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)

    print("\nEnvironment check passed.")


if __name__ == "__main__":
    main()
