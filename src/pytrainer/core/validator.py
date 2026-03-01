"""Output validator — exact, unordered, and tolerance comparison modes."""

from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of comparing actual output against expected output."""

    passed: bool
    details: str = ""


class Validator:
    """Compares user output against expected output using different modes."""

    @staticmethod
    def compare(
        actual: str,
        expected: str,
        mode: str = "exact",
        tolerance: float = 1e-6,
    ) -> ValidationResult:
        """Compare actual vs expected using the specified mode."""
        actual_lines = _normalize(actual)
        expected_lines = _normalize(expected)

        if mode == "exact":
            return _compare_exact(actual_lines, expected_lines)
        elif mode == "unordered":
            return _compare_unordered(actual_lines, expected_lines)
        elif mode == "tolerance":
            return _compare_tolerance(actual_lines, expected_lines, tolerance)
        else:
            return ValidationResult(passed=False, details=f"Unknown mode: {mode}")


def _normalize(text: str) -> list[str]:
    """Normalize text: convert CRLF, strip trailing whitespace per line, strip trailing blanks."""
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    lines = [line.rstrip() for line in lines]
    # Strip trailing blank lines
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _compare_exact(actual: list[str], expected: list[str]) -> ValidationResult:
    """Line-by-line exact comparison after normalization."""
    if len(actual) != len(expected):
        return ValidationResult(
            passed=False,
            details=(f"Line count differs: expected {len(expected)} lines, got {len(actual)}"),
        )
    for i, (a, e) in enumerate(zip(actual, expected, strict=True), start=1):
        if a != e:
            return ValidationResult(
                passed=False,
                details=f"Line {i}: expected '{e}' but got '{a}'",
            )
    return ValidationResult(passed=True)


def _compare_unordered(actual: list[str], expected: list[str]) -> ValidationResult:
    """Sort both line lists then compare (handles duplicate lines)."""
    sorted_actual = sorted(actual)
    sorted_expected = sorted(expected)
    if sorted_actual != sorted_expected:
        # Find first mismatch in sorted lists
        for i, (a, e) in enumerate(zip(sorted_actual, sorted_expected, strict=False), start=1):
            if a != e:
                return ValidationResult(
                    passed=False,
                    details=f"Sorted line {i}: expected '{e}' but got '{a}'",
                )
        # Different lengths
        return ValidationResult(
            passed=False,
            details=(
                f"Line count differs: expected {len(sorted_expected)}, got {len(sorted_actual)}"
            ),
        )
    return ValidationResult(passed=True)


def _compare_tolerance(
    actual: list[str], expected: list[str], tolerance: float
) -> ValidationResult:
    """Compare each line as a float within tolerance."""
    if len(actual) != len(expected):
        return ValidationResult(
            passed=False,
            details=(f"Line count differs: expected {len(expected)} lines, got {len(actual)}"),
        )
    for i, (a, e) in enumerate(zip(actual, expected, strict=True), start=1):
        try:
            val_a = float(a)
            val_e = float(e)
        except ValueError:
            return ValidationResult(
                passed=False,
                details=f"Line {i}: cannot parse as number — expected '{e}', got '{a}'",
            )
        if abs(val_a - val_e) > tolerance:
            return ValidationResult(
                passed=False,
                details=f"Line {i}: expected '{e}' but got '{a}' (diff={abs(val_a - val_e):.2e})",
            )
    return ValidationResult(passed=True)
