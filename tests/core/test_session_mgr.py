"""Tests for SessionManager — E5-S01 acceptance criteria."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from pytrainer.core.session_mgr import SessionManager
from pytrainer.models.exercise import Exercise, ExerciseIndex, TestCase
from pytrainer.models.session import (
    DifficultyMode,
    ProblemState,
    ProblemStatus,
    SessionConfig,
    SessionResult,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def exercise_index() -> ExerciseIndex:
    """Build a minimal ExerciseIndex with enough exercises per tier."""
    idx: ExerciseIndex = {}
    for tier in range(1, 6):
        exercises = []
        for i in range(10):
            ex = Exercise(
                id=f"t{tier}-{i:02d}",
                title=f"Tier {tier} Exercise {i}",
                tier=tier,
                topic="general",
                description=f"Desc for t{tier}-{i:02d}",
                time_estimate=5,
                test_cases=[
                    TestCase(
                        input_path=Path(f"/fake/t{tier}-{i:02d}/01.in"),
                        output_path=Path(f"/fake/t{tier}-{i:02d}/01.out"),
                    )
                ],
            )
            exercises.append(ex)
        idx[tier] = exercises
    return idx


@pytest.fixture
def session_config() -> SessionConfig:
    return SessionConfig(mode=DifficultyMode.BEGINNER)


@pytest.fixture
def session_mgr(session_config, exercise_index, qapp):
    """Create a SessionManager with default config."""
    return SessionManager(session_config, exercise_index)


# ---------------------------------------------------------------------------
# AC-1: Constructor takes SessionConfig + ExerciseIndex, calls selection
# ---------------------------------------------------------------------------


class TestConstructor:
    def test_constructor_calls_selection(self, session_config, exercise_index, qapp):
        """AC-1: Constructor calls select_session() for 30 exercises."""
        with patch("pytrainer.core.session_mgr.select_session") as mock_select:
            mock_select.return_value = exercise_index[1][:8]  # return something
            SessionManager(session_config, exercise_index)
            mock_select.assert_called_once()

    def test_constructor_stores_config(self, session_mgr):
        """AC-1: SessionManager stores config."""
        assert session_mgr.config.mode == DifficultyMode.BEGINNER


# ---------------------------------------------------------------------------
# AC-2: Initializes 30 ProblemState objects linked to selected exercises
# ---------------------------------------------------------------------------


class TestProblemStates:
    def test_problems_are_problem_state_objects(self, session_mgr):
        """AC-2: problems is a list of ProblemState."""
        assert all(isinstance(p, ProblemState) for p in session_mgr.problems)

    def test_problems_linked_to_exercises(self, session_mgr):
        """AC-2: Each ProblemState references an Exercise."""
        for ps in session_mgr.problems:
            assert isinstance(ps.exercise, Exercise)

    def test_problems_start_unsolved(self, session_mgr):
        """AC-2: All ProblemState start as UNSOLVED."""
        for ps in session_mgr.problems:
            assert ps.status == ProblemStatus.UNSOLVED


# ---------------------------------------------------------------------------
# AC-3: Tracks current_problem_index, mode, and running score
# ---------------------------------------------------------------------------


class TestTracking:
    def test_current_problem_index_default(self, session_mgr):
        """AC-3: current_problem_index starts at 0."""
        assert session_mgr.current_problem_index == 0

    def test_mode_from_config(self, session_mgr):
        """AC-3: mode reflects the config."""
        assert session_mgr.mode == DifficultyMode.BEGINNER

    def test_total_score_starts_zero(self, session_mgr):
        """AC-3: total_score starts at 0."""
        assert session_mgr.total_score == 0

    def test_current_problem_returns_problem_state(self, session_mgr):
        """AC-3: current_problem returns the current ProblemState."""
        cp = session_mgr.current_problem
        assert isinstance(cp, ProblemState)
        assert cp is session_mgr.problems[0]


# ---------------------------------------------------------------------------
# AC-4: State transitions: unsolved→attempted on wrong, attempted→solved on correct
# ---------------------------------------------------------------------------


class TestStateTransitions:
    def test_wrong_submit_marks_attempted(self, session_mgr):
        """AC-4: unsolved→attempted on wrong submission."""
        idx = session_mgr.current_problem_index
        session_mgr.record_attempt(idx, passed=False, score=0)
        assert session_mgr.problems[idx].status == ProblemStatus.ATTEMPTED
        assert session_mgr.problems[idx].attempts == 1

    def test_correct_submit_marks_solved(self, session_mgr):
        """AC-4: attempted→solved on correct submission."""
        idx = session_mgr.current_problem_index
        session_mgr.record_attempt(idx, passed=False, score=0)
        assert session_mgr.problems[idx].status == ProblemStatus.ATTEMPTED
        session_mgr.record_attempt(idx, passed=True, score=10)
        assert session_mgr.problems[idx].status == ProblemStatus.SOLVED
        assert session_mgr.problems[idx].score == 10

    def test_direct_solve_from_unsolved(self, session_mgr):
        """AC-4: unsolved→solved on first correct submission."""
        idx = session_mgr.current_problem_index
        session_mgr.record_attempt(idx, passed=True, score=10)
        assert session_mgr.problems[idx].status == ProblemStatus.SOLVED

    def test_total_score_updated(self, session_mgr):
        """AC-4: total_score updates on correct submission."""
        session_mgr.record_attempt(0, passed=True, score=10)
        session_mgr.record_attempt(1, passed=True, score=20)
        assert session_mgr.total_score == 30

    def test_problem_updated_signal_emitted(self, session_mgr, qtbot):
        """AC-4: problem_updated signal emitted on state change."""
        with qtbot.waitSignal(session_mgr.problem_updated, timeout=1000):
            session_mgr.record_attempt(0, passed=False, score=0)


# ---------------------------------------------------------------------------
# AC-5: to_json() serializes full session state
# ---------------------------------------------------------------------------


class TestToJson:
    def test_to_json_returns_valid_json(self, session_mgr):
        """AC-5: to_json() returns a parseable JSON string."""
        data = session_mgr.to_json()
        parsed = json.loads(data)
        assert isinstance(parsed, dict)

    def test_to_json_contains_config(self, session_mgr):
        """AC-5: JSON includes session config."""
        data = json.loads(session_mgr.to_json())
        assert "config" in data
        assert data["config"]["mode"] == "beginner"

    def test_to_json_contains_problems(self, session_mgr):
        """AC-5: JSON includes problem states with exercise IDs."""
        data = json.loads(session_mgr.to_json())
        assert "problems" in data
        assert len(data["problems"]) == len(session_mgr.problems)
        # Exercise stored as ID, not full object
        for p in data["problems"]:
            assert "exercise_id" in p

    def test_to_json_contains_score_and_index(self, session_mgr):
        """AC-5: JSON includes score and current index."""
        data = json.loads(session_mgr.to_json())
        assert "total_score" in data
        assert "current_problem_index" in data

    def test_to_json_preserves_code(self, session_mgr):
        """AC-5: JSON includes user code per problem."""
        session_mgr.problems[0].code = "print('hello')"
        data = json.loads(session_mgr.to_json())
        assert data["problems"][0]["code"] == "print('hello')"


# ---------------------------------------------------------------------------
# AC-6: from_json() restores session from serialized state
# ---------------------------------------------------------------------------


class TestFromJson:
    def test_from_json_roundtrip(self, session_mgr, exercise_index):
        """AC-6: from_json(to_json()) restores equivalent state."""
        session_mgr.problems[0].code = "x = 1"
        session_mgr.record_attempt(0, passed=True, score=10)
        json_str = session_mgr.to_json()

        restored = SessionManager.from_json(json_str, exercise_index)
        assert restored.total_score == session_mgr.total_score
        assert restored.current_problem_index == session_mgr.current_problem_index
        assert restored.problems[0].code == "x = 1"
        assert restored.problems[0].status == ProblemStatus.SOLVED
        assert restored.problems[0].score == 10

    def test_from_json_resolves_exercise_ids(self, session_mgr, exercise_index):
        """AC-6: Restores exercise references from IDs."""
        json_str = session_mgr.to_json()
        restored = SessionManager.from_json(json_str, exercise_index)
        for ps in restored.problems:
            assert isinstance(ps.exercise, Exercise)

    def test_from_json_preserves_mode(self, session_mgr, exercise_index):
        """AC-6: Restores session mode."""
        json_str = session_mgr.to_json()
        restored = SessionManager.from_json(json_str, exercise_index)
        assert restored.mode == DifficultyMode.BEGINNER


# ---------------------------------------------------------------------------
# AC-7: end() calculates and returns final SessionResult
# ---------------------------------------------------------------------------


class TestEnd:
    def test_end_returns_session_result(self, session_mgr):
        """AC-7: end() returns a SessionResult."""
        result = session_mgr.end()
        assert isinstance(result, SessionResult)

    def test_end_includes_total_score(self, session_mgr):
        """AC-7: SessionResult has total_score."""
        session_mgr.record_attempt(0, passed=True, score=10)
        result = session_mgr.end()
        assert result.total_score == 10

    def test_end_includes_all_problems(self, session_mgr):
        """AC-7: SessionResult includes all problem states."""
        result = session_mgr.end()
        assert len(result.problems) == len(session_mgr.problems)

    def test_end_includes_config(self, session_mgr):
        """AC-7: SessionResult includes config."""
        result = session_mgr.end()
        assert result.config.mode == DifficultyMode.BEGINNER
