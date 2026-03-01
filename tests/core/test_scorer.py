"""Tests for E2-S04: Score Calculator."""

import pytest

from pytrainer.core.scorer import Scorer


class TestBasePoints:
    """AC: Base points: T1=10, T2=20, T3=35, T4=50, T5=75."""

    @pytest.mark.parametrize(
        "tier,expected",
        [(1, 10), (2, 20), (3, 35), (4, 50), (5, 75)],
    )
    def test_base_points_per_tier(self, tier, expected):
        # time_spent=500, time_estimate=5 → threshold=150 → no bonus
        score = Scorer.calculate(
            tier=tier,
            time_spent=500,
            time_estimate=5,
            attempts=0,
            solution_viewed=False,
        )
        assert score == expected


class TestTimeBonus:
    """AC: Time bonus: +10% if time_spent < (time_estimate_minutes * 60) / 2."""

    def test_time_bonus_applied(self):
        # time_estimate=10 min → threshold = 300s, time_spent=100 < 300 → +10%
        score = Scorer.calculate(
            tier=1, time_spent=100, time_estimate=10, attempts=0, solution_viewed=False
        )
        assert score == 11  # int(10 * 1.1) = 11

    def test_no_time_bonus_at_threshold(self):
        # time_estimate=10 → threshold=300, time_spent=300 → NOT less than → no bonus
        score = Scorer.calculate(
            tier=1, time_spent=300, time_estimate=10, attempts=0, solution_viewed=False
        )
        assert score == 10

    def test_no_time_bonus_over_threshold(self):
        score = Scorer.calculate(
            tier=1, time_spent=500, time_estimate=10, attempts=0, solution_viewed=False
        )
        assert score == 10

    def test_time_bonus_tier5(self):
        # T5=75, bonus → int(75 * 1.1) = 82
        score = Scorer.calculate(
            tier=5, time_spent=100, time_estimate=20, attempts=0, solution_viewed=False
        )
        assert score == 82


class TestWrongAttemptPenalty:
    """AC: Wrong attempt penalty: -10% per attempt, minimum 50% of base score."""

    def test_one_attempt_penalty(self):
        # T1=10, 1 attempt → int(10 * (1 - 0.10)) = int(9.0) = 9
        score = Scorer.calculate(
            tier=1, time_spent=500, time_estimate=5, attempts=1, solution_viewed=False
        )
        assert score == 9

    def test_two_attempts_penalty(self):
        # T1=10, 2 attempts → int(10 * (1 - 0.20)) = int(8.0) = 8
        score = Scorer.calculate(
            tier=1, time_spent=500, time_estimate=5, attempts=2, solution_viewed=False
        )
        assert score == 8

    def test_three_attempts_penalty(self):
        score = Scorer.calculate(
            tier=1, time_spent=500, time_estimate=5, attempts=3, solution_viewed=False
        )
        assert score == 7

    def test_five_attempts_max_penalty(self):
        # 5 * 0.10 = 0.50 → capped at 0.50 → int(10 * 0.50) = 5
        score = Scorer.calculate(
            tier=1, time_spent=500, time_estimate=5, attempts=5, solution_viewed=False
        )
        assert score == 5

    def test_more_than_five_attempts_still_capped(self):
        # 10 * 0.10 = 1.00, capped at 0.50 → int(10 * 0.50) = 5
        score = Scorer.calculate(
            tier=1, time_spent=500, time_estimate=5, attempts=10, solution_viewed=False
        )
        assert score == 5

    def test_zero_attempts_no_penalty(self):
        score = Scorer.calculate(
            tier=1, time_spent=500, time_estimate=5, attempts=0, solution_viewed=False
        )
        assert score == 10


class TestSolutionViewed:
    """AC: Solution viewed: returns 0 regardless of other factors."""

    def test_solution_viewed_returns_zero(self):
        score = Scorer.calculate(
            tier=5, time_spent=10, time_estimate=20, attempts=0, solution_viewed=True
        )
        assert score == 0

    def test_solution_viewed_overrides_bonus(self):
        score = Scorer.calculate(
            tier=1, time_spent=10, time_estimate=10, attempts=0, solution_viewed=True
        )
        assert score == 0

    def test_solution_viewed_with_attempts(self):
        score = Scorer.calculate(
            tier=3, time_spent=500, time_estimate=10, attempts=3, solution_viewed=True
        )
        assert score == 0


class TestIntegerTruncation:
    """AC: Returns integer score (truncated, not rounded)."""

    def test_returns_int(self):
        score = Scorer.calculate(
            tier=1, time_spent=100, time_estimate=10, attempts=0, solution_viewed=False
        )
        assert isinstance(score, int)

    def test_truncation_not_rounding(self):
        # T3=35, bonus → 35*1.1=38.5, 1 attempt → int(38.5 * 0.9) = int(34.65) = 34
        score = Scorer.calculate(
            tier=3, time_spent=100, time_estimate=10, attempts=1, solution_viewed=False
        )
        assert score == 34


class TestCombinedBonusAndPenalty:
    """AC: Boundary case tests — combined bonus + penalty."""

    def test_bonus_plus_penalty(self):
        # T2=20, bonus → int(20*1.1)=22, 2 attempts → int(22 * 0.80) = int(17.6) = 17
        score = Scorer.calculate(
            tier=2, time_spent=100, time_estimate=10, attempts=2, solution_viewed=False
        )
        assert score == 17

    def test_bonus_plus_max_penalty(self):
        # T2=20, bonus → 22, 5 attempts → int(22 * 0.50) = 11
        score = Scorer.calculate(
            tier=2, time_spent=100, time_estimate=10, attempts=5, solution_viewed=False
        )
        assert score == 11
