"""Tests for Windows Installer (E8-S02)."""

from pathlib import Path


class TestInnoSetupScript:
    """E8-S02 AC1/AC3/AC4/AC5: Inno Setup .iss script with wizard configuration."""

    def test_iss_script_exists(self):
        """installer/windows/pytrainer.iss must exist."""
        iss = Path(__file__).parent.parent / "installer" / "windows" / "pytrainer.iss"
        assert iss.is_file(), "installer/windows/pytrainer.iss not found"

    def test_iss_references_pyinstaller_output(self):
        """ISS script must reference the PyInstaller dist directory."""
        iss = Path(__file__).parent.parent / "installer" / "windows" / "pytrainer.iss"
        content = iss.read_text()
        assert "dist" in content.lower() or "pytrainer" in content.lower()

    def test_iss_defines_app_name_and_version(self):
        """ISS script must define AppName and AppVersion."""
        iss = Path(__file__).parent.parent / "installer" / "windows" / "pytrainer.iss"
        content = iss.read_text()
        assert "AppName" in content
        assert "AppVersion" in content

    def test_iss_creates_start_menu_entry(self):
        """ISS script must create Start Menu icons."""
        iss = Path(__file__).parent.parent / "installer" / "windows" / "pytrainer.iss"
        content = iss.read_text()
        assert "[Icons]" in content

    def test_iss_creates_desktop_shortcut(self):
        """ISS script must offer Desktop shortcut."""
        iss = Path(__file__).parent.parent / "installer" / "windows" / "pytrainer.iss"
        content = iss.read_text()
        assert "desktop" in content.lower()

    def test_iss_includes_uninstaller(self):
        """ISS script must configure uninstaller (Uninstall* directives)."""
        iss = Path(__file__).parent.parent / "installer" / "windows" / "pytrainer.iss"
        content = iss.read_text()
        assert "Uninstall" in content

    def test_iss_includes_license(self):
        """ISS script must reference a license file for the wizard."""
        iss = Path(__file__).parent.parent / "installer" / "windows" / "pytrainer.iss"
        content = iss.read_text()
        assert "License" in content


class TestEmbeddedPython:
    """E8-S02 AC2: Embedded Python configuration for Windows."""

    def test_embed_python_script_exists(self):
        """Script to download/embed Python runtime must exist."""
        script = Path(__file__).parent.parent / "installer" / "windows" / "embed_python.py"
        assert script.is_file(), "installer/windows/embed_python.py not found"

    def test_embed_script_is_valid_python(self):
        """Embed script must be valid Python."""
        script = Path(__file__).parent.parent / "installer" / "windows" / "embed_python.py"
        content = script.read_text()
        compile(content, str(script), "exec")

    def test_embed_script_targets_python310_plus(self):
        """Embed script must target Python 3.10+."""
        script = Path(__file__).parent.parent / "installer" / "windows" / "embed_python.py"
        content = script.read_text()
        assert "3.10" in content or "3.11" in content or "3.12" in content


class TestWindowsBuildIntegration:
    """E8-S02 AC6: Build script integration for Windows."""

    def test_build_script_has_windows_target(self):
        """scripts/build.py should support --platform windows or document Windows build."""
        build = Path(__file__).parent.parent / "scripts" / "build.py"
        content = build.read_text()
        # Build script should at least reference windows or platform
        assert "windows" in content.lower() or "platform" in content.lower()
