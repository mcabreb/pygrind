"""Tests for E6-S04: Tier 4 — Hard Exercises.

Validates that all tier-4-hard exercises:
- Load via ExerciseLoader with valid YAML and required fields
- Have at least 3 test case pairs each (including large inputs)
- Cover the expected topics (DP, graphs, complex algorithms)
- Have hint and solution fields populated
"""

import subprocess
import sys
from pathlib import Path

from pytrainer.core.loader import ExerciseLoader

EXERCISES_DIR = Path(__file__).parents[2] / "exercises"
TIER4_DIR = EXERCISES_DIR / "tier-4-hard"


class TestTier4ExerciseCount:
    """AC: 3-5 exercises in exercises/tier-4-hard/."""

    def test_tier4_directory_exists(self):
        assert TIER4_DIR.is_dir(), f"Missing directory: {TIER4_DIR}"

    def test_tier4_has_3_to_5_exercises(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        assert 4 in index, "No tier-4 exercises loaded"
        count = len(index[4])
        assert 3 <= count <= 5, f"Expected 3-5 tier-4 exercises, got {count}"


class TestTier4YamlValidity:
    """AC: Each has valid problem.yaml with hint and solution."""

    def test_all_exercises_have_hint(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(4, []):
            assert ex.hint is not None, f"Exercise {ex.id} missing hint"

    def test_all_exercises_have_solution(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(4, []):
            assert ex.solution is not None, f"Exercise {ex.id} missing solution"

    def test_exercise_ids_follow_convention(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(4, []):
            assert ex.id.startswith("t4-"), f"Exercise {ex.id} should start with 't4-'"


class TestTier4TestCases:
    """AC: Each has at least 3 test case pairs including large inputs."""

    def test_all_exercises_have_at_least_3_test_cases(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(4, []):
            assert len(ex.test_cases) >= 3, (
                f"Exercise {ex.id} has {len(ex.test_cases)} test cases, need >= 3"
            )


class TestTier4Topics:
    """AC: Topics covered: DP, graphs, complex algorithms."""

    def test_topics_cover_required_areas(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        topics = {ex.topic for ex in index.get(4, [])}
        required = {"dp", "graphs"}
        missing = required - topics
        assert not missing, f"Missing required topics: {missing}"


class TestTier4Solutions:
    """Verify each solution produces correct output for all test cases within 10s."""

    def test_solutions_produce_correct_output(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(4, []):
            for tc in ex.test_cases:
                result = subprocess.run(
                    [sys.executable, "-c", ex.solution],
                    input=tc.input_text,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                assert result.returncode == 0, (
                    f"Solution for {ex.id} failed on {tc.input_path.name}: {result.stderr}"
                )
                assert result.stdout.strip() == tc.expected_output.strip(), (
                    f"Solution for {ex.id} wrong output on {tc.input_path.name}: "
                    f"expected {tc.expected_output.strip()!r}, got {result.stdout.strip()!r}"
                )
