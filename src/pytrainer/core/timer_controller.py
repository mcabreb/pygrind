"""Per-problem time tracking controller."""

from __future__ import annotations

import time

from pytrainer.models.session import ProblemState


class TimerController:
    """Tracks cumulative time per problem index using monotonic clock."""

    def __init__(self) -> None:
        self._problem_times: dict[int, float] = {}
        self._current_problem: int | None = None
        self._last_switch: float = 0.0
        self._running = False

    @property
    def problem_times(self) -> dict[int, float]:
        return dict(self._problem_times)

    def start(self, problem_index: int) -> None:
        """Start tracking time for the given problem."""
        self._current_problem = problem_index
        self._last_switch = time.monotonic()
        self._running = True

    def switch_problem(self, new_index: int) -> None:
        """Accumulate elapsed time to current problem and switch to new one."""
        if self._running and self._current_problem is not None:
            elapsed = time.monotonic() - self._last_switch
            self._problem_times[self._current_problem] = (
                self._problem_times.get(self._current_problem, 0.0) + elapsed
            )
        self._current_problem = new_index
        self._last_switch = time.monotonic()

    def stop(self) -> None:
        """Stop tracking and accumulate final elapsed time."""
        if self._running and self._current_problem is not None:
            elapsed = time.monotonic() - self._last_switch
            self._problem_times[self._current_problem] = (
                self._problem_times.get(self._current_problem, 0.0) + elapsed
            )
        self._running = False

    def elapsed_for_current(self) -> float:
        """Return elapsed seconds for the current problem (including accumulated)."""
        if not self._running or self._current_problem is None:
            return 0.0
        accumulated = self._problem_times.get(self._current_problem, 0.0)
        return accumulated + (time.monotonic() - self._last_switch)

    def finalize(self, problems: list[ProblemState]) -> None:
        """Write accumulated times to ProblemState.time_spent."""
        if self._running:
            self.stop()
        for idx, ps in enumerate(problems):
            ps.time_spent = self._problem_times.get(idx, 0.0)
