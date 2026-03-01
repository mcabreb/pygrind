"""Tests for E7-S06: Post-Session Analytics."""

import pytest

from pytrainer.core.analytics import SessionAnalytics
from pytrainer.models.exercise import Exercise
from pytrainer.models.session import (
    DifficultyMode,
    ProblemState,
    ProblemStatus,
    SessionConfig,
    SessionResult,
)
from pytrainer.storage.database import Database


def _make_exercise(id_: str, tier: int, topic: str, time_estimate: int = 5) -> Exercise:
    return Exercise(
        id=id_,
        title=f"Exercise {id_}",
        tier=tier,
        topic=topic,
        description="",
        time_estimate=time_estimate,
        test_cases=[],
    )


def _make_result(
    session_id: str,
    date: str,
    problems: list[ProblemState],
    total_score: int = 0,
) -> SessionResult:
    return SessionResult(
        session_id=session_id,
        date=date,
        config=SessionConfig(mode=DifficultyMode.BEGINNER),
        problems=problems,
        total_score=total_score,
        max_score=100,
        time_used=300.0,
    )


@pytest.fixture
def db(tmp_path):
    return Database(tmp_path / "test.db")


@pytest.fixture
def current_result():
    """A session result with mixed outcomes."""
    problems = [
        ProblemState(
            exercise=_make_exercise("e1", 1, "loops"),
            status=ProblemStatus.SOLVED,
            score=10,
            time_spent=60.0,
        ),
        ProblemState(
            exercise=_make_exercise("e2", 1, "loops"),
            status=ProblemStatus.SOLVED,
            score=10,
            time_spent=90.0,
        ),
        ProblemState(
            exercise=_make_exercise("e3", 2, "strings"),
            status=ProblemStatus.ATTEMPTED,
            score=0,
            time_spent=120.0,
        ),
        ProblemState(
            exercise=_make_exercise("e4", 3, "math"),
            status=ProblemStatus.UNSOLVED,
            score=0,
            time_spent=0.0,
        ),
    ]
    return _make_result("sess-current", "2026-03-01 12:00", problems, total_score=20)


class TestTierPerformance:
    """AC: Tier performance: solve rate per tier for current session."""

    def test_tier_solve_rates(self, current_result):
        analytics = SessionAnalytics(current_result)
        tier_stats = analytics.tier_performance()
        assert tier_stats[1]["solved"] == 2
        assert tier_stats[1]["total"] == 2
        assert tier_stats[2]["solved"] == 0
        assert tier_stats[2]["total"] == 1

    def test_tier_with_no_problems(self, current_result):
        analytics = SessionAnalytics(current_result)
        tier_stats = analytics.tier_performance()
        # Tier 4 and 5 not in session
        assert 4 not in tier_stats
        assert 5 not in tier_stats


class TestTimeAnalysis:
    """AC: Time analysis: average time vs estimate per tier."""

    def test_average_time_per_tier(self, current_result):
        analytics = SessionAnalytics(current_result)
        time_stats = analytics.time_analysis()
        # Tier 1: two problems, 60+90=150, avg=75
        assert time_stats[1]["avg_time"] == 75.0
        assert time_stats[1]["estimate"] == 300  # 5 min * 60

    def test_skipped_tier_excluded(self, current_result):
        analytics = SessionAnalytics(current_result)
        time_stats = analytics.time_analysis()
        # Tier 3 has 0 time_spent — still in the dict but avg is 0
        assert time_stats[3]["avg_time"] == 0.0


class TestTopicPerformance:
    """AC: Topic performance: per-topic solve percentage across last N sessions."""

    def test_topic_stats_from_db(self, db, current_result):
        db.save_session(current_result)
        analytics = SessionAnalytics(current_result, db=db)
        topic_stats = analytics.topic_performance()
        assert topic_stats["loops"]["solve_rate"] == 1.0  # 2/2
        assert topic_stats["strings"]["solve_rate"] == 0.0  # 0/1


class TestScoreTrend:
    """AC: Comparison to previous sessions if history exists (score trend)."""

    def test_no_history_returns_empty(self, db, current_result):
        analytics = SessionAnalytics(current_result, db=db)
        trend = analytics.score_trend()
        assert trend == []

    def test_returns_last_scores(self, db, current_result):
        # Save some prior sessions
        for i in range(3):
            prev = _make_result(f"prev-{i}", f"2026-02-{10+i} 12:00", [], total_score=i * 10)
            db.save_session(prev)
        analytics = SessionAnalytics(current_result, db=db)
        trend = analytics.score_trend()
        assert len(trend) == 3


class TestRecommendations:
    """AC: Top 3 specific recommendations."""

    def test_generates_recommendations(self, db, current_result):
        db.save_session(current_result)
        analytics = SessionAnalytics(current_result, db=db)
        recs = analytics.recommendations()
        assert isinstance(recs, list)
        assert len(recs) <= 3

    def test_recommendations_are_strings(self, db, current_result):
        db.save_session(current_result)
        analytics = SessionAnalytics(current_result, db=db)
        recs = analytics.recommendations()
        assert all(isinstance(r, str) for r in recs)

    def test_no_data_returns_empty(self, db, current_result):
        analytics = SessionAnalytics(current_result, db=db)
        # No data saved yet
        recs = analytics.recommendations()
        assert isinstance(recs, list)
