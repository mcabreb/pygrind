# E4-S03: Session Configuration Dialog

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
S

## Description
[PCT] A pre-session screen where the user selects difficulty mode (Beginner/Medium/Difficult) before starting a competition. Each mode shows a brief description of what help is available.

## Acceptance Criteria
- [x] Shows 3 radio buttons: Beginner, Medium, Difficult
- [x] Each mode has description: Beginner='Hints visible, solutions available', Medium='Hints on request, no solutions', Difficult='No hints, no solutions'
- [x] 'Start Session' button emits signal with selected DifficultyMode enum
- [x] 'Back' button returns to main menu

## Tasks
- **T1: Implement SessionConfigDialog** — QWidget with QButtonGroup of 3 QRadioButtons. QLabel descriptions below each. Start and Back QPushButtons.
- **T2: Connect to session start** — On Start: emit mode_selected(DifficultyMode) signal. MainWindow receives and calls show_competition().

## Technical Notes
- Default selection: Medium (most common use case for competition prep). Radio button group ensures exactly one selection.

## Dependencies
- E4-S01 (Application Shell) -- provides MainWindow navigation.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/ui/session_config.py` — SessionConfigScreen with radio buttons, descriptions, signals (~70 lines)
- `tests/ui/test_session_config.py` — 9 tests covering all ACs

**Key Decisions:**
- QButtonGroup with integer IDs mapped to DifficultyMode enum values
- Default selection is Medium per ticket spec

**Tests:** 9 new tests, all passing
**Branch:** hive/E4-competition-ui
**Date:** 2026-03-01
