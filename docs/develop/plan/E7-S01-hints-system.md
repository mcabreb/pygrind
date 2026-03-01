# E7-S01: Hints System

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
High

## Estimate
S

## Description
[PCT] Implement mode-based hint display. In Beginner mode, hints appear automatically below the problem description. In Medium mode, a 'Show Hint' button reveals the hint on click (one-way -- cannot re-hide). In Difficult mode, no hints are shown. Helps learners build problem-solving skills progressively.

## Acceptance Criteria
- [x] Beginner mode: hint text shown automatically below problem description
- [x] Medium mode: 'Show Hint' button visible; clicking reveals hint (one-way, cannot re-hide)
- [x] Difficult mode: no hint button or text visible
- [x] If exercise has no hint defined: shows 'No hint available'
- [x] ProblemState.hint_viewed tracked when hint is revealed

## Tasks
- **T1: Add hint UI to ProblemPanel** -- Add hint QLabel and 'Show Hint' QPushButton to ProblemPanel. set_exercise() configures visibility based on current DifficultyMode. Hint text styled in italic with distinct background.
- **T2: Wire hint state tracking** -- On hint button click: show hint text, set ProblemState.hint_viewed = True, disable button (prevent re-click). Connect to SessionManager state.

## Technical Notes
- Hint visibility logic in set_exercise(exercise, mode). Beginner: show hint QLabel directly. Medium: show button, hide hint until clicked. Difficult: hide both.

## Dependencies
- E5-S02 (Competition Window) -- provides the ProblemPanel to extend with hint UI.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/ui/problem.py` — Added hint_viewed signal, hint QLabel, Show Hint QPushButton, mode-based visibility logic in set_exercise() (~30 lines added)
- `tests/ui/test_hints.py` — 12 tests covering beginner/medium/difficult modes, fallback text, signal emission (new file)

**Key Decisions:**
- Made `mode` parameter optional (default None) in set_exercise() for backward compatibility with existing callers
- hint_viewed signal emitted from ProblemPanel so any controller can track it on ProblemState

**Tests:** 12 new tests, all passing
**Branch:** hive/E7-learning-analytics
**Date:** 2026-03-01
