"""SQLite persistence layer for session history, analytics, and exercise flags."""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from pytrainer.models.session import ProblemStatus, SessionResult

log = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    mode TEXT NOT NULL,
    total_score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,
    time_used REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS problem_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    exercise_id TEXT NOT NULL,
    title TEXT NOT NULL,
    tier INTEGER NOT NULL,
    topic TEXT NOT NULL,
    status TEXT NOT NULL,
    score INTEGER NOT NULL,
    attempts INTEGER NOT NULL,
    time_spent REAL NOT NULL,
    hint_viewed INTEGER NOT NULL DEFAULT 0,
    solution_viewed INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS exercise_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_id TEXT NOT NULL,
    session_id TEXT,
    timestamp TEXT NOT NULL,
    comment TEXT,
    UNIQUE(exercise_id, session_id)
);
"""


class Database:
    """SQLite database for session persistence and analytics."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @property
    def db_path(self) -> Path:
        return self._db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        conn = self._connect()
        conn.executescript(_SCHEMA)
        conn.commit()
        conn.close()

    def save_session(self, result: SessionResult) -> None:
        """Save a complete session with all problem results in a transaction."""
        conn = self._connect()
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO sessions"
                " (session_id, date, mode, total_score, max_score, time_used)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (
                    result.session_id,
                    result.date,
                    result.config.mode.value,
                    result.total_score,
                    result.max_score,
                    result.time_used,
                ),
            )
            for ps in result.problems:
                conn.execute(
                    "INSERT INTO problem_results "
                    "(session_id, exercise_id, title, tier, topic, status, score, attempts, "
                    "time_spent, hint_viewed, solution_viewed) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        result.session_id,
                        ps.exercise.id,
                        ps.exercise.title,
                        ps.exercise.tier,
                        ps.exercise.topic,
                        ps.status.value,
                        ps.score,
                        ps.attempts,
                        ps.time_spent,
                        int(ps.hint_viewed),
                        int(ps.solution_viewed),
                    ),
                )
        conn.close()

    def get_sessions(self) -> list[dict[str, Any]]:
        """Return session summaries ordered by date descending."""
        conn = self._connect()
        rows = conn.execute(
            "SELECT session_id, date, mode, total_score, max_score, time_used "
            "FROM sessions ORDER BY date DESC"
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_session_detail(self, session_id: str) -> dict[str, Any] | None:
        """Return a single session with all problem results."""
        conn = self._connect()
        sess = conn.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
        if sess is None:
            conn.close()
            return None
        problems = conn.execute(
            "SELECT * FROM problem_results WHERE session_id = ? ORDER BY id",
            (session_id,),
        ).fetchall()
        conn.close()
        result = dict(sess)
        result["problems"] = [dict(p) for p in problems]
        return result

    def get_topic_stats(self, last_n: int | None = None) -> dict[str, dict[str, int]]:
        """Return per-topic solve rates. Optionally limit to last N sessions."""
        conn = self._connect()
        if last_n is not None:
            session_ids = conn.execute(
                "SELECT session_id FROM sessions ORDER BY date DESC LIMIT ?",
                (last_n,),
            ).fetchall()
            ids = [r["session_id"] for r in session_ids]
            if not ids:
                conn.close()
                return {}
            placeholders = ",".join("?" * len(ids))
            rows = conn.execute(
                f"SELECT topic, status FROM problem_results WHERE session_id IN ({placeholders})",
                ids,
            ).fetchall()
        else:
            rows = conn.execute("SELECT topic, status FROM problem_results").fetchall()
        conn.close()

        stats: dict[str, dict[str, int]] = {}
        for row in rows:
            topic = row["topic"]
            if topic not in stats:
                stats[topic] = {"solved": 0, "total": 0}
            stats[topic]["total"] += 1
            if row["status"] == ProblemStatus.SOLVED.value:
                stats[topic]["solved"] += 1
        return stats

    def save_flag(
        self, exercise_id: str, session_id: str | None, comment: str | None
    ) -> bool:
        """Save an exercise flag. Returns False if duplicate."""
        conn = self._connect()
        try:
            with conn:
                conn.execute(
                    "INSERT INTO exercise_flags (exercise_id, session_id, timestamp, comment) "
                    "VALUES (?, ?, ?, ?)",
                    (exercise_id, session_id, datetime.now().isoformat(), comment),
                )
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def get_flags(self) -> list[dict[str, Any]]:
        """Return all exercise flags ordered by timestamp descending."""
        conn = self._connect()
        rows = conn.execute(
            "SELECT exercise_id, session_id, timestamp, comment "
            "FROM exercise_flags ORDER BY timestamp DESC"
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]
