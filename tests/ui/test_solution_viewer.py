"""Tests for E7-S02: Solution Viewer."""

import pytest
from PyQt6.QtWidgets import QApplication

from pytrainer.models.exercise import Exercise
from pytrainer.models.session import DifficultyMode
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
def exercise_with_solution():
    return Exercise(
        id="test-sol",
        title="With Solution",
        tier=1,
        topic="basics",
        description="Solve.",
        time_estimate=5,
        test_cases=[],
        solution="print('hello')",
    )


@pytest.fixture
def exercise_no_solution():
    return Exercise(
        id="test-no-sol",
        title="No Solution",
        tier=2,
        topic="strings",
        description="Figure it out.",
        time_estimate=5,
        test_cases=[],
        solution=None,
    )


class TestSolutionButtonVisibility:
    """AC: Show Solution button visible only in Beginner mode."""

    def test_visible_in_beginner(self, panel, exercise_with_solution):
        panel.set_exercise(exercise_with_solution, mode=DifficultyMode.BEGINNER)
        assert panel._solution_button.isVisible()

    def test_hidden_in_medium(self, panel, exercise_with_solution):
        panel.set_exercise(exercise_with_solution, mode=DifficultyMode.MEDIUM)
        assert not panel._solution_button.isVisible()

    def test_hidden_in_difficult(self, panel, exercise_with_solution):
        panel.set_exercise(exercise_with_solution, mode=DifficultyMode.DIFFICULT)
        assert not panel._solution_button.isVisible()


class TestNoSolutionHandling:
    """AC: If exercise has no solution defined, button disabled with tooltip."""

    def test_button_disabled_when_no_solution(self, panel, exercise_no_solution):
        panel.set_exercise(exercise_no_solution, mode=DifficultyMode.BEGINNER)
        assert not panel._solution_button.isEnabled()
        assert "No solution available" in panel._solution_button.toolTip()

    def test_button_enabled_when_solution_exists(self, panel, exercise_with_solution):
        panel.set_exercise(exercise_with_solution, mode=DifficultyMode.BEGINNER)
        assert panel._solution_button.isEnabled()


class TestSolutionViewedSignal:
    """AC: ProblemState.solution_viewed set to True, score forced to 0."""

    def test_solution_viewed_signal_emitted(self, panel, exercise_with_solution):
        panel.set_exercise(exercise_with_solution, mode=DifficultyMode.BEGINNER)
        received = []
        panel.solution_viewed.connect(lambda: received.append(True))
        # Simulate confirmation by calling internal reveal directly
        panel._reveal_solution()
        assert len(received) == 1

    def test_solution_panel_shown_after_reveal(self, panel, exercise_with_solution):
        panel.set_exercise(exercise_with_solution, mode=DifficultyMode.BEGINNER)
        panel._reveal_solution()
        assert panel._solution_label.isVisible()
        assert panel._solution_label.text() == "print('hello')"

    def test_solution_button_disabled_after_reveal(self, panel, exercise_with_solution):
        panel.set_exercise(exercise_with_solution, mode=DifficultyMode.BEGINNER)
        panel._reveal_solution()
        assert not panel._solution_button.isEnabled()
