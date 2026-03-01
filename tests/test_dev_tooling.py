"""Tests for E1-S02: Configure Developer Tooling."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


class TestRuff:
    """AC: ruff check/format passes cleanly."""

    def test_ruff_check_passes(self):
        """AC: ruff check . passes with zero warnings on the scaffold."""
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "."],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=30,
        )
        assert result.returncode == 0, f"ruff check failed:\n{result.stdout}\n{result.stderr}"

    def test_ruff_format_no_changes(self):
        """AC: ruff format . produces no changes."""
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "format", "--check", "."],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=30,
        )
        assert result.returncode == 0, f"ruff format would change:\n{result.stdout}"


class TestPytest:
    """AC: pytest runs and discovers test directory."""

    def test_pytest_discovers_tests(self):
        """AC: pytest runs and discovers test directory."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=30,
        )
        assert result.returncode == 0, f"pytest collection failed:\n{result.stderr}"
        assert "test" in result.stdout.lower() or "selected" in result.stdout.lower()


class TestGitignore:
    """AC: .gitignore covers Python/Qt artifacts."""

    def test_gitignore_exists(self):
        assert (ROOT / ".gitignore").is_file()

    def test_gitignore_covers_pycache(self):
        content = (ROOT / ".gitignore").read_text()
        assert "__pycache__" in content

    def test_gitignore_covers_venv(self):
        content = (ROOT / ".gitignore").read_text()
        assert ".venv" in content

    def test_gitignore_covers_pyc(self):
        content = (ROOT / ".gitignore").read_text()
        assert "*.pyc" in content or "*.py[cod" in content

    def test_gitignore_covers_dist(self):
        content = (ROOT / ".gitignore").read_text()
        assert "dist/" in content

    def test_gitignore_covers_build(self):
        content = (ROOT / ".gitignore").read_text()
        assert "build/" in content

    def test_gitignore_covers_egg_info(self):
        content = (ROOT / ".gitignore").read_text()
        assert "*.egg-info" in content

    def test_gitignore_covers_pytest_cache(self):
        content = (ROOT / ".gitignore").read_text()
        assert ".pytest_cache" in content

    def test_gitignore_covers_ruff_cache(self):
        content = (ROOT / ".gitignore").read_text()
        assert ".ruff_cache" in content


class TestReadme:
    """AC: README.md with project description and dev setup."""

    def test_readme_exists(self):
        assert (ROOT / "README.md").is_file()

    def test_readme_has_project_name(self):
        content = (ROOT / "README.md").read_text()
        assert "PyTrainer" in content or "pytrainer" in content.lower()

    def test_readme_has_dev_setup(self):
        content = (ROOT / "README.md").read_text()
        assert "pip install" in content or "uv" in content
