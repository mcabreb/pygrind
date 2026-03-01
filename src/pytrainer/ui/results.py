"""Session results summary screen — end-of-session display."""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pytrainer.models.session import ProblemStatus, SessionResult

_STATUS_LABELS = {
    ProblemStatus.SOLVED: "Solved",
    ProblemStatus.ATTEMPTED: "Attempted",
    ProblemStatus.UNSOLVED: "Skipped",
}

_STATUS_COLORS = {
    ProblemStatus.SOLVED: "#4CAF50",
    ProblemStatus.ATTEMPTED: "#FF9800",
    ProblemStatus.UNSOLVED: "#9E9E9E",
}

_COLUMNS = ["#", "Title", "Tier", "Status", "Score", "Time", "Attempts"]


class ResultsScreen(QWidget):
    """End-of-session results display with score, table, and navigation."""

    back_to_menu = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Mode label (header)
        self._mode_label = QLabel()
        mode_font = QFont()
        mode_font.setPointSize(14)
        self._mode_label.setFont(mode_font)
        self._mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._mode_label)

        # Score label — large and prominent
        self._score_label = QLabel()
        score_font = QFont()
        score_font.setPointSize(28)
        score_font.setBold(True)
        self._score_label.setFont(score_font)
        self._score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._score_label)

        # Stats row: solved / attempted / skipped
        self._stats_label = QLabel()
        self._stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._stats_label)

        # Session time
        self._time_label = QLabel()
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._time_label)

        layout.addSpacing(16)

        # Per-problem table
        self._table = QTableWidget()
        self._table.setColumnCount(len(_COLUMNS))
        self._table.setHorizontalHeaderLabels(_COLUMNS)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._table)

        layout.addSpacing(16)

        # Analytics section (E7-S06)
        self._analytics_label = QLabel()
        self._analytics_label.setWordWrap(True)
        self._analytics_label.setStyleSheet(
            "background-color: #E3F2FD; padding: 12px; border-radius: 6px;"
        )
        self._analytics_label.setVisible(False)
        layout.addWidget(self._analytics_label)

        layout.addSpacing(16)

        # Return to Main Menu button
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._back_button = QPushButton("Return to Main Menu")
        self._back_button.setMinimumSize(200, 40)
        self._back_button.clicked.connect(self.back_to_menu)
        btn_row.addWidget(self._back_button)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def set_results(self, result: SessionResult) -> None:
        """Populate all widgets from a SessionResult."""
        # Mode header
        mode_name = result.config.mode.value.capitalize()
        self._mode_label.setText(f"Session Mode: {mode_name}")

        # Score
        pct = int(result.total_score / result.max_score * 100) if result.max_score else 0
        self._score_label.setText(f"{result.total_score} / {result.max_score} — {pct}%")

        # Stats
        solved = sum(1 for p in result.problems if p.status == ProblemStatus.SOLVED)
        attempted = sum(1 for p in result.problems if p.status == ProblemStatus.ATTEMPTED)
        skipped = sum(1 for p in result.problems if p.status == ProblemStatus.UNSOLVED)
        self._stats_label.setText(
            f"Solved: {solved}  |  Attempted: {attempted}  |  Skipped: {skipped}"
        )

        # Time
        mins = int(result.time_used) // 60
        secs = int(result.time_used) % 60
        self._time_label.setText(f"Total Time: {mins}:{secs:02d}")

        # Table
        self._table.setRowCount(len(result.problems))
        for row, ps in enumerate(result.problems):
            self._table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self._table.setItem(row, 1, QTableWidgetItem(ps.exercise.title))
            self._table.setItem(row, 2, QTableWidgetItem(str(ps.exercise.tier)))

            status_item = QTableWidgetItem(_STATUS_LABELS[ps.status])
            self._table.setItem(row, 3, status_item)

            self._table.setItem(row, 4, QTableWidgetItem(str(ps.score)))

            t_mins = int(ps.time_spent) // 60
            t_secs = int(ps.time_spent) % 60
            self._table.setItem(row, 5, QTableWidgetItem(f"{t_mins}:{t_secs:02d}"))

            self._table.setItem(row, 6, QTableWidgetItem(str(ps.attempts)))

    def set_analytics(
        self,
        tier_stats: dict[int, dict[str, int]],
        recommendations: list[str],
        score_trend: list[dict[str, Any]],
    ) -> None:
        """Populate the analytics section below the results table."""
        parts: list[str] = []

        # Tier performance
        if tier_stats:
            lines = ["<b>Tier Performance:</b>"]
            for tier in sorted(tier_stats):
                d = tier_stats[tier]
                pct = int(d["solved"] / d["total"] * 100) if d["total"] else 0
                lines.append(f"  Tier {tier}: {d['solved']}/{d['total']} ({pct}%)")
            parts.append("\n".join(lines))

        # Score trend
        if score_trend:
            lines = ["<b>Previous Sessions:</b>"]
            for s in score_trend:
                lines.append(f"  {s['date']}: {s['score']}/{s['max_score']}")
            parts.append("\n".join(lines))

        # Recommendations
        if recommendations:
            lines = ["<b>Recommendations:</b>"]
            for r in recommendations:
                lines.append(f"  • {r}")
            parts.append("\n".join(lines))

        if not parts:
            parts.append("No analytics data available yet. Complete more sessions to see trends.")

        self._analytics_label.setText("\n\n".join(parts))
        self._analytics_label.setVisible(True)
