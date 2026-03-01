# E5-S02: Competition Window Layout

## Status
Done

## Epic
E5 - Session Orchestration & Game Loop

## Priority
Critical

## Estimate
M

## Description
[PCT] The main competition screen that wires all UI widgets together into a functional workspace: problem panel on the left, code editor on the right, output panel below the editor, timer at the top, and Run/Submit buttons. This is where users spend their entire 3-hour session.

## Acceptance Criteria
- [x] Problem panel occupies left side (30-40% width)
- [x] Code editor occupies right side (60-70% width) with Run/Submit buttons below
- [x] Output panel below the editor (collapsible or resizable)
- [x] Timer widget prominently at the top center
- [x] QSplitter allows user to resize panels
- [x] Ctrl+Enter triggers Submit from anywhere in the editor

## Tasks
- **T1: Implement CompetitionWindow** — Create ui/competition.py. Use QSplitter for left/right. Nest vertical QSplitter for editor/output on right side. Add QToolBar or button bar with Run/Submit.
- **T2: Wire widget connections** — Connect Run/Submit buttons to handler methods. Connect SessionManager.problem_updated to UI refresh. Connect TimerController.tick to TimerWidget.update_time.
- **T3: Add keyboard shortcut** — QShortcut(QKeySequence('Ctrl+Return'), self, submit_action). Verify it works when editor has focus.

## Technical Notes
- QSplitter preserves user's panel sizes during session. Initial splitter ratio: 35/65 left/right.
- Button bar: Run (test sample) | Submit (test all) | separate from editor toolbar.

## Dependencies
- E4-S04 (QScintilla Editor) -- provides EditorWidget.
- E4-S05 (Problem Panel) -- provides ProblemPanel.
- E4-S06 (Output Panel) -- provides OutputPanel.
- E4-S07 (Timer Widget) -- provides TimerWidget.
- E5-S01 (Session Manager) -- provides session state and logic.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/ui/competition.py` — CompetitionWindow with QSplitter layout, buttons, Ctrl+Return shortcut (~85 lines)
- `tests/ui/test_competition.py` — 12 tests covering all 6 ACs (~120 lines)

**Key Decisions:**
- Horizontal QSplitter at 35/65 ratio for problem/editor, vertical QSplitter at 70/30 for editor/output
- run_requested / submit_requested signals decouple buttons from action logic (wired in E5-S03)
- QScintilla mocked at sys.modules level in tests for headless CI compatibility

**Tests:** 12 new tests, all passing
**Branch:** hive/E5-session-orchestration
**Date:** 2026-03-01
