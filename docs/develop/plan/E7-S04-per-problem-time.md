# E7-S04: Per-Problem Time Tracking

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
Must

## Estimate
S

## Description
[PCT] Track how much time the user spends on each individual problem. Timer switches when the user navigates between problems. Per-problem times are displayed in the session results breakdown for time management analysis.

## Acceptance Criteria
- [x] TimerController tracks cumulative seconds per problem index
- [x] switch_problem(idx) accumulates elapsed time to previous problem and starts new counter
- [x] Per-problem time written to ProblemState.time_spent on session end
- [x] ResultsScreen shows per-problem time in the breakdown table (MM:SS format)

## Tasks
- **T1: Extend TimerController** -- Add _problem_times: dict[int, float] and _current_problem: int. In switch_problem(idx): add elapsed to previous, reset for new. Use QElapsedTimer for accurate sub-second tracking.
- **T2: Integrate with results** -- On session end: populate each ProblemState.time_spent. ResultsScreen formats as MM:SS in the time column.

## Technical Notes
- switch_problem() called by CompetitionWindow when problem_selected signal fires. Same QElapsedTimer approach as global timer -- monotonic, no drift.

## Dependencies
- E5-S01 (Session Manager) -- provides the session and timer infrastructure.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/timer_controller.py` — New TimerController class with start/switch_problem/stop/finalize using time.monotonic() (~60 lines)
- `tests/core/test_timer_controller.py` — 8 tests covering tracking, switching, accumulation, finalize, MM:SS format (new file)

**Key Decisions:**
- Used time.monotonic() instead of QElapsedTimer for pure-Python testability without Qt event loop
- finalize() auto-stops if still running, then writes to ProblemState list

**Tests:** 8 new tests, all passing
**Branch:** hive/E7-learning-analytics
**Date:** 2026-03-01
