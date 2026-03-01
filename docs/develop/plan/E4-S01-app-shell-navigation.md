# E4-S01: Application Shell & Screen Navigation

## Status
To Do

## Epic
E4 - Competition UI Shell

## Priority
Critical

## Estimate
M

## Description
[PCT] Set up the QApplication with a top-level exception handler and a QStackedWidget for navigating between screens (main menu, session config, competition, results, history). This is the application skeleton that hosts all UI screens.

## Acceptance Criteria
- [x] QApplication starts and shows main window with title 'Python Competition Trainer'
- [x] Top-level exception handler catches unhandled errors and shows QMessageBox dialog
- [x] QStackedWidget enables switching between screens without window recreation
- [x] Logging configured to file at platformdirs user_data_dir with 5MB rotation
- [x] Window size defaults to 1200x800, resizable

## Tasks
- **T1: Implement app.py main()** — Create QApplication, configure logging (file handler at user_data_dir('pytrainer')/pytrainer.log + RotatingFileHandler), set up sys.excepthook, create MainWindow, show().
- **T2: Create MainWindow class** — QMainWindow subclass with QStackedWidget as central widget. Methods: show_menu(), show_config(), show_competition(session), show_results(result), show_history().
- **T3: Add error handler** — Override sys.excepthook to log exception traceback and show QMessageBox.critical(). Ensure app doesn't silently crash.

## Technical Notes
- Use platformdirs.user_data_dir("pytrainer") for log path. Window state NOT persisted (keep simple).

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the ui/ package and app.py stub.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/app.py` — Rewrote with configure_logging(), install_exception_handler(), --version support (~70 lines)
- `src/pytrainer/ui/main_window.py` — MainWindow with QStackedWidget, screen register/show methods (~57 lines)
- `tests/ui/test_app_shell.py` — 12 tests covering all ACs
- `tests/test_project_structure.py` — Updated entry point test to use --version flag

**Key Decisions:**
- Screen registration pattern (register_menu/register_config/etc.) for decoupled screen management
- Added --version flag to main() so entry point test works without blocking on GUI event loop
- Lazy QMessageBox import in exception handler to allow headless test imports

**Tests:** 12 new tests, all passing
**Branch:** hive/E4-competition-ui
**Date:** 2026-03-01
