"""Runtime path resolution for both development and frozen (PyInstaller) environments."""

import sys
from pathlib import Path


def get_base_path() -> Path:
    """Return the application base path.

    In a frozen PyInstaller bundle, this is ``sys._MEIPASS``.
    In development, this is the project root (two levels up from this file).
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    # Development: src/pytrainer/paths.py -> src/pytrainer -> src -> project root
    return Path(__file__).resolve().parent.parent.parent


def get_exercises_dir() -> Path:
    """Return the path to the exercises directory."""
    return get_base_path() / "exercises"
