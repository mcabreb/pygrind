# E4-S07: Timer Widget

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
M

## Description
[PCT] A prominent countdown display showing remaining competition time in HH:MM:SS format. Changes color at 30 minutes (warning yellow) and 5 minutes (urgent red). Shows a pause indicator when code is executing.

## Acceptance Criteria
- [x] Displays time in HH:MM:SS format with large, bold font (20pt+)
- [x] Default color: standard text color
- [x] At 30 minutes remaining (1800s): text turns yellow/orange
- [x] At 5 minutes remaining (300s): text turns red and bold
- [x] When paused: shows pause icon or 'PAUSED' indicator
- [x] update_time(remaining_secs: int) method refreshes the display

## Tasks
- **T1: Implement TimerWidget** — Create ui/timer_widget.py with TimerWidget(QWidget). Large QLabel centered. Format seconds as HH:MM:SS string.
- **T2: Add color thresholds** — In update_time(): apply QLabel.setStyleSheet() with color based on remaining_secs thresholds (>1800: default, <=1800: orange, <=300: red).
- **T3: Add pause indicator** — set_paused(paused: bool) toggles a secondary QLabel showing 'PAUSED' or shows/hides it.

## Technical Notes
- HH:MM:SS format: f"{secs//3600:02d}:{(secs%3600)//60:02d}:{secs%60:02d}". Color via stylesheet: setStyleSheet("color: #f44336; font-weight: bold;"). Pause indicator positioned next to or below the time.

## Dependencies
- E4-S01 (Application Shell) -- provides the ui/ package.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/ui/timer_widget.py` — TimerWidget with HH:MM:SS display, color thresholds, pause (~52 lines)
- `tests/ui/test_timer_widget.py` — 13 tests covering all ACs

**Key Decisions:**
- Color thresholds via setStyleSheet: >1800s default, <=1800s orange, <=300s red
- PAUSED label visibility toggled via set_paused()

**Tests:** 13 new tests, all passing
**Branch:** hive/E4-competition-ui
**Date:** 2026-03-01
