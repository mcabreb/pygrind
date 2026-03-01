"""Tests for Linux Distribution (E8-S03)."""

from pathlib import Path


class TestAppImageAssets:
    """E8-S03 AC1/AC4: AppImage packaging assets and desktop integration."""

    def test_desktop_file_exists(self):
        """AppImage .desktop file must exist."""
        desktop = Path(__file__).parent.parent / "installer" / "linux" / "pytrainer.desktop"
        assert desktop.is_file(), "installer/linux/pytrainer.desktop not found"

    def test_desktop_file_has_required_fields(self):
        """Desktop file must have Name, Exec, Icon, Type, Categories."""
        desktop = Path(__file__).parent.parent / "installer" / "linux" / "pytrainer.desktop"
        content = desktop.read_text()
        assert "[Desktop Entry]" in content
        assert "Name=" in content
        assert "Exec=" in content
        assert "Icon=" in content
        assert "Type=" in content
        assert "Categories=" in content

    def test_icon_file_exists(self):
        """Application icon must exist (PNG or SVG)."""
        linux_dir = Path(__file__).parent.parent / "installer" / "linux"
        icons = list(linux_dir.glob("pytrainer.*"))
        icon_exts = {p.suffix for p in icons}
        assert icon_exts & {".png", ".svg"}, "No pytrainer.png or .svg icon found"

    def test_appimage_build_script_exists(self):
        """AppImage build script must exist."""
        script = Path(__file__).parent.parent / "installer" / "linux" / "build_appimage.sh"
        assert script.is_file(), "installer/linux/build_appimage.sh not found"

    def test_appimage_script_references_appimagetool(self):
        """Build script should reference appimagetool."""
        script = Path(__file__).parent.parent / "installer" / "linux" / "build_appimage.sh"
        content = script.read_text()
        assert "appimagetool" in content.lower() or "appimage" in content.lower()


class TestLinuxBuildIntegration:
    """E8-S03 AC1: Build script integration for Linux AppImage."""

    def test_build_script_has_linux_target(self):
        """scripts/build.py should document Linux build process."""
        build = Path(__file__).parent.parent / "scripts" / "build.py"
        content = build.read_text()
        assert "linux" in content.lower()


class TestInstallDocs:
    """E8-S03 AC3: Installation instructions documented."""

    def test_install_docs_exist(self):
        """docs/INSTALL.md must exist with Linux instructions."""
        install = Path(__file__).parent.parent / "docs" / "INSTALL.md"
        assert install.is_file(), "docs/INSTALL.md not found"

    def test_install_docs_cover_linux(self):
        """Installation docs must cover Linux."""
        install = Path(__file__).parent.parent / "docs" / "INSTALL.md"
        content = install.read_text()
        assert "linux" in content.lower() or "ubuntu" in content.lower()

    def test_install_docs_cover_appimage(self):
        """Installation docs must mention AppImage."""
        install = Path(__file__).parent.parent / "docs" / "INSTALL.md"
        content = install.read_text()
        assert "appimage" in content.lower() or "AppImage" in content
