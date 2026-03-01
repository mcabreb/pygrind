# PyTrainer — Python Competition Trainer

A cross-platform desktop application that simulates HP Code Wars-style coding competitions. Solve 30 randomly selected Python problems across 5 difficulty tiers within a 3-hour timed session.

## Prerequisites

- Python 3.10+
- Qt6 runtime libraries

## Development Setup

```bash
# Clone and install
git clone <repo-url>
cd python-test-suite

# Create virtual environment and install with dev dependencies
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

pip install -e ".[dev]"
```

## Development Commands

```bash
# Run the application
python -m pytrainer

# Run tests
pytest

# Lint
ruff check .

# Format
ruff format .
```

## Project Structure

```
src/pytrainer/
├── models/     # Data models (Exercise, Session, etc.)
├── core/       # Business logic (loader, runner, validator, scorer)
├── storage/    # SQLite persistence and auto-save
└── ui/         # PyQt6 user interface components
```
