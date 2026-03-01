"""Tests for E2-S01: Exercise Loader — YAML Discovery & Parsing."""

import logging
from pathlib import Path

from pytrainer.core.loader import ExerciseLoader
from pytrainer.models.exercise import Exercise

FIXTURES_DIR = Path(__file__).parents[1] / "fixtures" / "exercises"


class TestExerciseDiscovery:
    """AC: Discovers exercises in tier-{1..5}-*/ directories recursively."""

    def test_discovers_all_fixture_exercises(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        # Fixtures have 5 tiers, 1 exercise each
        total = sum(len(exs) for exs in index.values())
        assert total == 5

    def test_discovers_exercises_per_tier(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        for tier in range(1, 6):
            assert tier in index
            assert len(index[tier]) >= 1


class TestYamlParsing:
    """AC: Parses problem.yaml using PyYAML and maps to Exercise dataclass."""

    def test_parsed_exercise_is_exercise_type(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        ex = index[1][0]
        assert isinstance(ex, Exercise)

    def test_parsed_exercise_has_correct_fields(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        ex = index[1][0]
        assert ex.id == "tier1-sum-two"
        assert ex.title == "Sum of Two Numbers"
        assert ex.tier == 1
        assert ex.topic == "arithmetic"
        assert ex.description == "Read two integers from input and print their sum."
        assert ex.time_estimate == 3

    def test_parsed_exercise_optional_fields(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        ex = index[1][0]
        assert ex.hint is not None
        assert ex.solution is not None
        assert ex.validation == "exact"


class TestFieldValidation:
    """AC: Validates required fields — skips invalid with log warning."""

    def test_missing_required_field_skips_exercise(self, tmp_path):
        """Exercise with missing 'title' field should be skipped."""
        tier_dir = tmp_path / "tier-1-test"
        ex_dir = tier_dir / "bad-exercise"
        tests_dir = ex_dir / "tests"
        tests_dir.mkdir(parents=True)
        (ex_dir / "problem.yaml").write_text(
            "id: bad\ntier: 1\ntopic: test\ndescription: test\ntime_estimate: 5\n"
        )
        (tests_dir / "01.in").write_text("1")
        (tests_dir / "01.out").write_text("1")

        loader = ExerciseLoader(tmp_path)
        index = loader.load_all()
        total = sum(len(exs) for exs in index.values())
        assert total == 0

    def test_missing_field_logs_warning(self, tmp_path, caplog):
        """Missing field should produce a log warning."""
        tier_dir = tmp_path / "tier-1-test"
        ex_dir = tier_dir / "bad-exercise"
        tests_dir = ex_dir / "tests"
        tests_dir.mkdir(parents=True)
        (ex_dir / "problem.yaml").write_text(
            "id: bad\ntier: 1\ntopic: test\ndescription: test\ntime_estimate: 5\n"
        )
        (tests_dir / "01.in").write_text("1")
        (tests_dir / "01.out").write_text("1")

        loader = ExerciseLoader(tmp_path)
        with caplog.at_level(logging.WARNING):
            loader.load_all()
        assert any("title" in record.message for record in caplog.records)

    def test_invalid_yaml_skips_exercise(self, tmp_path, caplog):
        """Unparseable YAML should be skipped with warning."""
        tier_dir = tmp_path / "tier-1-test"
        ex_dir = tier_dir / "broken-yaml"
        tests_dir = ex_dir / "tests"
        tests_dir.mkdir(parents=True)
        (ex_dir / "problem.yaml").write_text(": : : [invalid yaml{{{")
        (tests_dir / "01.in").write_text("1")
        (tests_dir / "01.out").write_text("1")

        loader = ExerciseLoader(tmp_path)
        with caplog.at_level(logging.WARNING):
            index = loader.load_all()
        total = sum(len(exs) for exs in index.values())
        assert total == 0
        assert len(caplog.records) > 0


class TestTestCasePairing:
    """AC: Loads test case file paths (tests/*.in, tests/*.out) paired by number."""

    def test_test_cases_loaded(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        ex = index[1][0]
        assert len(ex.test_cases) >= 2

    def test_test_case_paths_are_paired(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        ex = index[1][0]
        for tc in ex.test_cases:
            assert tc.input_path.suffix == ".in"
            assert tc.output_path.suffix == ".out"
            assert tc.input_path.stem == tc.output_path.stem


class TestExerciseIndex:
    """AC: Returns ExerciseIndex (dict[int, list[Exercise]]) keyed by tier."""

    def test_returns_dict(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        assert isinstance(index, dict)

    def test_keys_are_tier_numbers(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        for key in index:
            assert isinstance(key, int)
            assert 1 <= key <= 5

    def test_values_are_exercise_lists(self):
        loader = ExerciseLoader(FIXTURES_DIR)
        index = loader.load_all()
        for exs in index.values():
            assert isinstance(exs, list)
            for ex in exs:
                assert isinstance(ex, Exercise)


class TestMissingTestFiles:
    """AC: Exercises with missing test files are skipped with log warning."""

    def test_missing_test_files_skips(self, tmp_path, caplog):
        """Exercise with no tests/ directory should be skipped."""
        tier_dir = tmp_path / "tier-1-test"
        ex_dir = tier_dir / "no-tests"
        ex_dir.mkdir(parents=True)
        (ex_dir / "problem.yaml").write_text(
            "id: no-tests\ntitle: No Tests\ntier: 1\ntopic: test\n"
            "description: test\ntime_estimate: 5\n"
        )

        loader = ExerciseLoader(tmp_path)
        with caplog.at_level(logging.WARNING):
            index = loader.load_all()
        total = sum(len(exs) for exs in index.values())
        assert total == 0
        assert any("test" in record.message.lower() for record in caplog.records)

    def test_unpaired_test_files_skips(self, tmp_path, caplog):
        """Exercise with .in but no matching .out should be skipped."""
        tier_dir = tmp_path / "tier-1-test"
        ex_dir = tier_dir / "unpaired"
        tests_dir = ex_dir / "tests"
        tests_dir.mkdir(parents=True)
        (ex_dir / "problem.yaml").write_text(
            "id: unpaired\ntitle: Unpaired\ntier: 1\ntopic: test\n"
            "description: test\ntime_estimate: 5\n"
        )
        (tests_dir / "01.in").write_text("1")
        # no 01.out

        loader = ExerciseLoader(tmp_path)
        with caplog.at_level(logging.WARNING):
            index = loader.load_all()
        total = sum(len(exs) for exs in index.values())
        assert total == 0


class TestEmptyDirectory:
    """AC: Unit tests cover empty directory."""

    def test_empty_exercises_dir(self, tmp_path):
        loader = ExerciseLoader(tmp_path)
        index = loader.load_all()
        assert index == {}

    def test_empty_tier_directory(self, tmp_path):
        (tmp_path / "tier-1-empty").mkdir()
        loader = ExerciseLoader(tmp_path)
        index = loader.load_all()
        total = sum(len(exs) for exs in index.values())
        assert total == 0
