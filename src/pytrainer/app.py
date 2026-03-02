"""PyTrainer application entry point."""

import logging
import logging.handlers
import sys
import traceback
from pathlib import Path

from platformdirs import user_data_dir

# Lazy import to allow tests to import functions without full Qt init
QMessageBox = None


def _get_qmessagebox():
    global QMessageBox  # noqa: N814
    if QMessageBox is None:
        from PyQt6.QtWidgets import QMessageBox  # noqa: N814

    return QMessageBox


def configure_logging() -> logging.Logger:
    """Configure rotating file logging at platformdirs user_data_dir."""
    log_dir = Path(user_data_dir("pytrainer"))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "pytrainer.log"

    logger = logging.getLogger("pytrainer")
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers on repeated calls
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) for h in logger.handlers):
        handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
        )
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def install_exception_handler() -> None:
    """Install a global exception handler that logs and shows a dialog."""

    def _handle_exception(exc_type, exc_value, exc_tb):
        logger = logging.getLogger("pytrainer")
        tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        logger.critical("Unhandled exception:\n%s", tb_text)

        msgbox = _get_qmessagebox()
        msgbox.critical(
            None,
            "Unexpected Error",
            f"{exc_type.__name__}: {exc_value}",
        )

    sys.excepthook = _handle_exception


