# E7-S07: Exercise Flagging

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
Must

## Estimate
S

## Description
[PCT] Allow users to flag exercises they believe have incorrect test cases or ambiguous descriptions. Flags are stored locally in SQLite with optional comments. A summary of all flags is accessible from the main menu for review.

## Acceptance Criteria
- [x] 'Flag Problem' button visible on each problem in the competition view
- [x] Clicking opens input dialog for optional comment text
- [x] Flag stored in SQLite: exercise_id, session_id, timestamp, comment
- [x] Flagged Exercises summary accessible from main menu
- [x] Duplicate flags for same exercise in same session are prevented

## Tasks
- **T1: Add flag UI** -- Add 'Flag' QPushButton to ProblemPanel. On click: QInputDialog.getText() for optional comment. Call Database.save_flag().
- **T2: Add flag summary screen** -- Add 'Flagged Exercises' button to MainMenu. QTableWidget showing: exercise title, tier, flag date, comment. Load from Database.get_flags().

## Technical Notes
- exercise_flags table: id, exercise_id, session_id (nullable for outside-session flags), timestamp (ISO 8601), comment (nullable). Duplicate prevention: check if flag exists for (exercise_id, session_id) before INSERT.

## Dependencies
- E7-S05 (SQLite Persistence) -- provides Database with exercise_flags table.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/ui/problem.py` — Added flag_requested signal and Flag Problem QPushButton, visible in all difficulty modes (~10 lines added)
- `src/pytrainer/ui/main_menu.py` — Added flags_requested signal and Flagged Exercises button (~8 lines added)
- `tests/ui/test_flagging.py` — 10 tests covering button visibility, signal emission, DB storage, duplicate prevention, main menu integration (new file)

**Key Decisions:**
- Flag button visible in all modes (Beginner/Medium/Difficult) — flagging is about exercise quality, not difficulty
- flag_requested signal emitted from ProblemPanel; controller handles dialog + DB save
- Flagged Exercises button added to main menu between Session History and Quit

**Tests:** 10 new tests, all passing
**Branch:** hive/E7-learning-analytics
**Date:** 2026-03-01
