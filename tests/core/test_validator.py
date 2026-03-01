"""Tests for E2-S03: Output Validator — Exact, Unordered, Tolerance."""

import pytest

from pytrainer.core.validator import ValidationResult, Validator


class TestExactMode:
    """AC: Exact mode: strips trailing whitespace per line and trailing blank lines."""

    def test_exact_match(self):
        result = Validator.compare("hello\nworld\n", "hello\nworld\n", mode="exact")
        assert result.passed is True

    def test_exact_trailing_whitespace(self):
        result = Validator.compare("hello  \nworld\t\n", "hello\nworld\n", mode="exact")
        assert result.passed is True

    def test_exact_trailing_blank_lines(self):
        result = Validator.compare("hello\nworld\n\n\n", "hello\nworld\n", mode="exact")
        assert result.passed is True

    def test_exact_mismatch(self):
        result = Validator.compare("hello\nworld\n", "hello\nearth\n", mode="exact")
        assert result.passed is False
        assert result.details != ""

    def test_exact_different_line_count(self):
        result = Validator.compare("hello\n", "hello\nworld\n", mode="exact")
        assert result.passed is False


class TestUnorderedMode:
    """AC: Unordered mode: sorts both line lists then compares (handles duplicates)."""

    def test_unordered_same_order(self):
        result = Validator.compare("a\nb\nc\n", "a\nb\nc\n", mode="unordered")
        assert result.passed is True

    def test_unordered_different_order(self):
        result = Validator.compare("c\na\nb\n", "a\nb\nc\n", mode="unordered")
        assert result.passed is True

    def test_unordered_with_duplicates(self):
        result = Validator.compare("a\na\nb\n", "a\nb\na\n", mode="unordered")
        assert result.passed is True

    def test_unordered_mismatch(self):
        result = Validator.compare("a\nb\n", "a\nc\n", mode="unordered")
        assert result.passed is False

    def test_unordered_different_counts_of_duplicates(self):
        result = Validator.compare("a\na\nb\n", "a\nb\nb\n", mode="unordered")
        assert result.passed is False


class TestToleranceMode:
    """AC: Tolerance mode: parses each line as float, compares within tolerance."""

    def test_tolerance_exact_match(self):
        result = Validator.compare("3.14\n2.72\n", "3.14\n2.72\n", mode="tolerance")
        assert result.passed is True

    def test_tolerance_within_epsilon(self):
        result = Validator.compare(
            "3.1400001\n2.72\n", "3.14\n2.72\n", mode="tolerance", tolerance=1e-6
        )
        assert result.passed is True

    def test_tolerance_outside_epsilon(self):
        result = Validator.compare(
            "3.15\n2.72\n", "3.14\n2.72\n", mode="tolerance", tolerance=1e-6
        )
        assert result.passed is False

    def test_tolerance_custom_epsilon(self):
        result = Validator.compare("3.15\n", "3.14\n", mode="tolerance", tolerance=0.02)
        assert result.passed is True

    def test_tolerance_mixed_int_float(self):
        """AC: Handles tolerance mode with mixed int/float output."""
        result = Validator.compare("42\n3.14\n", "42\n3.14\n", mode="tolerance")
        assert result.passed is True

    def test_tolerance_int_comparison(self):
        result = Validator.compare("42\n", "42\n", mode="tolerance")
        assert result.passed is True


class TestValidationResult:
    """AC: Returns ValidationResult with passed (bool) and details (diff string on failure)."""

    def test_result_has_passed(self):
        result = Validator.compare("hello\n", "hello\n", mode="exact")
        assert isinstance(result, ValidationResult)
        assert hasattr(result, "passed")
        assert isinstance(result.passed, bool)

    def test_result_has_details(self):
        result = Validator.compare("hello\n", "world\n", mode="exact")
        assert isinstance(result, ValidationResult)
        assert hasattr(result, "details")
        assert isinstance(result.details, str)

    def test_passed_result_details_empty(self):
        result = Validator.compare("hello\n", "hello\n", mode="exact")
        assert result.details == ""


class TestEdgeCases:
    """AC: Handles edge cases: empty output, Windows line endings, mixed line types."""

    def test_empty_output_matches_empty_expected(self):
        result = Validator.compare("", "", mode="exact")
        assert result.passed is True

    def test_empty_output_vs_nonempty(self):
        result = Validator.compare("", "hello\n", mode="exact")
        assert result.passed is False

    def test_windows_line_endings(self):
        result = Validator.compare("hello\r\nworld\r\n", "hello\nworld\n", mode="exact")
        assert result.passed is True

    def test_mixed_line_endings(self):
        result = Validator.compare("hello\r\nworld\n", "hello\nworld\n", mode="exact")
        assert result.passed is True


class TestDiffDetails:
    """AC: Diff details show first mismatching line number and expected vs actual values."""

    def test_diff_shows_line_number(self):
        result = Validator.compare("hello\nworld\n", "hello\nearth\n", mode="exact")
        assert "2" in result.details

    def test_diff_shows_expected_and_actual(self):
        result = Validator.compare("hello\nworld\n", "hello\nearth\n", mode="exact")
        assert "world" in result.details
        assert "earth" in result.details

    def test_tolerance_diff_shows_values(self):
        result = Validator.compare("3.15\n", "3.14\n", mode="tolerance", tolerance=1e-6)
        assert "3.15" in result.details
        assert "3.14" in result.details


class TestParametrized:
    """AC: Parametrized unit tests cover all 3 modes with edge cases."""

    @pytest.mark.parametrize(
        "actual,expected,mode,should_pass",
        [
            # Exact mode
            ("42\n", "42\n", "exact", True),
            ("42  \n", "42\n", "exact", True),
            ("42\n\n", "42\n", "exact", True),
            ("42\n", "43\n", "exact", False),
            # Unordered mode
            ("b\na\n", "a\nb\n", "unordered", True),
            ("a\n", "b\n", "unordered", False),
            # Tolerance mode
            ("1.0000001\n", "1.0\n", "tolerance", True),
            ("2.0\n", "1.0\n", "tolerance", False),
        ],
    )
    def test_modes(self, actual, expected, mode, should_pass):
        result = Validator.compare(actual, expected, mode=mode)
        assert result.passed is should_pass
