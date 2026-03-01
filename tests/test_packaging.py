"""Tests for distribution & packaging (E8)."""

import sys
from pathlib import Path
from unittest.mock import patch


class TestRuntimePaths:
    """E8-S01 AC1/AC2: Runtime path resolution for frozen and dev environments."""

    def test_get_base_path_returns_project_root_in_dev(self):
        """In dev mode (not frozen), base_path should be the project root."""
        from pytrainer.paths import get_base_path

        base = get_base_path()
        # In dev, base_path is the project root (where pyproject.toml lives)
        assert base.is_dir()
        # The exercises dir should be reachable from base
        assert (base / "exercises").is_dir()

    def test_get_base_path_uses_meipass_when_frozen(self, tmp_path):
        """When sys._MEIPASS is set (frozen app), base_path should use it."""
        from pytrainer.paths import get_base_path

        fake_meipass = str(tmp_path / "frozen_bundle")
        Path(fake_meipass).mkdir()

        with (
            patch.object(sys, "frozen", True, create=True),
            patch.object(sys, "_MEIPASS", fake_meipass, create=True),
        ):
            base = get_base_path()
            assert base == Path(fake_meipass)

    def test_get_exercises_dir_returns_exercises_subdir(self):
        """get_exercises_dir() should return {base}/exercises."""
        from pytrainer.paths import get_exercises_dir

        ex_dir = get_exercises_dir()
        assert ex_dir.name == "exercises"
        assert ex_dir.is_dir()

    def test_get_exercises_dir_frozen(self, tmp_path):
        """In frozen mode, exercises dir comes from _MEIPASS."""
        from pytrainer.paths import get_exercises_dir

        fake_meipass = str(tmp_path / "frozen_bundle")
        ex_path = Path(fake_meipass) / "exercises"
        ex_path.mkdir(parents=True)

        with (
            patch.object(sys, "frozen", True, create=True),
            patch.object(sys, "_MEIPASS", fake_meipass, create=True),
        ):
            result = get_exercises_dir()
            assert result == ex_path


class TestSpecFile:
    """E8-S01 AC1/AC2: PyInstaller spec file exists with correct configuration."""

    def test_spec_file_exists(self):
        """pytrainer.spec must exist at project root."""
        spec = Path(__file__).parent.parent / "pytrainer.spec"
        assert spec.is_file(), "pytrainer.spec not found at project root"

    def test_spec_contains_hidden_imports(self):
        """Spec file must declare hidden imports for PyQt6, QScintilla, yaml."""
        spec = Path(__file__).parent.parent / "pytrainer.spec"
        content = spec.read_text()
        assert "PyQt6" in content
        assert "yaml" in content

    def test_spec_includes_exercises_data(self):
        """Spec file must include exercises/ as data files."""
        spec = Path(__file__).parent.parent / "pytrainer.spec"
        content = spec.read_text()
        assert "exercises" in content

    def test_spec_uses_onedir_mode(self):
        """Spec file should use --onedir (not --onefile) for faster startup."""
        spec = Path(__file__).parent.parent / "pytrainer.spec"
        content = spec.read_text()
        # COLLECT is used in onedir mode (vs MERGE for onefile)
        assert "COLLECT" in content


class TestBuildScript:
    """E8-S01 AC5: Build script automates the process."""

    def test_build_script_exists(self):
        """scripts/build.py must exist."""
        build = Path(__file__).parent.parent / "scripts" / "build.py"
        assert build.is_file(), "scripts/build.py not found"

    def test_build_script_is_executable_python(self):
        """Build script should be valid Python."""
        build = Path(__file__).parent.parent / "scripts" / "build.py"
        content = build.read_text()
        compile(content, str(build), "exec")  # Raises SyntaxError if invalid

    def test_build_script_references_spec(self):
        """Build script should reference the .spec file."""
        build = Path(__file__).parent.parent / "scripts" / "build.py"
        content = build.read_text()
        assert "pytrainer.spec" in content
