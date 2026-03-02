# Building the Windows Installer (PyTrainer-Setup.exe)

This guide walks you through building the Windows installer on a Windows machine,
from cloning the repo to producing the final `PyTrainer-Setup.exe`.

## What You'll Produce

A single `PyTrainer-Setup.exe` file (~50-150 MB) that gives users a standard
Windows installation wizard: license agreement, folder selection, Start Menu and
Desktop shortcuts, and an uninstaller via Add/Remove Programs. The installer
bundles everything — including an embedded Python runtime — so end users don't
need Python installed on their system.

## Prerequisites

Install these on your Windows build machine:

| Tool | Version | Download |
|------|---------|----------|
| **Python** | 3.10+ | https://www.python.org/downloads/ |
| **Git** | any | https://git-scm.com/download/win |
| **Inno Setup** | 6+ | https://jrsoftware.org/isdl.php |

> During Python installation, check **"Add Python to PATH"**.
>
> During Inno Setup installation, the defaults are fine. The installer adds `iscc.exe`
> (the command-line compiler) to `C:\Program Files (x86)\Inno Setup 6\`.

## Step-by-Step Build

Open **PowerShell** or **Command Prompt** and run:

### 1. Clone the repository

```powershell
git clone https://github.com/pytrainer/pytrainer.git
cd pytrainer
```

### 2. Create a virtual environment and install dependencies

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

This installs PyQt6, QScintilla, PyYAML, platformdirs, and the dev tools
(pytest, ruff, **PyInstaller**).

### 3. Build the application with PyInstaller

```powershell
python scripts/build.py --clean
```

This runs PyInstaller using `pytrainer.spec` and produces:

```
dist\pytrainer\
├── pytrainer.exe      ← the main executable
├── exercises\          ← bundled problem files
├── PyQt6\              ← Qt runtime DLLs
└── ...                 ← other dependencies
```

> **Verify:** Run `dist\pytrainer\pytrainer.exe` to confirm the app launches correctly.

### 4. Download the embedded Python runtime

```powershell
python installer/windows/embed_python.py
```

This downloads the Python 3.12 embeddable package (~15 MB) from python.org and
extracts it to `installer/windows/python-embed/`. This minimal runtime is what
end users will use to execute their competition code — it's bundled inside the
installer so they don't need system Python.

### 5. Compile the installer with Inno Setup

**Option A — GUI:** Open `installer/windows/pytrainer.iss` in Inno Setup and
press **Build > Compile** (Ctrl+F9).

**Option B — Command line:**

```powershell
& "C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer\windows\pytrainer.iss
```

Output:

```
dist\PyTrainer-Setup.exe
```

> **Verify:** Run the installer on a clean machine (or VM) to confirm the wizard
> works, the app launches from Start Menu, and the uninstaller removes everything.

## Summary of Commands

```powershell
# Full build sequence (copy-paste friendly)
git clone https://github.com/pytrainer/pytrainer.git
cd pytrainer
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
python scripts/build.py --clean
python installer/windows/embed_python.py
& "C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer\windows\pytrainer.iss
# → dist\PyTrainer-Setup.exe is ready
```

## Publishing to GitHub Releases

Once you have `PyTrainer-Setup.exe`, publish it so users can download it:

1. Go to your GitHub repository page
2. Click **Releases** (right sidebar) > **Draft a new release**
3. Create a tag (e.g. `v1.0.0`), write release notes
4. Drag and drop `dist/PyTrainer-Setup.exe` into the **Attach binaries** area
5. Click **Publish release**

Users then visit your Releases page, download `PyTrainer-Setup.exe`, and
double-click it to get the standard install wizard — no Python, no git, no
terminal required.

## What the Installer Does for End Users

1. Shows a license agreement (MIT)
2. Lets them choose an install folder (default: `C:\Users\<name>\AppData\Local\Programs\PyTrainer`)
3. Creates a **Start Menu** shortcut
4. Optionally creates a **Desktop** shortcut
5. Installs the app + embedded Python runtime
6. Offers to launch PyTrainer immediately
7. Adds an entry to **Add/Remove Programs** for clean uninstallation

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pyinstaller` not found | Make sure `.venv\Scripts\activate` was run |
| `iscc` not found | Add Inno Setup to PATH or use full path as shown above |
| App crashes after install | Run `dist\pytrainer\pytrainer.exe` directly to see error output |
| `python-embed/` already exists | Delete `installer/windows/python-embed/` and re-run step 4 |
| Installer too large | Check that `dist/` doesn't contain stale builds; use `--clean` flag |

## Version Updates

When releasing a new version, update the version number in **both** files:

- `pyproject.toml` → `version = "x.y.z"`
- `installer/windows/pytrainer.iss` → `#define AppVersion "x.y.z"`
