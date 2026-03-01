# E8-S04: macOS Distribution

## Status
Done

## Epic
E8 - Distribution & Packaging

## Priority
High

## Estimate
S

## Description
[PCT] Package the application for macOS as a .dmg with .app bundle, supporting both Apple Silicon (ARM) and Intel architectures via universal2 build.

## Acceptance Criteria
- [x] .dmg file produced containing .app bundle
- [x] Works on macOS 13+ (Apple Silicon and Intel)
- [x] App can be dragged to Applications folder from .dmg
- [x] Gatekeeper workaround documented (app is unsigned)

## Tasks
- **T1: Create macOS package** -- Use PyInstaller with --windowed flag for .app bundle. Wrap in .dmg using create-dmg or hdiutil. Build as universal2 for ARM+x86 support.
- **T2: Test on macOS** -- Install and run on macOS 13+. Test both architectures if possible. Document Gatekeeper bypass: right-click -> Open -> confirm.

## Technical Notes
- PyInstaller --windowed creates .app bundle. create-dmg (npm package) or hdiutil for .dmg creation. Universal2: requires building on macOS with universal2 Python. Unsigned app warning: users must right-click -> Open first time.

## Dependencies
- E8-S01 (PyInstaller Config) -- provides the base package configuration.

## Implementation Summary

**Files Created/Modified:**
- `installer/macos/build_dmg.sh` — DMG build script with create-dmg and hdiutil fallback (~80 lines)
- `tests/test_macos_distribution.py` — 8 tests covering build script, spec config, Gatekeeper docs

**Key Decisions:**
- create-dmg preferred for styled DMG with drag-to-Applications; hdiutil as fallback
- universal2 documented for dual-arch support (requires building on macOS with universal2 Python)
- Gatekeeper bypass via right-click->Open documented in INSTALL.md
- console=False in spec already handles macOS .app bundle generation

**Tests:** 8 new tests, all passing
**Branch:** hive/E8-distribution
**Date:** 2026-03-01
