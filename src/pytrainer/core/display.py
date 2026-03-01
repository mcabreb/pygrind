"""Exercise display data preparation helpers."""

from pytrainer.models.exercise import Exercise

TIER_NAMES: dict[int, str] = {
    1: "Easy",
    2: "Basic",
    3: "Medium",
    4: "Hard",
    5: "Expert",
}

TIER_COLORS: dict[int, str] = {
    1: "green",
    2: "blue",
    3: "orange",
    4: "red",
    5: "purple",
}


def format_description(exercise: Exercise) -> str:
    """Return formatted description text for the problem panel."""
    return exercise.description


def get_sample_io(exercise: Exercise) -> tuple[str, str]:
    """Extract first test case as sample input/output for display.

    Returns ("No sample available", "No sample available") if no test cases.
    """
    if not exercise.test_cases:
        return ("No sample available", "No sample available")
    tc = exercise.test_cases[0]
    return (tc.input_text, tc.expected_output)


def get_tier_badge(tier: int) -> tuple[str, str]:
    """Return (badge_text, color) for a tier number.

    Example: (\"Tier 1 — Easy\", \"green\")
    """
    name = TIER_NAMES.get(tier, "Unknown")
    color = TIER_COLORS.get(tier, "gray")
    return (f"Tier {tier} \u2014 {name}", color)
