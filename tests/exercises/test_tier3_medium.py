"""Tests for E6-S03: Tier 3 — Medium Exercises.

Validates that all tier-3-medium exercises:
- Load via ExerciseLoader with valid YAML and required fields
- Have at least 3 test case pairs each (including edge cases)
- Cover the expected topics (sorting, searching, recursion, data structures)
- Have hint and solution fields populated
"""

import subprocess
import sys
from pathlib import Path

from pytrainer.core.loader import ExerciseLoader

EXERCISES_DIR = Path(__file__).parents[2] / "exercises"
TIER3_DIR = EXERCISES_DIR / "tier-3-medium"


class TestTier3ExerciseCount:
    """AC: 4-6 exercises in exercises/tier-3-medium/."""

    def test_tier3_directory_exists(self):
        assert TIER3_DIR.is_dir(), f"Missing directory: {TIER3_DIR}"

    def test_tier3_has_4_to_6_exercises(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        assert 3 in index, "No tier-3 exercises loaded"
        count = len(index[3])
        assert 4 <= count <= 6, f"Expected 4-6 tier-3 exercises, got {count}"


class TestTier3YamlValidity:
    """AC: Each has valid problem.yaml with hint and solution."""

    def test_all_exercises_have_hint(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(3, []):
            assert ex.hint is not None, f"Exercise {ex.id} missing hint"

    def test_all_exercises_have_solution(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(3, []):
            assert ex.solution is not None, f"Exercise {ex.id} missing solution"

    def test_exercise_ids_follow_convention(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(3, []):
            assert ex.id.startswith("t3-"), f"Exercise {ex.id} should start with 't3-'"


class TestTier3TestCases:
    """AC: Each has at least 3 test case pairs including edge cases."""

    def test_all_exercises_have_at_least_3_test_cases(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(3, []):
            assert len(ex.test_cases) >= 3, (
                f"Exercise {ex.id} has {len(ex.test_cases)} test cases, need >= 3"
            )


class TestTier3Topics:
    """AC: Topics covered: sorting, searching, recursion, data structures."""

    def test_topics_cover_required_areas(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        topics = {ex.topic for ex in index.get(3, [])}
        # Need at least 3 of the 4 required topic areas
        required = {"sorting", "searching", "recursion", "data structures"}
        covered = required & topics
        assert len(covered) >= 3, f"Need >= 3 of {required} covered, got {covered}"


class TestTier3Solutions:
    """Verify each solution produces correct output for all test cases."""

    def test_solutions_produce_correct_output(self):
        loader = ExerciseLoader(EXERCISES_DIR)
        index = loader.load_all()
        for ex in index.get(3, []):
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
