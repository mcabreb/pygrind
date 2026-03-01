"""Tests for E7-S05: SQLite Persistence Layer."""

import sqlite3

import pytest

from pytrainer.models.exercise import Exercise
from pytrainer.models.session import (
    DifficultyMode,
    ProblemState,
    ProblemStatus,
    SessionConfig,
    SessionResult,
)
from pytrainer.storage.database import Database


@pytest.fixture
def db(tmp_path):
    """Create a Database with an isolated temp path."""
    return Database(tmp_path / "test.db")


@pytest.fixture
def sample_result():
    """Build a SessionResult with 3 problems for testing."""
    config = SessionConfig(mode=DifficultyMode.BEGINNER)
    problems = []
    for i in range(3):
        ex = Exercise(
            id=f"ex-{i}",
            title=f"Exercise {i}",
            tier=i + 1,
            topic=["loops", "strings", "math"][i],
            description=f"Desc {i}",
            time_estimate=5,
            test_cases=[],
        )
        ps = ProblemState(
            exercise=ex,
            status=[ProblemStatus.SOLVED, ProblemStatus.ATTEMPTED, ProblemStatus.UNSOLVED][i],
            score=[10, 0, 0][i],
            attempts=[1, 2, 0][i],
            time_spent=[60.0, 120.0, 0.0][i],
            hint_viewed=[True, False, False][i],
            solution_viewed=[False, False, False][i],
        )
        problems.append(ps)

    return SessionResult(
        session_id="sess-001",
        date="2026-03-01 12:00",
        config=config,
        problems=problems,
        total_score=10,
        max_score=65,
        time_used=180.0,
    )


class TestSchemaCreation:
    """AC: Schema auto-created on first run."""

    def test_tables_created(self, db):
        conn = sqlite3.connect(db.db_path)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        assert "sessions" in tables
        assert "problem_results" in tables
        assert "exercise_flags" in tables

    def test_db_file_exists(self, db):
        assert db.db_path.exists()


class TestSaveSession:
    """AC: save_session writes session + problem results in a transaction."""

    def test_save_and_count(self, db, sample_result):
        db.save_session(sample_result)
        conn = sqlite3.connect(db.db_path)
        sess_count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        prob_count = conn.execute("SELECT COUNT(*) FROM problem_results").fetchone()[0]
        conn.close()
        assert sess_count == 1
        assert prob_count == 3

    def test_session_fields_stored(self, db, sample_result):
        db.save_session(sample_result)
        conn = sqlite3.connect(db.db_path)
        row = conn.execute("SELECT * FROM sessions WHERE session_id = ?", ("sess-001",)).fetchone()
        conn.close()
        assert row is not None


class TestGetSessions:
    """AC: get_sessions returns session summaries ordered by date descending."""

    def test_returns_empty_initially(self, db):
        assert db.get_sessions() == []

    def test_returns_saved_sessions(self, db, sample_result):
        db.save_session(sample_result)
        sessions = db.get_sessions()
        assert len(sessions) == 1
        assert sessions[0]["session_id"] == "sess-001"

    def test_ordered_by_date_desc(self, db, sample_result):
        db.save_session(sample_result)
        # Save a second session with a later date
        result2 = SessionResult(
            session_id="sess-002",
            date="2026-03-02 12:00",
            config=sample_result.config,
            problems=sample_result.problems,
            total_score=20,
            max_score=65,
            time_used=200.0,
        )
        db.save_session(result2)
        sessions = db.get_sessions()
        assert sessions[0]["session_id"] == "sess-002"
        assert sessions[1]["session_id"] == "sess-001"


class TestGetSessionDetail:
    """AC: get_session_detail returns full session with all problem results."""

    def test_returns_none_for_missing(self, db):
        assert db.get_session_detail("nonexistent") is None

    def test_returns_session_with_problems(self, db, sample_result):
        db.save_session(sample_result)
        detail = db.get_session_detail("sess-001")
        assert detail is not None
        assert detail["session_id"] == "sess-001"
        assert len(detail["problems"]) == 3

    def test_problem_fields(self, db, sample_result):
        db.save_session(sample_result)
        detail = db.get_session_detail("sess-001")
        prob = detail["problems"][0]
        assert prob["exercise_id"] == "ex-0"
        assert prob["score"] == 10


class TestGetTopicStats:
    """AC: get_topic_stats returns per-topic solve rates for analytics."""

    def test_empty_db_returns_empty(self, db):
        assert db.get_topic_stats() == {}

    def test_returns_topic_solve_rates(self, db, sample_result):
        db.save_session(sample_result)
        stats = db.get_topic_stats()
        assert "loops" in stats
        assert stats["loops"]["solved"] == 1
        assert stats["loops"]["total"] == 1

    def test_aggregates_across_sessions(self, db, sample_result):
        db.save_session(sample_result)
        # Save another session with same topics
        result2 = SessionResult(
            session_id="sess-002",
            date="2026-03-02 12:00",
            config=sample_result.config,
            problems=sample_result.problems,
            total_score=10,
            max_score=65,
            time_used=180.0,
        )
        db.save_session(result2)
        stats = db.get_topic_stats()
        assert stats["loops"]["total"] == 2


class TestFlagStorage:
    """AC: exercise_flags table supports flag operations."""

    def test_save_flag(self, db):
        db.save_flag("ex-1", "sess-001", "Bad test case")
        flags = db.get_flags()
        assert len(flags) == 1
        assert flags[0]["exercise_id"] == "ex-1"
        assert flags[0]["comment"] == "Bad test case"

    def test_duplicate_prevention(self, db):
        db.save_flag("ex-1", "sess-001", "First flag")
        db.save_flag("ex-1", "sess-001", "Duplicate")
        flags = db.get_flags()
        assert len(flags) == 1

    def test_different_sessions_allowed(self, db):
        db.save_flag("ex-1", "sess-001", "First")
        db.save_flag("ex-1", "sess-002", "Second")
        flags = db.get_flags()
        assert len(flags) == 2