def main(argv: list[str] | None = None) -> None:
    """Launch the PyTrainer application.

    With ``--version`` or without a GUI environment, prints version info and exits.
    """
    if argv is None:
        argv = sys.argv

    if "--version" in argv or "-V" in argv:
        from pytrainer import __version__

        print(f"PyTrainer v{__version__} — Python Competition Trainer")
        sys.exit(0)

    from PyQt6.QtCore import QTimer
    from PyQt6.QtWidgets import QApplication, QMessageBox

    from pytrainer.core.analytics import SessionAnalytics
    from pytrainer.core.loader import ExerciseLoader
    from pytrainer.core.pipeline import ExecutionPipeline
    from pytrainer.core.scanner import SafetyScanner
    from pytrainer.core.session_mgr import SessionManager
    from pytrainer.core.timer_controller import TimerController
    from pytrainer.models.session import DifficultyMode, SessionConfig
    from pytrainer.paths import get_exercises_dir
    from pytrainer.settings import load_settings
    from pytrainer.storage.database import Database
    from pytrainer.ui.competition import CompetitionWindow
    from pytrainer.ui.history import HistoryScreen
    from pytrainer.ui.main_menu import MainMenuScreen
    from pytrainer.ui.main_window import MainWindow
    from pytrainer.ui.results import ResultsScreen
    from pytrainer.ui.session_config import SessionConfigScreen
    from pytrainer.ui.submit_flow import SubmitFlowController

    app = QApplication(argv)

    configure_logging()
    install_exception_handler()
    log = logging.getLogger("pytrainer.app")

    # -- Load exercises --------------------------------------------------------
    exercises_dir = get_exercises_dir()
    loader = ExerciseLoader(exercises_dir)
    exercise_index = loader.load_all()
    total_exercises = sum(len(v) for v in exercise_index.values())
    log.info("Loaded %d exercises from %s", total_exercises, exercises_dir)

    # -- Settings & Database ---------------------------------------------------
    settings = load_settings()
    db_path = Path(user_data_dir("pytrainer")) / "pytrainer.db"
    db = Database(db_path)

    # -- Create UI screens -----------------------------------------------------
    window = MainWindow()
    menu = MainMenuScreen()
    config = SessionConfigScreen()
    competition = CompetitionWindow()
    results = ResultsScreen()
    history = HistoryScreen()

    window.register_menu(menu)
    window.register_config(config)
    window.register_competition(competition)
    window.register_results(results)
    window.register_history(history)

    # -- Mutable session state (replaced each session) -------------------------
    state: dict = {
        "session_mgr": None,
        "submit_flow": None,
        "timer_ctrl": None,
        "tick_timer": None,
        "pipeline": None,
        "session_elapsed": 0,
        "problem_elapsed": 0,
        "score_frozen": False,
        "warning_level": "normal",
    }

    # -- Helpers ---------------------------------------------------------------

    def _load_problem(index: int) -> None:
        """Display the problem at the given index in the competition UI."""
        mgr = state["session_mgr"]
        if mgr is None:
            return

        # Save current editor code before switching
        if mgr.current_problem_index != index:
            mgr.current_problem.code = competition.editor.text()

        mgr.current_problem_index = index
        ps = mgr.current_problem

        # Update timer tracking
        timer_ctrl = state["timer_ctrl"]
        if timer_ctrl is not None:
            timer_ctrl.switch_problem(index)

        # Reset per-problem timer display
        state["problem_elapsed"] = int(ps.time_spent)
        competition.timer_widget.update_problem_time(state["problem_elapsed"])

        competition.problem_panel.set_exercise(ps.exercise, mode=mgr.mode)
        competition.editor.set_code(ps.code)
        competition.problem_list.set_current(index)
        competition.output_panel.clear()

    def _on_problem_solved(solved_idx: int) -> None:
        """Auto-advance to the next unsolved problem after a successful submit."""
        mgr = state["session_mgr"]
        if mgr is None:
            return
        from pytrainer.models.session import ProblemStatus

        # Find the next unsolved problem after the current one
        n = len(mgr.problems)
        for offset in range(1, n):
            candidate = (solved_idx + offset) % n
            if mgr.problems[candidate].status != ProblemStatus.SOLVED:
                _load_problem(candidate)
                return

    def _start_session(mode: DifficultyMode) -> None:
        """Create a new session and transition to the competition screen."""
        if not exercise_index:
            QMessageBox.warning(
                window,
                "No Exercises",
                f"No exercises found in {exercises_dir}.\n"
                "Please add exercise directories under tier-*/*/problem.yaml.",
            )
            window.show_menu()
            return

        session_config = SessionConfig(mode=mode)
        mgr = SessionManager(session_config, exercise_index)

        if not mgr.problems:
            QMessageBox.warning(window, "No Exercises", "No exercises could be selected.")
            window.show_menu()
            return

        state["session_mgr"] = mgr
        state["score_frozen"] = False
        state["warning_level"] = "normal"

        # Timer controller for per-problem time tracking
        timer_ctrl = TimerController()
        timer_ctrl.start(0)
        state["timer_ctrl"] = timer_ctrl

        # Time limit settings
        ss = settings.session
        time_limit = ss.time_limit_secs
        yellow_threshold = time_limit - ss.warn_yellow_secs
        red_threshold = time_limit - ss.warn_red_secs
        beep_start = time_limit - ss.beep_last_seconds

        # Count-up timer (ticks every second)
        state["session_elapsed"] = 0
        state["problem_elapsed"] = 0
        tick_timer = QTimer()
        tick_timer.setInterval(1000)

        def _tick():
            state["session_elapsed"] += 1
            state["problem_elapsed"] += 1
            elapsed = state["session_elapsed"]
            competition.timer_widget.update_session_time(elapsed)
            competition.timer_widget.update_problem_time(state["problem_elapsed"])

            # Warning thresholds
            if elapsed >= time_limit:
                if state["warning_level"] != "overtime":
                    state["warning_level"] = "overtime"
                    competition.timer_widget.set_session_warning("overtime")
                    # Freeze scoring and show popup
                    state["score_frozen"] = True
                    mins = time_limit // 60
                    QMessageBox.information(
                        window,
                        "Time's Up",
                        f"The {mins}-minute time limit has passed.\n\n"
                        "You can keep practicing, but scores will no longer "
                        "be updated.\n\nClick OK to continue.",
                    )
            elif elapsed >= red_threshold:
                if state["warning_level"] != "red":
                    state["warning_level"] = "red"
                    competition.timer_widget.set_session_warning("red")
            elif elapsed >= yellow_threshold:
                if state["warning_level"] != "yellow":
                    state["warning_level"] = "yellow"
                    competition.timer_widget.set_session_warning("yellow")

            # Beeps in the final seconds before time limit
            if beep_start <= elapsed < time_limit:
                app.beep()

        tick_timer.timeout.connect(_tick)
        tick_timer.start()
        state["tick_timer"] = tick_timer
        competition.timer_widget.update_session_time(0)
        competition.timer_widget.update_problem_time(0)
        competition.timer_widget.set_session_warning("normal")

        # Pipeline and submit flow
        scanner = SafetyScanner()
        pipeline = ExecutionPipeline(scanner)
        state["pipeline"] = pipeline

        submit_flow = SubmitFlowController(
            mgr, competition, pipeline,
            score_frozen_check=lambda: state["score_frozen"],
        )
        state["submit_flow"] = submit_flow

        # Auto-advance on solve
        submit_flow.problem_solved.connect(_on_problem_solved)

        # Populate problem list and load first problem
        competition.problem_list.set_problems(mgr.problems)
        _load_problem(0)

        # Connect problem list navigation
        competition.problem_list.problem_selected.connect(_load_problem)

        # Connect problem status updates to list widget
        mgr.problem_updated.connect(
            lambda idx, ps: competition.problem_list.update_status(idx, ps.status)
        )

        window.show_competition()
        log.info(
            "Session started: mode=%s, problems=%d, time_limit=%ds",
            mode.value,
            len(mgr.problems),
            time_limit,
        )

    def _end_session() -> None:
        """End the current session: stop timers, compute results, show results screen."""
        mgr = state["session_mgr"]
        if mgr is None:
            return

        # Save current editor text
        mgr.current_problem.code = competition.editor.text()

        # Stop tick timer
        tick_timer = state["tick_timer"]
        if tick_timer is not None:
            tick_timer.stop()

        # Finalize per-problem times
        timer_ctrl = state["timer_ctrl"]
        if timer_ctrl is not None:
            timer_ctrl.finalize(mgr.problems)
            mgr.time_used = sum(ps.time_spent for ps in mgr.problems)

        # Get session result
        result = mgr.end()

        # Save to database
        try:
            db.save_session(result)
            log.info("Session %s saved to database", result.session_id)
        except Exception:
            log.exception("Failed to save session")

        # Show results
        results.set_results(result)

        # Analytics
        try:
            analytics = SessionAnalytics(result, db)
            results.set_analytics(
                tier_stats=analytics.tier_performance(),
                recommendations=analytics.recommendations(),
                score_trend=analytics.score_trend(),
            )
        except Exception:
            log.exception("Analytics failed")

        # Disconnect signals to avoid stale connections on next session
        try:
            competition.problem_list.problem_selected.disconnect(_load_problem)
        except TypeError:
            pass

        # Clear session state
        state["session_mgr"] = None
        state["submit_flow"] = None
        state["timer_ctrl"] = None
        state["tick_timer"] = None
        state["pipeline"] = None
        state["score_frozen"] = False
        state["warning_level"] = "normal"

        window.show_results()

    def _show_history() -> None:
        """Populate and show the session history screen."""
        sessions = db.get_sessions()
        history.set_sessions(sessions)
        window.show_history()

    # -- Wire navigation signals -----------------------------------------------
    menu.start_requested.connect(window.show_config)
    menu.history_requested.connect(_show_history)
    config.back_requested.connect(window.show_menu)
    config.mode_selected.connect(_start_session)
    competition.end_session_requested.connect(_end_session)
    results.back_to_menu.connect(window.show_menu)
    history.back_requested.connect(window.show_menu)

    # Start on the main menu
    window.show_menu()
    window.show()

    sys.exit(app.exec())
