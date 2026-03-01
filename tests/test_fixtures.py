"""Tests for E1-S04: Create Test Exercise Fixtures."""

from pathlib import Path

import yaml

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "exercises"

TIERS = [
    "tier-1-easy",
    "tier-2-basic",
    "tier-3-medium",
    "tier-4-hard",
    "tier-5-expert",
]

REQUIRED_YAML_FIELDS = ["id", "title", "tier", "topic", "description", "time_estimate"]


class TestFixtureDirectoryStructure:
    """AC: tests/fixtures/exercises/ contains tier-1-easy/ through tier-5-expert/."""

    def test_fixtures_dir_exists(self):
        assert FIXTURES_DIR.is_dir()

    def test_all_tiers_present(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            assert tier_dir.is_dir(), f"Missing tier directory: {tier}"

    def test_each_tier_has_at_least_one_exercise(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            exercises = [d for d in tier_dir.iterdir() if d.is_dir()]
            assert len(exercises) >= 1, f"No exercises in {tier}"


class TestExerciseYaml:
    """AC: Each exercise has a valid problem.yaml with all required fields."""

    def test_all_exercises_have_problem_yaml(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            for ex_dir in tier_dir.iterdir():
                if ex_dir.is_dir():
                    yaml_path = ex_dir / "problem.yaml"
                    assert yaml_path.is_file(), f"Missing problem.yaml in {ex_dir}"

    def test_all_yaml_have_required_fields(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            for ex_dir in tier_dir.iterdir():
                if ex_dir.is_dir():
                    yaml_path = ex_dir / "problem.yaml"
                    if yaml_path.is_file():
                        data = yaml.safe_load(yaml_path.read_text())
                        for field in REQUIRED_YAML_FIELDS:
                            assert field in data, f"Missing field '{field}' in {yaml_path}"

    def test_all_yaml_parseable(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            for ex_dir in tier_dir.iterdir():
                if ex_dir.is_dir():
                    yaml_path = ex_dir / "problem.yaml"
                    if yaml_path.is_file():
                        data = yaml.safe_load(yaml_path.read_text())
                        assert isinstance(data, dict), f"Invalid YAML in {yaml_path}"


class TestTestCases:
    """AC: Each exercise has at least 2 test case pairs."""

    def test_each_exercise_has_test_cases(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            for ex_dir in tier_dir.iterdir():
                if ex_dir.is_dir():
                    tests_dir = ex_dir / "tests"
                    assert tests_dir.is_dir(), f"Missing tests/ in {ex_dir}"

    def test_each_exercise_has_at_least_2_pairs(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            for ex_dir in tier_dir.iterdir():
                if ex_dir.is_dir():
                    tests_dir = ex_dir / "tests"
                    if tests_dir.is_dir():
                        in_files = sorted(tests_dir.glob("*.in"))
                        out_files = sorted(tests_dir.glob("*.out"))
                        assert len(in_files) >= 2, (
                            f"Need >=2 .in files in {tests_dir}, found {len(in_files)}"
                        )
                        assert len(out_files) >= 2, (
                            f"Need >=2 .out files in {tests_dir}, found {len(out_files)}"
                        )

    def test_in_out_pairs_match(self):
        for tier in TIERS:
            tier_dir = FIXTURES_DIR / tier
            for ex_dir in tier_dir.iterdir():
                if ex_dir.is_dir():
                    tests_dir = ex_dir / "tests"
                    if tests_dir.is_dir():
                        in_stems = {f.stem for f in tests_dir.glob("*.in")}
                        out_stems = {f.stem for f in tests_dir.glob("*.out")}
                        assert in_stems == out_stems, (
                            f"Mismatched pairs in {tests_dir}: in={in_stems}, out={out_stems}"
                        )


class TestConftest:
    """AC: conftest.py provides fixture_exercises_dir fixture."""

    def test_fixture_exercises_dir(self, fixture_exercises_dir):
        assert fixture_exercises_dir.is_dir()
        assert (fixture_exercises_dir / "tier-1-easy").is_dir()

    def test_sample_exercise(self, sample_exercise):
        from pytrainer.models.exercise import Exercise

        assert isinstance(sample_exercise, Exercise)
        assert sample_exercise.id
        assert sample_exercise.title
        assert sample_exercise.tier >= 1
        assert len(sample_exercise.test_cases) >= 1

    def test_sample_session_config(self, sample_session_config):
        from pytrainer.models.session import SessionConfig

        assert isinstance(sample_session_config, SessionConfig)
