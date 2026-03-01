"""Tests for E7-S01: Hints System."""

import pytest
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton

from pytrainer.models.exercise import Exercise, TestCase
from pytrainer.models.session import DifficultyMode
from pytrainer.ui.problem import ProblemPanel


@pytest.fixture(scope="module")
def _qapp():
    """Ensure a QApplication exists for widget tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def panel(_qapp):
    """Create a fresh ProblemPanel for each test."""
    p = ProblemPanel()
    p.show()
    return p


@pytest.fixture
def exercise_with_hint():
    """Exercise that has a hint."""
    return Exercise(
        id="test-hint",
        title="Test Hint",
        tier=1,
        topic="basics",
        description="Solve this.",
        time_estimate=5,
        test_cases=[],
        hint="Use a loop",
    )


@pytest.fixture
def exercise_no_hint():
    """Exercise without a hint."""
    return Exercise(
        id="test-no-hint",
        title="No Hint",
        tier=2,
        topic="strings",
        description="Figure it out.",
        time_estimate=5,
        test_cases=[],
        hint=None,
    )


class TestBeginnerMode:
    """AC: Beginner mode — hint text shown automatically below problem description."""

    def test_hint_label_visible_in_beginner(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.BEGINNER)
        assert panel._hint_label.isVisible()
        assert panel._hint_label.text() == "Use a loop"

    def test_hint_button_hidden_in_beginner(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.BEGINNER)
        assert not panel._hint_button.isVisible()

    def test_no_hint_shows_fallback_in_beginner(self, panel, exercise_no_hint):
        panel.set_exercise(exercise_no_hint, mode=DifficultyMode.BEGINNER)
        assert panel._hint_label.isVisible()
        assert panel._hint_label.text() == "No hint available"


class TestMediumMode:
    """AC: Medium mode — Show Hint button visible, clicking reveals hint (one-way)."""

    def test_hint_button_visible_in_medium(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.MEDIUM)
        assert panel._hint_button.isVisible()
        assert not panel._hint_label.isVisible()

    def test_clicking_button_reveals_hint(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.MEDIUM)
        panel._hint_button.click()
        assert panel._hint_label.isVisible()
        assert panel._hint_label.text() == "Use a loop"

    def test_button_disabled_after_click(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.MEDIUM)
        panel._hint_button.click()
        assert not panel._hint_button.isEnabled()

    def test_no_hint_shows_fallback_on_click(self, panel, exercise_no_hint):
        panel.set_exercise(exercise_no_hint, mode=DifficultyMode.MEDIUM)
        panel._hint_button.click()
        assert panel._hint_label.text() == "No hint available"


class TestDifficultMode:
    """AC: Difficult mode — no hint button or text visible."""

    def test_hint_label_hidden_in_difficult(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.DIFFICULT)
        assert not panel._hint_label.isVisible()

    def test_hint_button_hidden_in_difficult(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.DIFFICULT)
        assert not panel._hint_button.isVisible()


class TestHintViewedTracking:
    """AC: ProblemState.hint_viewed tracked when hint is revealed."""

    def test_hint_viewed_signal_emitted_on_medium_click(self, panel, exercise_with_hint):
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.MEDIUM)
        received = []
        panel.hint_viewed.connect(lambda: received.append(True))
        panel._hint_button.click()
        assert len(received) == 1

    def test_hint_viewed_signal_emitted_in_beginner(self, panel, exercise_with_hint):
        received = []
        panel.hint_viewed.connect(lambda: received.append(True))
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.BEGINNER)
        assert len(received) == 1

    def test_hint_viewed_signal_not_emitted_in_difficult(self, panel, exercise_with_hint):
        received = []
        panel.hint_viewed.connect(lambda: received.append(True))
        panel.set_exercise(exercise_with_hint, mode=DifficultyMode.DIFFICULT)
        assert len(received) == 0
