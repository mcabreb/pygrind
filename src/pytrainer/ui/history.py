"""Session history screen — displays past session summaries from the database."""

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

_COLUMNS = ["Date", "Mode", "Score", "Max", "%", "Time"]


class HistoryScreen(QWidget):
    """Displays a table of past sessions with a back button."""

    back_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Session History")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(16)

        # Table
        self._table = QTableWidget()
        self._table.setColumnCount(len(_COLUMNS))
        self._table.setHorizontalHeaderLabels(_COLUMNS)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._table)

        # Empty state label
        self._empty_label = QLabel("No sessions recorded yet. Start a competition first!")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.setStyleSheet("color: #999; font-size: 14px;")
        self._empty_label.setVisible(False)
        layout.addWidget(self._empty_label)

        layout.addSpacing(16)

        # Back button
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        back_btn = QPushButton("Back to Menu")
        back_btn.setMinimumSize(200, 40)
        back_btn.clicked.connect(self.back_requested)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def set_sessions(self, sessions: list[dict[str, Any]]) -> None:
        """Populate the table from database session rows."""
        if not sessions:
            self._table.setRowCount(0)
            self._table.setVisible(False)
            self._empty_label.setVisible(True)
            return

        self._table.setVisible(True)
        self._empty_label.setVisible(False)
        self._table.setRowCount(len(sessions))

        for row, s in enumerate(sessions):
            self._table.setItem(row, 0, QTableWidgetItem(s.get("date", "")))
            self._table.setItem(row, 1, QTableWidgetItem(s.get("mode", "")))

            score = s.get("total_score", 0)
            max_score = s.get("max_score", 0)
            pct = int(score / max_score * 100) if max_score else 0

            self._table.setItem(row, 2, QTableWidgetItem(str(score)))
            self._table.setItem(row, 3, QTableWidgetItem(str(max_score)))
            self._table.setItem(row, 4, QTableWidgetItem(f"{pct}%"))

            time_used = s.get("time_used", 0.0)
            mins = int(time_used) // 60
            secs = int(time_used) % 60
            self._table.setItem(row, 5, QTableWidgetItem(f"{mins}:{secs:02d}"))
