#!/usr/bin/env python3
"""Download and configure the Windows embeddable Python package.

Downloads the Python 3.12 embeddable zip from python.org and extracts it
to installer/windows/python-embed/ for inclusion in the installer.

Usage:
    python installer/windows/embed_python.py

The embeddable package provides a minimal Python runtime (~15 MB) that
the installer bundles so users don't need system Python for code execution.
Targets Python 3.12 (compatible with 3.10+ exercise requirements).
"""

import io
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen

# Python 3.12 embeddable package for Windows (amd64)
PYTHON_VERSION = "3.12.8"
EMBED_URL = (
    f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"
)

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "python-embed"


def download_and_extract() -> None:
    """Download the embeddable Python zip and extract to python-embed/."""
    if OUTPUT_DIR.exists():
        print(f"python-embed/ already exists at {OUTPUT_DIR}")
        print("Delete it first if you want to re-download.")
        sys.exit(0)

    print(f"Downloading Python {PYTHON_VERSION} embeddable package...")
    print(f"URL: {EMBED_URL}")

    response = urlopen(EMBED_URL)  # noqa: S310
    data = response.read()
    print(f"Downloaded {len(data) / 1024 / 1024:.1f} MB")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(OUTPUT_DIR)

    # Enable pip-installed packages by uncommenting import site in ._pth
    pth_files = list(OUTPUT_DIR.glob("python*._pth"))
    for pth in pth_files:
        content = pth.read_text()
        content = content.replace("#import site", "import site")
        pth.write_text(content)

    print(f"Extracted to {OUTPUT_DIR}")
    print(f"Files: {len(list(OUTPUT_DIR.iterdir()))}")


if __name__ == "__main__":
    download_and_extract()
