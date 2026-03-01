# E1-S02: Configure Developer Tooling

## Status
Done

## Epic
E1 - Project Foundation & Dev Environment

## Priority
Critical

## Estimate
S

## Description
[PCT] Set up ruff for linting/formatting, pytest + pytest-qt for testing, .gitignore for Python/Qt artifacts, and verify the complete dev workflow (install, lint, test, format). This ensures consistent code quality from the start.

## Acceptance Criteria
- [x] ruff check . passes with zero warnings on the scaffold
- [x] ruff format . produces no changes (code is already formatted)
- [x] pytest runs and discovers test directory (0 tests initially is OK)
- [x] .gitignore covers: __pycache__, .venv, *.pyc, .eggs, dist/, build/, *.egg-info, .pytest_cache, .ruff_cache
- [x] README.md updated with project description and dev setup instructions

## Tasks
- **T1: Configure ruff** — Verify ruff config in pyproject.toml: line-length=99, target-version=py310, select rules [E,F,W,I,N,UP,B,SIM], quote-style=double. Run ruff check and ruff format to validate.
- **T2: Configure pytest** — Add [tool.pytest.ini_options] to pyproject.toml: testpaths=['tests'], python_files='test_*.py'. Verify pytest discovers tests/ directory. Add conftest.py stub.
- **T3: Create .gitignore and update README** — Write comprehensive .gitignore for Python/Qt/IDE artifacts. Update README.md with project name, description, prerequisites, and dev setup commands.

## Technical Notes
- ruff replaces black + flake8 + isort in a single tool
- Line length: 99 chars (matches architecture spec)
- pytest-qt will be used starting in E4 for UI tests

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the project scaffold to configure tooling on.

## Implementation Summary

**Files Created/Modified:**
- `README.md` — Updated with project description, prereqs, dev setup, commands (~40 lines)
- `tests/conftest.py` — Shared fixtures stub (~1 line)
- `tests/test_dev_tooling.py` — Tooling validation tests (15 tests)

**Key Decisions:**
- `.gitignore` already comprehensive from initial commit; uses `*.py[codz]` glob covering `.pyc`
- ruff config already in pyproject.toml from S01; verified passing

**Tests:** 15 new tests, all passing (27 total)
**Branch:** hive/E1-project-foundation
**Date:** 2026-03-01
