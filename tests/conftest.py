"""Shared pytest fixtures for PyTrainer test suite."""

from pathlib import Path

import pytest
import yaml

from pytrainer.models.exercise import Exercise, TestCase
from pytrainer.models.session import DifficultyMode, SessionConfig


@pytest.fixture
def fixture_exercises_dir():
    """Return the Path to the test fixtures exercises directory."""
    return Path(__file__).parent / "fixtures" / "exercises"


@pytest.fixture
def sample_exercise(fixture_exercises_dir):
    """Return a loaded Exercise object from the tier-1 fixture."""
    ex_dir = fixture_exercises_dir / "tier-1-easy" / "sum-two-numbers"
    yaml_path = ex_dir / "problem.yaml"
    data = yaml.safe_load(yaml_path.read_text())

    tests_dir = ex_dir / "tests"
    test_cases = []
    for in_file in sorted(tests_dir.glob("*.in")):
        out_file = in_file.with_suffix(".out")
        if out_file.exists():
            test_cases.append(TestCase(input_path=in_file, output_path=out_file))

    return Exercise(
        id=data["id"],
        title=data["title"],
        tier=data["tier"],
        topic=data["topic"],
        description=data["description"],
        time_estimate=data["time_estimate"],
        test_cases=test_cases,
        hint=data.get("hint"),
        solution=data.get("solution"),
        source=data.get("source", "original"),
        validation=data.get("validation", "exact"),
        tolerance=data.get("tolerance", 1e-6),
    )


@pytest.fixture
def sample_session_config():
    """Return a SessionConfig with default settings."""
    return SessionConfig(mode=DifficultyMode.BEGINNER)
