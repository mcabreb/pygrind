"""Tests for E7-S06: Analytics section in ResultsScreen."""

import pytest
from PyQt6.QtWidgets import QApplication, QLabel

from pytrainer.models.exercise import Exercise
from pytrainer.models.session import (
    DifficultyMode,
    ProblemState,
    ProblemStatus,
    SessionConfig,
    SessionResult,
)
from pytrainer.ui.results import ResultsScreen


@pytest.fixture(scope="module")
def _qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def screen(_qapp):
    s = ResultsScreen()
    s.show()
    return s


@pytest.fixture
def sample_result():
    config = SessionConfig(mode=DifficultyMode.BEGINNER)
    problems = [
        ProblemState(
            exercise=Exercise(
                id="ex-1", title="Ex 1", tier=1, topic="loops",
                description="", time_estimate=5, test_cases=[],
            ),
            status=ProblemStatus.SOLVED,
            score=10,
            time_spent=60.0,
        ),
    ]
    return SessionResult(
        session_id="s-1",
        date="2026-03-01 12:00",
        config=config,
        problems=problems,
        total_score=10,
        max_score=10,
        time_used=60.0,
    )


class TestAnalyticsInResults:
    """AC: Analytics section displayed in ResultsScreen below score summary."""

    def test_analytics_section_exists(self, screen, sample_result):
        screen.set_results(sample_result)
        assert hasattr(screen, "_analytics_label")

    def test_analytics_shows_content(self, screen, sample_result):
        screen.set_results(sample_result)
        screen.set_analytics(
            tier_stats={1: {"solved": 1, "total": 1}},
            recommendations=["Focus on strings"],
            score_trend=[],
        )
        assert screen._analytics_label.isVisible()
        text = screen._analytics_label.text()
        assert "Tier 1" in text
        assert "Focus on strings" in text

    def test_analytics_with_no_data(self, screen, sample_result):
        screen.set_results(sample_result)
        screen.set_analytics(tier_stats={}, recommendations=[], score_trend=[])
        assert screen._analytics_label.isVisible()

    def test_score_trend_shown(self, screen, sample_result):
        screen.set_results(sample_result)
        screen.set_analytics(
            tier_stats={},
            recommendations=[],
            score_trend=[{"date": "2026-02-28", "score": 50, "max_score": 100}],
        )
        text = screen._analytics_label.text()
        assert "Previous" in text or "Trend" in text or "50" in text
