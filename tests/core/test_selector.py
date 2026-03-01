"""Tests for E2-S02: Tier-Based Random Exercise Selection."""

import logging
import random

from pytrainer.core.selector import select_session
from pytrainer.models.exercise import Exercise, ExerciseIndex


def _make_exercises(tier: int, count: int) -> list[Exercise]:
    """Helper: create N dummy exercises for a given tier."""
    return [
        Exercise(
            id=f"tier{tier}-ex{i}",
            title=f"Exercise {i}",
            tier=tier,
            topic="test",
            description="test",
            time_estimate=5,
            test_cases=[],
        )
        for i in range(count)
    ]


def _full_index(per_tier: int = 20) -> ExerciseIndex:
    """Helper: index with enough exercises per tier."""
    return {t: _make_exercises(t, per_tier) for t in range(1, 6)}


class TestCorrectDistribution:
    """AC: Selects exactly 30 exercises: 8 tier-1, 8 tier-2, 6 tier-3, 5 tier-4, 3 tier-5."""

    def test_total_count(self):
        index = _full_index()
        result = select_session(index)
        assert len(result) == 30

    def test_tier_distribution(self):
        index = _full_index()
        result = select_session(index)
        tier_counts = {}
        for ex in result:
            tier_counts[ex.tier] = tier_counts.get(ex.tier, 0) + 1
        assert tier_counts == {1: 8, 2: 8, 3: 6, 4: 5, 5: 3}


class TestRandomSelection:
    """AC: Selection is random within each tier (different results on repeated calls)."""

    def test_different_results_on_repeated_calls(self):
        index = _full_index()
        results = [tuple(ex.id for ex in select_session(index)) for _ in range(10)]
        # With 20 exercises per tier, 10 calls should produce at least 2 distinct orderings
        assert len(set(results)) > 1

    def test_seeded_random_is_reproducible(self):
        index = _full_index()
        random.seed(42)
        r1 = [ex.id for ex in select_session(index)]
        random.seed(42)
        r2 = [ex.id for ex in select_session(index)]
        assert r1 == r2


class TestNoRepeats:
    """AC: No exercise is repeated within a session."""

    def test_no_duplicate_exercises(self):
        index = _full_index()
        result = select_session(index)
        ids = [ex.id for ex in result]
        assert len(ids) == len(set(ids))


class TestInsufficientTier:
    """AC: If a tier has fewer exercises than required, selects all available and logs warning."""

    def test_insufficient_tier_selects_all_available(self):
        index = _full_index()
        index[1] = _make_exercises(1, 2)  # Only 2, need 8
        result = select_session(index)
        tier1 = [ex for ex in result if ex.tier == 1]
        assert len(tier1) == 2

    def test_insufficient_tier_logs_warning(self, caplog):
        index = _full_index()
        index[1] = _make_exercises(1, 2)
        with caplog.at_level(logging.WARNING):
            select_session(index)
        assert any("tier 1" in record.message.lower() for record in caplog.records)

    def test_missing_tier_returns_empty_for_that_tier(self):
        index = _full_index()
        del index[5]  # No tier-5 at all
        result = select_session(index)
        tier5 = [ex for ex in result if ex.tier == 5]
        assert len(tier5) == 0

    def test_total_less_than_30_when_insufficient(self):
        index = _full_index()
        index[1] = _make_exercises(1, 2)
        result = select_session(index)
        assert len(result) < 30


class TestAscendingTierOrder:
    """AC: Returns exercises ordered by ascending tier (easy first)."""

    def test_ascending_tier_order(self):
        index = _full_index()
        result = select_session(index)
        tiers = [ex.tier for ex in result]
        assert tiers == sorted(tiers)

    def test_ascending_order_with_insufficient_tiers(self):
        index = _full_index()
        index[1] = _make_exercises(1, 2)
        result = select_session(index)
        tiers = [ex.tier for ex in result]
        assert tiers == sorted(tiers)
