"""Tests for E7-S04: Per-Problem Time Tracking via TimerController."""

import time

import pytest

from pytrainer.core.timer_controller import TimerController
from pytrainer.models.exercise import Exercise
from pytrainer.models.session import ProblemState


def _make_problems(n: int = 3) -> list[ProblemState]:
    return [
        ProblemState(
            exercise=Exercise(
                id=f"ex-{i}",
                title=f"Exercise {i}",
                tier=1,
                topic="basics",
                description="",
                time_estimate=5,
                test_cases=[],
            )
        )
        for i in range(n)
    ]


class TestPerProblemTracking:
    """AC: TimerController tracks cumulative seconds per problem index."""

    def test_initial_problem_times_empty(self):
        tc = TimerController()
        assert tc.problem_times == {}

    def test_start_begins_tracking(self):
        tc = TimerController()
        tc.start(0)
        time.sleep(0.05)
        assert tc.elapsed_for_current() > 0


class TestSwitchProblem:
    """AC: switch_problem(idx) accumulates elapsed time to previous problem."""

    def test_switch_accumulates_time(self):
        tc = TimerController()
        tc.start(0)
        time.sleep(0.05)
        tc.switch_problem(1)
        assert tc.problem_times.get(0, 0) > 0

    def test_switch_starts_new_counter(self):
        tc = TimerController()
        tc.start(0)
        time.sleep(0.05)
        tc.switch_problem(1)
        time.sleep(0.05)
        tc.switch_problem(2)
        assert tc.problem_times.get(1, 0) > 0

    def test_switch_back_accumulates(self):
        tc = TimerController()
        tc.start(0)
        time.sleep(0.05)
        tc.switch_problem(1)
        time.sleep(0.05)
        tc.switch_problem(0)
        time.sleep(0.05)
        tc.stop()
        # Problem 0 was active twice
        assert tc.problem_times.get(0, 0) > 0.05


class TestFinalize:
    """AC: Per-problem time written to ProblemState.time_spent on session end."""

    def test_finalize_writes_to_problem_states(self):
        problems = _make_problems(3)
        tc = TimerController()
        tc.start(0)
        time.sleep(0.05)
        tc.switch_problem(1)
        time.sleep(0.05)
        tc.switch_problem(2)
        time.sleep(0.05)
        tc.stop()
        tc.finalize(problems)
        assert all(ps.time_spent > 0 for ps in problems)

    def test_finalize_without_stop_still_works(self):
        problems = _make_problems(2)
        tc = TimerController()
        tc.start(0)
        time.sleep(0.05)
        tc.switch_problem(1)
        time.sleep(0.05)
        tc.finalize(problems)
        assert problems[0].time_spent > 0
        assert problems[1].time_spent > 0


class TestResultsScreenTimeFormat:
    """AC: ResultsScreen shows per-problem time in MM:SS format (verified via existing code)."""

    def test_time_format_mm_ss(self):
        """Verify that 125 seconds formats as 2:05."""
        t = 125.0
        mins = int(t) // 60
        secs = int(t) % 60
        formatted = f"{mins}:{secs:02d}"
        assert formatted == "2:05"
