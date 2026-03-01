# E4-S06: Output Panel

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
S

## Description
[PCT] The panel below the editor showing execution results: pass/fail status per test case, error messages and tracebacks, output diff on mismatch, and timeout indicators. Gives users immediate feedback on their submissions.

## Acceptance Criteria
- [x] Shows pass/fail status per test case with green checkmark / red X indicators
- [x] Displays error messages and tracebacks in monospace red text
- [x] Shows expected vs actual diff on output mismatch
- [x] Shows 'Time Limit Exceeded (10s)' message on timeout
- [x] clear() method resets the panel between executions

## Tasks
- **T1: Implement OutputPanel layout** — Create ui/output.py with OutputPanel(QWidget). QScrollArea with vertical layout. Dynamically add result widgets per test case.
- **T2: Implement display methods** — show_results(results: list), show_error(message: str), show_timeout(), show_safety_violation(violations: list[str]), clear(). Each creates appropriate styled widgets.

## Technical Notes
- Use green/red colored QLabels for pass/fail. Monospace font for all output text. Diff format: "Expected: X\nGot: Y" for each mismatched line.

## Dependencies
- E4-S01 (Application Shell) -- provides the ui/ package.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/ui/output.py` — OutputPanel with show_results, show_error, show_timeout, clear (~85 lines)
- `tests/ui/test_output_panel.py` — 8 tests covering all ACs

**Key Decisions:**
- Dynamic widget creation per test case result (cleared between runs)
- setParent(None) instead of deleteLater() for immediate cleanup in clear()
- Added show_safety_violation() for future E3 integration

**Tests:** 8 new tests, all passing
**Branch:** hive/E4-competition-ui
**Date:** 2026-03-01
