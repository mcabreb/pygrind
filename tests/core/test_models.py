"""Tests for E1-S03: Define Core Data Models."""

import tempfile
from pathlib import Path


class TestExerciseModels:
    """AC: models/exercise.py contains Exercise and TestCase dataclasses."""

    def test_testcase_dataclass_exists(self):
        from pytrainer.models.exercise import TestCase

        assert TestCase is not None

    def test_exercise_dataclass_exists(self):
        from pytrainer.models.exercise import Exercise

        assert Exercise is not None

    def test_exercise_index_type_alias(self):
        from pytrainer.models.exercise import ExerciseIndex

        assert ExerciseIndex is not None

    def test_testcase_fields(self):
        from pytrainer.models.exercise import TestCase

        with tempfile.NamedTemporaryFile(mode="w", suffix=".in", delete=False) as f_in:
            f_in.write("hello input")
            in_path = Path(f_in.name)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".out", delete=False) as f_out:
            f_out.write("hello output")
            out_path = Path(f_out.name)

        tc = TestCase(input_path=in_path, output_path=out_path)
        assert tc.input_path == in_path
        assert tc.output_path == out_path

        # Clean up
        in_path.unlink()
        out_path.unlink()

    def test_testcase_lazy_loading(self):
        """AC: TestCase has lazy-loading properties for input_text and expected_output."""
        from pytrainer.models.exercise import TestCase

        with tempfile.NamedTemporaryFile(mode="w", suffix=".in", delete=False) as f_in:
            f_in.write("lazy input")
            in_path = Path(f_in.name)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".out", delete=False) as f_out:
            f_out.write("lazy output")
            out_path = Path(f_out.name)

        tc = TestCase(input_path=in_path, output_path=out_path)
        # Not loaded yet
        assert tc._input_text is None
        assert tc._expected_output is None
        # Lazy load on access
        assert tc.input_text == "lazy input"
        assert tc.expected_output == "lazy output"
        # Cached after first access
        assert tc._input_text == "lazy input"
        assert tc._expected_output == "lazy output"

        in_path.unlink()
        out_path.unlink()

    def test_exercise_all_fields(self):
        from pytrainer.models.exercise import Exercise

        ex = Exercise(
            id="test-001",
            title="Test Exercise",
            tier=1,
            topic="basics",
            description="A test exercise",
            time_estimate=5,
            test_cases=[],
            hint="Try harder",
            solution="print('hello')",
            source="original",
            validation="exact",
            tolerance=1e-6,
        )
        assert ex.id == "test-001"
        assert ex.title == "Test Exercise"
        assert ex.tier == 1
        assert ex.topic == "basics"
        assert ex.description == "A test exercise"
        assert ex.time_estimate == 5
        assert ex.test_cases == []
        assert ex.hint == "Try harder"
        assert ex.solution == "print('hello')"
        assert ex.source == "original"
        assert ex.validation == "exact"
        assert ex.tolerance == 1e-6

    def test_exercise_defaults(self):
        from pytrainer.models.exercise import Exercise

        ex = Exercise(
            id="test-002",
            title="Defaults",
            tier=2,
            topic="basics",
            description="Testing defaults",
            time_estimate=3,
            test_cases=[],
        )
        assert ex.hint is None
        assert ex.solution is None
        assert ex.source == "original"
        assert ex.validation == "exact"
        assert ex.tolerance == 1e-6

    def test_exercise_index_is_dict_type(self):
        from pytrainer.models.exercise import ExerciseIndex

        # Verify it's the expected type alias
        assert ExerciseIndex is not None


