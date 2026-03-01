"""Tests for E7-S07: Exercise Flagging."""

import pytest
from PyQt6.QtWidgets import QApplication

from pytrainer.models.exercise import Exercise
from pytrainer.models.session import DifficultyMode
from pytrainer.storage.database import Database
from pytrainer.ui.problem import ProblemPanel


@pytest.fixture(scope="module")
def _qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def panel(_qapp):
    p = ProblemPanel()
    p.show()
    return p


@pytest.fixture
def exercise():
    return Exercise(
        id="flag-test",
        title="Flag Test",
        tier=1,
        topic="basics",
        description="Test flagging.",
        time_estimate=5,
        test_cases=[],
    )


@pytest.fixture
def db(tmp_path):
    return Database(tmp_path / "test.db")


class TestFlagButtonVisibility:
    """AC: Flag Problem button visible on each problem in competition view."""

    def test_flag_button_visible_in_beginner(self, panel, exercise):
        panel.set_exercise(exercise, mode=DifficultyMode.BEGINNER)
        assert panel._flag_button.isVisible()

    def test_flag_button_visible_in_medium(self, panel, exercise):
        panel.set_exercise(exercise, mode=DifficultyMode.MEDIUM)
        assert panel._flag_button.isVisible()

    def test_flag_button_visible_in_difficult(self, panel, exercise):
        panel.set_exercise(exercise, mode=DifficultyMode.DIFFICULT)
        assert panel._flag_button.isVisible()

    def test_flag_button_hidden_when_no_mode(self, panel, exercise):
        """Flag button not shown when mode is None (backward compat)."""
        panel.set_exercise(exercise)
        assert not panel._flag_button.isVisible()


class TestFlagSignal:
    """AC: Clicking flag button emits a signal for the controller to handle."""

    def test_flag_requested_signal_emitted(self, panel, exercise):
        panel.set_exercise(exercise, mode=DifficultyMode.BEGINNER)
        received = []
        panel.flag_requested.connect(lambda: received.append(True))
        panel._flag_button.click()
        assert len(received) == 1


class TestFlagStorage:
    """AC: Flag stored in SQLite; duplicates prevented."""

    def test_save_flag_stores_in_db(self, db):
        db.save_flag("ex-1", "sess-1", "Bad test case")
        flags = db.get_flags()
        assert len(flags) == 1
        assert flags[0]["exercise_id"] == "ex-1"
        assert flags[0]["comment"] == "Bad test case"

    def test_duplicate_flag_prevented(self, db):
        db.save_flag("ex-1", "sess-1", "First")
        result = db.save_flag("ex-1", "sess-1", "Duplicate")
        assert result is False
        flags = db.get_flags()
        assert len(flags) == 1

    def test_flag_with_no_comment(self, db):
        db.save_flag("ex-2", "sess-1", None)
        flags = db.get_flags()
        assert flags[0]["comment"] is None


class TestFlagSummaryScreen:
    """AC: Flagged Exercises summary accessible from main menu."""

    def test_main_menu_has_flags_button(self, _qapp):
        from pytrainer.ui.main_menu import MainMenuScreen

        menu = MainMenuScreen()
        menu.show()
        assert hasattr(menu, "flags_requested")
        assert hasattr(menu, "_flags_button")
        assert menu._flags_button.isVisible()

    def test_flags_signal_emitted(self, _qapp):
        from pytrainer.ui.main_menu import MainMenuScreen

        menu = MainMenuScreen()
        menu.show()
        received = []
        menu.flags_requested.connect(lambda: received.append(True))
        menu._flags_button.click()
        assert len(received) == 1
