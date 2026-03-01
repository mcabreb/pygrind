"""Tests for E2-S05: Exercise Display Data Preparation."""

import tempfile
from pathlib import Path

from pytrainer.core.display import format_description, get_sample_io, get_tier_badge
from pytrainer.models.exercise import Exercise, TestCase


def _make_exercise(test_cases: list[TestCase] | None = None) -> Exercise:
    """Helper: build an Exercise with optional test cases."""
    return Exercise(
        id="test-ex",
        title="Test Exercise",
        tier=1,
        topic="basics",
        description="Read two numbers and print their sum.",
        time_estimate=5,
        test_cases=test_cases or [],
    )


def _make_test_case(input_text: str, output_text: str) -> TestCase:
    """Helper: create a TestCase with temp files."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".in", delete=False) as in_file:
        in_file.write(input_text)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".out", delete=False) as out_file:
        out_file.write(output_text)
    return TestCase(input_path=Path(in_file.name), output_path=Path(out_file.name))


class TestFormatDescription:
    """AC: Provides formatted description text for the problem panel."""

    def test_returns_description_text(self):
        ex = _make_exercise()
        result = format_description(ex)
        assert "Read two numbers and print their sum." in result

    def test_returns_string(self):
        ex = _make_exercise()
        result = format_description(ex)
        assert isinstance(result, str)


class TestGetSampleIO:
    """AC: Extracts first test case as sample input/output for display."""

    def test_returns_first_test_case_content(self):
        tc = _make_test_case("3\n5\n", "8\n")
        ex = _make_exercise(test_cases=[tc])
        sample_in, sample_out = get_sample_io(ex)
        assert sample_in == "3\n5\n"
        assert sample_out == "8\n"

    def test_returns_tuple_of_strings(self):
        tc = _make_test_case("1\n", "1\n")
        ex = _make_exercise(test_cases=[tc])
        result = get_sample_io(ex)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)

    def test_no_test_cases_returns_placeholder(self):
        """AC: Handles exercises with no test cases gracefully."""
        ex = _make_exercise(test_cases=[])
        sample_in, sample_out = get_sample_io(ex)
        assert "No sample available" in sample_in
        assert "No sample available" in sample_out


class TestGetTierBadge:
    """AC: Returns tier badge text and associated color."""

    def test_tier_1_badge(self):
        text, color = get_tier_badge(1)
        assert "Tier 1" in text
        assert "Easy" in text
        assert color == "green"

    def test_tier_2_badge(self):
        text, color = get_tier_badge(2)
        assert "Tier 2" in text
        assert "Basic" in text
        assert color == "blue"

    def test_tier_3_badge(self):
        text, color = get_tier_badge(3)
        assert "Tier 3" in text
        assert "Medium" in text
        assert color == "orange"

    def test_tier_4_badge(self):
        text, color = get_tier_badge(4)
        assert "Tier 4" in text
        assert "Hard" in text
        assert color == "red"

    def test_tier_5_badge(self):
        text, color = get_tier_badge(5)
        assert "Tier 5" in text
        assert "Expert" in text
        assert color == "purple"

    def test_returns_tuple_of_strings(self):
        result = get_tier_badge(1)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)
