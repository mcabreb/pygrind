"""Post-session analytics engine."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pytrainer.models.session import ProblemStatus, SessionResult

if TYPE_CHECKING:
    from pytrainer.storage.database import Database


class SessionAnalytics:
    """Analyzes a session result and historical data for recommendations."""

    def __init__(
        self,
        result: SessionResult,
        db: Database | None = None,
    ) -> None:
        self._result = result
        self._db = db

    def tier_performance(self) -> dict[int, dict[str, int]]:
        """Solve rate per tier for the current session."""
        stats: dict[int, dict[str, int]] = {}
        for ps in self._result.problems:
            tier = ps.exercise.tier
            if tier not in stats:
                stats[tier] = {"solved": 0, "total": 0}
            stats[tier]["total"] += 1
            if ps.status == ProblemStatus.SOLVED:
                stats[tier]["solved"] += 1
        return stats

    def time_analysis(self) -> dict[int, dict[str, float]]:
        """Average time vs estimate per tier."""
        tier_times: dict[int, list[float]] = {}
        tier_estimates: dict[int, int] = {}
        for ps in self._result.problems:
            tier = ps.exercise.tier
            if tier not in tier_times:
                tier_times[tier] = []
                tier_estimates[tier] = ps.exercise.time_estimate * 60
            tier_times[tier].append(ps.time_spent)

        result: dict[int, dict[str, float]] = {}
        for tier, times in tier_times.items():
            avg = sum(times) / len(times) if times else 0.0
            result[tier] = {
                "avg_time": avg,
                "estimate": float(tier_estimates[tier]),
            }
        return result

    def topic_performance(self) -> dict[str, dict[str, Any]]:
        """Per-topic solve percentage from database history."""
        if self._db is None:
            return {}
        stats = self._db.get_topic_stats()
        result: dict[str, dict[str, Any]] = {}
        for topic, data in stats.items():
            total = data["total"]
            solved = data["solved"]
            result[topic] = {
                "solved": solved,
                "total": total,
                "solve_rate": solved / total if total > 0 else 0.0,
            }
        return result

    def score_trend(self, limit: int = 5) -> list[dict[str, Any]]:
        """Last N session scores for trend comparison."""
        if self._db is None:
            return []
        sessions = self._db.get_sessions()
        # Exclude current session from trend
        trend = [
            {"date": s["date"], "score": s["total_score"], "max_score": s["max_score"]}
            for s in sessions
            if s["session_id"] != self._result.session_id
        ]
        return trend[:limit]

    def recommendations(self, min_data: int = 1) -> list[str]:
        """Top 3 improvement recommendations based on weakest areas."""
        if self._db is None:
            return []

        topic_stats = self.topic_performance()
        tier_stats = self.tier_performance()

        # Rank topics by weakness (lowest solve rate with enough data)
        weak_topics = [
            (topic, data)
            for topic, data in topic_stats.items()
            if data["total"] >= min_data and data["solve_rate"] < 1.0
        ]
        weak_topics.sort(key=lambda x: x[1]["solve_rate"])

        recs: list[str] = []

        # Topic-based recommendations
        for topic, data in weak_topics[:2]:
            pct = int(data["solve_rate"] * 100)
            recs.append(f"Focus on {topic} — {pct}% solve rate ({data['solved']}/{data['total']})")

        # Tier-based recommendation
        weak_tiers = [
            (tier, data)
            for tier, data in tier_stats.items()
            if data["total"] > 0 and data["solved"] < data["total"]
        ]
        weak_tiers.sort(key=lambda x: x[1]["solved"] / x[1]["total"] if x[1]["total"] else 1.0)
        if weak_tiers and len(recs) < 3:
            tier, data = weak_tiers[0]
            recs.append(
                f"Practice tier-{tier} problems"
                f" — solved {data['solved']}/{data['total']} this session"
            )

        return recs[:3]
