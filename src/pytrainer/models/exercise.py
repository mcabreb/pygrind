"""Exercise and TestCase data models."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestCase:
    """A single test case with lazy-loaded input/output content."""

    input_path: Path
    output_path: Path
    _input_text: str | None = field(default=None, repr=False)
    _expected_output: str | None = field(default=None, repr=False)

    @property
    def input_text(self) -> str:
        """Lazily load and cache input file content."""
        if self._input_text is None:
            self._input_text = self.input_path.read_text()
        return self._input_text

    @property
    def expected_output(self) -> str:
        """Lazily load and cache expected output file content."""
        if self._expected_output is None:
            self._expected_output = self.output_path.read_text()
        return self._expected_output


@dataclass
class Exercise:
    """A competition exercise with metadata and test cases."""

    id: str
    title: str
    tier: int
    topic: str
    description: str
    time_estimate: int
    test_cases: list[TestCase]
    hint: str | None = None
    solution: str | None = None
    source: str = "original"
    validation: str = "exact"
    tolerance: float = 1e-6


ExerciseIndex = dict[int, list[Exercise]]
