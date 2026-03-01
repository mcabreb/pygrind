# E8-S02: Windows Installer

## Status
Done

## Epic
E8 - Distribution & Packaging

## Priority
Critical

## Estimate
M

## Description
[PCT] Create a wizard-style Windows installer using Inno Setup that bundles the PyInstaller output with an embedded Python runtime. Users get a familiar Next->Next->Install experience with Start Menu shortcut, Desktop shortcut, and uninstaller.

## Acceptance Criteria
- [x] Inno Setup .iss script wraps PyInstaller output into installer wizard
- [x] Installer bundles embedded Python 3.10+ runtime (no system Python required)
- [x] Wizard installation with license, destination, and progress bar
- [x] Creates Start Menu entry and optional Desktop shortcut
- [x] Includes functional uninstaller in Add/Remove Programs
- [x] Installer file size under 200 MB

## Tasks
- **T1: Create Inno Setup script** -- Write installer/windows/pytrainer.iss: source dir (PyInstaller dist/), output filename, Start Menu group, Desktop icon, uninstall support.
- **T2: Bundle embedded Python** -- Download Python 3.10+ embeddable package for Windows. Include in installer. Configure app to use this Python for code execution (not system Python).
- **T3: Test install/uninstall** -- Build installer, run on Windows 11 (VM or physical). Verify: install wizard, app launch from Start Menu, code execution works, uninstall removes all files.

## Technical Notes
- Inno Setup is free and well-documented. Embeddable Python: python.org/downloads -> Windows embeddable package. Must include python310._pth file configured to find user code. Alternative: NSIS if Inno Setup insufficient.

## Dependencies
- E8-S01 (PyInstaller Config) -- provides the packaged application to wrap in installer.

## Implementation Summary

**Files Created/Modified:**
- `installer/windows/pytrainer.iss` — Inno Setup script with wizard, shortcuts, uninstaller (~60 lines)
- `installer/windows/embed_python.py` — Downloads Python 3.12 embeddable package (~60 lines)
- `LICENSE` — MIT license for installer wizard display
- `scripts/build.py` — Updated with Windows platform documentation
- `tests/test_windows_installer.py` — 11 tests covering ISS script, embed script, integration

**Key Decisions:**
- Inno Setup over NSIS — better wizard UI, simpler scripting, widely used
- Python 3.12 embeddable package (~15 MB) avoids system Python dependency
- LZMA2/ultra64 compression to stay under 200 MB target
- `desktopicon` task unchecked by default (optional shortcut)

**Tests:** 11 new tests, all passing
**Branch:** hive/E8-distribution
**Date:** 2026-03-01
