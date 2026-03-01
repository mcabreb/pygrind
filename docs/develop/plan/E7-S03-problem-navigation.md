# E7-S03: Problem Navigation Sidebar

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
High

## Estimate
M

## Description
[PCT] A sidebar showing all 30 problems with status indicators. Users can click any problem to jump to it, use next/prev buttons, and see at a glance which problems are solved, attempted, or untouched. Editor state is preserved when navigating between problems.

## Acceptance Criteria
- [x] Sidebar shows all 30 problems with number, abbreviated title, and status icon
- [x] Status icons: grey circle (unsolved), yellow triangle (attempted), green checkmark (solved)
- [x] Clicking a problem jumps to it (updates problem panel and editor)
- [x] Next/Previous buttons at top of sidebar
- [x] Current problem highlighted with distinct background
- [x] Editor code preserved when navigating away and restored when returning

## Tasks
- **T1: Implement ProblemListWidget** -- Create ui/problem_list.py. QListWidget with custom items showing "1. Hello Wor..." + status icon. Emit problem_selected(idx: int) signal on click.
- **T2: Wire navigation** -- Connect problem_selected to CompetitionWindow. Before switching: save current editor code to ProblemState.code. After switching: restore ProblemState.code to editor.
- **T3: Add next/prev buttons** -- QPushButtons above the list. Wire to current_index +/- 1 with bounds checking (wrap or disable at edges).

## Technical Notes
- Status icons: use Unicode characters or QIcon with colored pixmaps. Title truncation: first 20 chars + '...' if longer. Sidebar width: ~200px.

## Dependencies
- E5-S02 (Competition Window) -- provides the layout to add sidebar to.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/ui/problem_list.py` — New ProblemListWidget with QListWidget, next/prev buttons, status icons, problem_selected signal (~100 lines)
- `tests/ui/test_problem_list.py` — 13 tests covering display, icons, click nav, next/prev, highlight, status update (new file)

**Key Decisions:**
- Used Unicode emoji for status icons (⚪/🔶/✅) for simplicity — avoids QIcon/pixmap complexity
- Title truncation at 20 chars with ellipsis
- Signal suppression during programmatic selection to avoid spurious emissions

**Tests:** 13 new tests, all passing
**Branch:** hive/E7-learning-analytics
**Date:** 2026-03-01
