"""Tests for macOS Distribution (E8-S04)."""

from pathlib import Path


class TestMacOSBuildScript:
    """E8-S04 AC1/AC2: macOS .dmg build script with universal2 support."""

    def test_macos_build_script_exists(self):
        """macOS build script must exist."""
        script = Path(__file__).parent.parent / "installer" / "macos" / "build_dmg.sh"
        assert script.is_file(), "installer/macos/build_dmg.sh not found"

    def test_script_references_dmg_creation(self):
        """Build script must create a .dmg."""
        script = Path(__file__).parent.parent / "installer" / "macos" / "build_dmg.sh"
        content = script.read_text()
        assert "dmg" in content.lower()

    def test_script_references_app_bundle(self):
        """Build script must reference .app bundle creation."""
        script = Path(__file__).parent.parent / "installer" / "macos" / "build_dmg.sh"
        content = script.read_text()
        assert ".app" in content

    def test_script_supports_universal2(self):
        """Build script should mention universal2 or both architectures."""
        script = Path(__file__).parent.parent / "installer" / "macos" / "build_dmg.sh"
        content = script.read_text()
        assert "universal2" in content or "arm64" in content or "x86_64" in content


class TestMacOSSpecConfig:
    """E8-S04 AC1: PyInstaller spec supports macOS .app bundle."""

    def test_spec_supports_windowed_mode(self):
        """Spec file should support --windowed for macOS .app bundle.
        The spec uses console=False on EXE which creates a windowed app.
        """
        spec = Path(__file__).parent.parent / "pytrainer.spec"
        content = spec.read_text()
        # console=False creates a windowed app (no terminal)
        assert "console=False" in content or "console = False" in content


class TestGatekeeperDocs:
    """E8-S04 AC4: Gatekeeper workaround documented."""

    def test_install_docs_cover_macos(self):
        """Installation docs must cover macOS."""
        install = Path(__file__).parent.parent / "docs" / "INSTALL.md"
        content = install.read_text()
        assert "macos" in content.lower() or "macOS" in content

    def test_install_docs_mention_gatekeeper(self):
        """Installation docs must mention Gatekeeper bypass."""
        install = Path(__file__).parent.parent / "docs" / "INSTALL.md"
        content = install.read_text()
        assert "gatekeeper" in content.lower() or "unsigned" in content.lower()

    def test_install_docs_mention_drag_to_applications(self):
        """Installation docs must mention drag-to-Applications workflow."""
        install = Path(__file__).parent.parent / "docs" / "INSTALL.md"
        content = install.read_text()
        assert "applications" in content.lower()
