"""Tests for E7-S03: Problem Navigation Sidebar."""

import pytest
from PyQt6.QtWidgets import QApplication

from pytrainer.models.exercise import Exercise
from pytrainer.models.session import ProblemState, ProblemStatus
from pytrainer.ui.problem_list import ProblemListWidget


@pytest.fixture(scope="module")
def _qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def _make_problems(n: int = 5) -> list[ProblemState]:
    problems = []
    for i in range(n):
        ex = Exercise(
            id=f"ex-{i}",
            title=f"Exercise Number {i}" if i < 3 else f"A Very Long Title That Exceeds Twenty Characters {i}",
            tier=(i % 5) + 1,
            topic="basics",
            description=f"Desc {i}",
            time_estimate=5,
            test_cases=[],
        )
        problems.append(ProblemState(exercise=ex))
    return problems


@pytest.fixture
def widget(_qapp):
    w = ProblemListWidget()
    w.show()
    return w


@pytest.fixture
def problems():
    return _make_problems(5)


class TestSidebarDisplay:
    """AC: Sidebar shows all problems with number, abbreviated title, status icon."""

    def test_list_count_matches_problems(self, widget, problems):
        widget.set_problems(problems)
        assert widget._list.count() == 5

    def test_item_text_contains_number(self, widget, problems):
        widget.set_problems(problems)
        text = widget._list.item(0).text()
        assert "1." in text

    def test_long_title_truncated(self, widget, problems):
        widget.set_problems(problems)
        text = widget._list.item(3).text()
        assert "..." in text


class TestStatusIcons:
    """AC: Status icons for unsolved, attempted, solved."""

    def test_unsolved_icon(self, widget, problems):
        widget.set_problems(problems)
        text = widget._list.item(0).text()
        assert "⚪" in text  # grey circle

    def test_attempted_icon(self, widget, problems):
        problems[1].status = ProblemStatus.ATTEMPTED
        widget.set_problems(problems)
        text = widget._list.item(1).text()
        assert "🔶" in text  # yellow/orange diamond

    def test_solved_icon(self, widget, problems):
        problems[2].status = ProblemStatus.SOLVED
        widget.set_problems(problems)
        text = widget._list.item(2).text()
        assert "✅" in text  # green checkmark


class TestClickNavigation:
    """AC: Clicking a problem emits problem_selected signal."""

    def test_signal_emitted_on_click(self, widget, problems):
        widget.set_problems(problems)
        received = []
        widget.problem_selected.connect(lambda idx: received.append(idx))
        widget._list.setCurrentRow(2)
        assert received == [2]


class TestNextPrevButtons:
    """AC: Next/Previous buttons at top of sidebar."""

    def test_next_button_increments(self, widget, problems):
        widget.set_problems(problems)
        widget._list.setCurrentRow(0)
        received = []
        widget.problem_selected.connect(lambda idx: received.append(idx))
        widget._next_button.click()
        assert received[-1] == 1

    def test_prev_button_decrements(self, widget, problems):
        widget.set_problems(problems)
        widget._list.setCurrentRow(2)
        received = []
        widget.problem_selected.connect(lambda idx: received.append(idx))
        widget._prev_button.click()
        assert received[-1] == 1

    def test_next_at_end_stays(self, widget, problems):
        widget.set_problems(problems)
        widget._list.setCurrentRow(4)
        received = []
        widget.problem_selected.connect(lambda idx: received.append(idx))
        widget._next_button.click()
        assert widget._list.currentRow() == 4

    def test_prev_at_start_stays(self, widget, problems):
        widget.set_problems(problems)
        widget._list.setCurrentRow(0)
        received = []
        widget.problem_selected.connect(lambda idx: received.append(idx))
        widget._prev_button.click()
        assert widget._list.currentRow() == 0


class TestCurrentHighlight:
    """AC: Current problem highlighted with distinct background."""

    def test_set_current_updates_selection(self, widget, problems):
        widget.set_problems(problems)
        widget.set_current(3)
        assert widget._list.currentRow() == 3


class TestStatusUpdate:
    """AC: Status can be updated individually."""

    def test_update_status_changes_icon(self, widget, problems):
        widget.set_problems(problems)
        widget.update_status(0, ProblemStatus.SOLVED)
        text = widget._list.item(0).text()
        assert "✅" in text
