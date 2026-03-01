#!/usr/bin/env python3
"""Build script for PyTrainer — automates PyInstaller packaging.

Usage:
    python scripts/build.py [--clean]

Platform notes:
    Linux:   Produces dist/pytrainer/ directory with executable
    Windows: Produces dist/pytrainer/ — then use Inno Setup to create installer:
             1. python installer/windows/embed_python.py
             2. Compile installer/windows/pytrainer.iss with Inno Setup 6+
    macOS:   Produces .app bundle — then wrap with create-dmg

Prerequisites:
    pip install -e ".[dev]"   # installs pyinstaller
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPEC_FILE = PROJECT_ROOT / "pytrainer.spec"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"


def clean() -> None:
    """Remove previous build artifacts."""
    for d in (DIST_DIR, BUILD_DIR):
        if d.exists():
            shutil.rmtree(d)
            print(f"Removed {d}")


def build() -> int:
    """Run PyInstaller with the spec file. Returns exit code."""
    if not SPEC_FILE.exists():
        print(f"ERROR: Spec file not found: {SPEC_FILE}", file=sys.stderr)
        return 1

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(SPEC_FILE),
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
        "--noconfirm",
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return result.returncode


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PyTrainer executable")
    parser.add_argument(
        "--clean", action="store_true", help="Clean build artifacts before building"
    )
    args = parser.parse_args()

    if args.clean:
        clean()

    rc = build()
    if rc == 0:
        exe_dir = DIST_DIR / "pytrainer"
        print(f"\nBuild successful! Output: {exe_dir}")
    else:
        print("\nBuild FAILED.", file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()