class TestSessionModels:
    """AC: models/session.py contains session dataclasses and enums."""

    def test_problem_status_enum(self):
        """AC: ProblemStatus enum has UNSOLVED, ATTEMPTED, SOLVED values."""
        from pytrainer.models.session import ProblemStatus

        assert ProblemStatus.UNSOLVED.value == "unsolved"
        assert ProblemStatus.ATTEMPTED.value == "attempted"
        assert ProblemStatus.SOLVED.value == "solved"

    def test_difficulty_mode_enum(self):
        """AC: DifficultyMode enum has BEGINNER, MEDIUM, DIFFICULT values."""
        from pytrainer.models.session import DifficultyMode

        assert DifficultyMode.BEGINNER.value == "beginner"
        assert DifficultyMode.MEDIUM.value == "medium"
        assert DifficultyMode.DIFFICULT.value == "difficult"

    def test_problem_state_dataclass(self):
        """AC: models/session.py contains ProblemState dataclass."""
        from pytrainer.models.exercise import Exercise
        from pytrainer.models.session import ProblemState, ProblemStatus

        ex = Exercise(
            id="ps-test",
            title="Test",
            tier=1,
            topic="test",
            description="test",
            time_estimate=5,
            test_cases=[],
        )
        ps = ProblemState(exercise=ex)
        assert ps.exercise is ex
        assert ps.code == ""
        assert ps.status == ProblemStatus.UNSOLVED
        assert ps.attempts == 0
        assert ps.time_spent == 0.0
        assert ps.score == 0
        assert ps.hint_viewed is False
        assert ps.solution_viewed is False

    def test_problem_state_mutable(self):
        from pytrainer.models.exercise import Exercise
        from pytrainer.models.session import ProblemState, ProblemStatus

        ex = Exercise(
            id="mut-test",
            title="Mutable",
            tier=1,
            topic="test",
            description="test",
            time_estimate=5,
            test_cases=[],
        )
        ps = ProblemState(exercise=ex)
        ps.status = ProblemStatus.ATTEMPTED
        ps.attempts = 3
        ps.code = "print('hi')"
        assert ps.status == ProblemStatus.ATTEMPTED
        assert ps.attempts == 3
        assert ps.code == "print('hi')"

    def test_session_config_dataclass(self):
        """AC: models/session.py contains SessionConfig dataclass."""
        from pytrainer.models.session import DifficultyMode, SessionConfig

        sc = SessionConfig(mode=DifficultyMode.BEGINNER)
        assert sc.mode == DifficultyMode.BEGINNER
        assert sc.total_time == 10800
        assert sc.tier_distribution == {1: 8, 2: 8, 3: 6, 4: 5, 5: 3}

    def test_session_config_default_factory_independence(self):
        from pytrainer.models.session import DifficultyMode, SessionConfig

        sc1 = SessionConfig(mode=DifficultyMode.BEGINNER)
        sc2 = SessionConfig(mode=DifficultyMode.MEDIUM)
        sc1.tier_distribution[1] = 99
        assert sc2.tier_distribution[1] == 8  # not shared

    def test_session_result_dataclass(self):
        """AC: models/session.py contains SessionResult dataclass."""
        from pytrainer.models.session import DifficultyMode, SessionConfig, SessionResult

        config = SessionConfig(mode=DifficultyMode.BEGINNER)
        sr = SessionResult(
            session_id="test-session-1",
            date="2026-03-01T12:00:00",
            config=config,
            problems=[],
            total_score=100,
        )
        assert sr.session_id == "test-session-1"
        assert sr.max_score == 925
        assert sr.time_used == 0.0
        assert sr.time_paused == 0.0


class TestModelsImportable:
    """AC: All models are importable from pytrainer.models."""

    def test_import_exercise(self):
        from pytrainer.models import Exercise  # noqa: F401

    def test_import_testcase(self):
        from pytrainer.models import TestCase  # noqa: F401

    def test_import_exercise_index(self):
        from pytrainer.models import ExerciseIndex  # noqa: F401

    def test_import_problem_status(self):
        from pytrainer.models import ProblemStatus  # noqa: F401

    def test_import_difficulty_mode(self):
        from pytrainer.models import DifficultyMode  # noqa: F401

    def test_import_problem_state(self):
        from pytrainer.models import ProblemState  # noqa: F401

    def test_import_session_config(self):
        from pytrainer.models import SessionConfig  # noqa: F401

    def test_import_session_result(self):
        from pytrainer.models import SessionResult  # noqa: F401
