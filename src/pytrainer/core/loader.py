"""Exercise loader — YAML discovery and parsing."""

import logging
from pathlib import Path

import yaml

from pytrainer.models.exercise import Exercise, ExerciseIndex, TestCase

log = logging.getLogger(__name__)

REQUIRED_FIELDS = ("id", "title", "tier", "topic", "description", "time_estimate")


class ExerciseLoader:
    """Scans an exercises directory, parses YAML, and builds an ExerciseIndex."""

    def __init__(self, exercises_dir: Path) -> None:
        self.exercises_dir = exercises_dir

    def load_all(self) -> ExerciseIndex:
        """Discover and load all valid exercises, grouped by tier."""
        index: ExerciseIndex = {}
        for problem_yaml in sorted(self.exercises_dir.glob("tier-*/*/problem.yaml")):
            exercise = self._load_exercise(problem_yaml)
            if exercise is not None:
                index.setdefault(exercise.tier, []).append(exercise)
        return index

    def _load_exercise(self, yaml_path: Path) -> Exercise | None:
        """Parse a single exercise from its problem.yaml. Returns None on failure."""
        ex_dir = yaml_path.parent

        # Parse YAML
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError:
            log.warning("Invalid YAML in %s — skipping", yaml_path)
            return None

        if not isinstance(data, dict):
            log.warning("YAML is not a mapping in %s — skipping", yaml_path)
            return None

        # Validate required fields
        missing = [f for f in REQUIRED_FIELDS if f not in data]
        if missing:
            log.warning("Missing fields %s in %s — skipping", missing, yaml_path)
            return None

        # Load test case pairs
        test_cases = self._load_test_cases(ex_dir / "tests")
        if not test_cases:
            log.warning("No valid test case pairs in %s — skipping", ex_dir)
            return None

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

    @staticmethod
    def _load_test_cases(tests_dir: Path) -> list[TestCase]:
        """Pair NN.in with NN.out files by stem. Returns empty list if none found."""
        if not tests_dir.is_dir():
            return []

        in_files = {f.stem: f for f in sorted(tests_dir.glob("*.in"))}
        out_files = {f.stem: f for f in sorted(tests_dir.glob("*.out"))}

        pairs = []
        for stem in sorted(in_files.keys() & out_files.keys()):
            pairs.append(TestCase(input_path=in_files[stem], output_path=out_files[stem]))
        return pairs
