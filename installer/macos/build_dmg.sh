#!/usr/bin/env bash
# Build PyTrainer .dmg for macOS from PyInstaller .app bundle.
#
# Prerequisites:
#   1. Build on macOS with universal2 Python:
#      python scripts/build.py
#   2. Optional: install create-dmg for a styled DMG:
#      brew install create-dmg
#
# The PyInstaller spec uses console=False which produces a .app bundle
# on macOS (via --windowed). This script wraps it in a .dmg.
#
# Architecture support:
#   - For universal2 (arm64 + x86_64), build with a universal2 Python
#   - For single-arch, use native Python on the target architecture
#
# Usage:
#   bash installer/macos/build_dmg.sh
#
# Output: dist/PyTrainer.dmg

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
APP_BUNDLE="$DIST_DIR/pytrainer.app"
DMG_OUTPUT="$DIST_DIR/PyTrainer.dmg"

# Check prerequisites
if [ ! -d "$APP_BUNDLE" ]; then
    echo "ERROR: .app bundle not found at $APP_BUNDLE"
    echo "Build on macOS first: python scripts/build.py"
    echo ""
    echo "Note: PyInstaller creates a .app bundle on macOS when console=False."
    echo "On Linux, only a directory is produced (not a .app)."
    exit 1
fi

# Remove old DMG
rm -f "$DMG_OUTPUT"

echo "Building PyTrainer.dmg..."

if command -v create-dmg &>/dev/null; then
    # Styled DMG with create-dmg (prettier)
    create-dmg \
        --volname "PyTrainer" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "pytrainer.app" 150 190 \
        --app-drop-link 450 190 \
        --no-internet-enable \
        "$DMG_OUTPUT" \
        "$APP_BUNDLE"
else
    # Fallback: plain DMG with hdiutil
    echo "create-dmg not found — using hdiutil (plain DMG without styling)"
    STAGING="$DIST_DIR/dmg-staging"
    rm -rf "$STAGING"
    mkdir -p "$STAGING"
    cp -r "$APP_BUNDLE" "$STAGING/"
    ln -s /Applications "$STAGING/Applications"

    hdiutil create -volname "PyTrainer" \
        -srcfolder "$STAGING" \
        -ov -format UDZO \
        "$DMG_OUTPUT"

    rm -rf "$STAGING"
fi

echo ""
echo "DMG built: $DMG_OUTPUT"
echo ""
echo "To install:"
echo "  1. Open PyTrainer.dmg"
echo "  2. Drag PyTrainer.app to Applications"
echo "  3. First launch: right-click -> Open (Gatekeeper bypass for unsigned app)"
