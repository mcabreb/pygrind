# Installation Guide

## Linux (Ubuntu 22.04+)

### Option 1: AppImage (Recommended)

Download the latest `PyTrainer-x86_64.AppImage` from the releases page.

```bash
chmod +x PyTrainer-x86_64.AppImage
./PyTrainer-x86_64.AppImage
```

No installation required — the AppImage is self-contained.

### Option 2: pip install

Requires Python 3.10+ and system Qt6 libraries.

```bash
pip install pytrainer
pytrainer
```

### Building the AppImage from source

```bash
git clone https://github.com/pytrainer/pytrainer.git
cd pytrainer
pip install -e ".[dev]"
python scripts/build.py
bash installer/linux/build_appimage.sh
```

## Windows

### Installer (Recommended)

Download and run `PyTrainer-Setup.exe`. The installer wizard will guide you through:

1. License agreement
2. Installation directory selection
3. Start Menu and Desktop shortcut options

The installer bundles an embedded Python runtime — no system Python required.

### Uninstalling

Use **Add/Remove Programs** in Windows Settings.

## macOS (13+)

### DMG (Recommended)

1. Download `PyTrainer.dmg`
2. Open the DMG and drag PyTrainer to Applications
3. On first launch, right-click the app and select **Open** to bypass Gatekeeper (the app is unsigned)

Supports both Apple Silicon (ARM) and Intel architectures.
