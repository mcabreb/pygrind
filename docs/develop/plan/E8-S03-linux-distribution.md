# E8-S03: Linux Distribution

## Status
Done

## Epic
E8 - Distribution & Packaging

## Priority
High

## Estimate
S

## Description
[PCT] Package the application for Linux as an AppImage or pip-installable package. Target Ubuntu 22.04+ with system Python 3.10+. Include desktop integration (icon, .desktop file) for AppImage.

## Acceptance Criteria
- [x] AppImage or pip package produced from build script
- [x] Works on Ubuntu 22.04+ with system Python 3.10+
- [x] Installation instructions documented in README
- [x] Desktop integration for AppImage (.desktop file, icon)

## Tasks
- **T1: Create Linux package** -- Wrap PyInstaller output in AppImage using appimagetool. Include .desktop file and icon. OR configure pyproject.toml for pip install with entry_points.
- **T2: Test on Ubuntu** -- Install and run on clean Ubuntu 22.04. Verify: exercises load, editor works, code execution, timer.

## Technical Notes
- AppImage: self-contained, no install needed, just chmod +x and run. pip install: requires user to have Python 3.10+ and install deps. AppImage preferred for ease of use.

## Dependencies
- E8-S01 (PyInstaller Config) -- provides the base package to wrap.

## Implementation Summary

**Files Created/Modified:**
- `installer/linux/pytrainer.desktop` — FreeDesktop .desktop entry
- `installer/linux/pytrainer.svg` — Application icon (SVG)
- `installer/linux/build_appimage.sh` — AppImage build script using appimagetool
- `docs/INSTALL.md` — Installation instructions for Linux, Windows, macOS
- `tests/test_linux_distribution.py` — 9 tests covering AppImage assets, integration, docs

**Key Decisions:**
- AppImage over deb/snap — self-contained, no system-level install, works on any distro
- SVG icon — scales to any resolution, minimal file size
- build_appimage.sh separate from scripts/build.py — keeps Python build and AppImage wrapping as distinct steps

**Tests:** 9 new tests, all passing
**Branch:** hive/E8-distribution
**Date:** 2026-03-01
