"""Problem navigation sidebar — list of all problems with status icons."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pytrainer.models.session import ProblemState, ProblemStatus

_STATUS_ICONS = {
    ProblemStatus.UNSOLVED: "⚪",
    ProblemStatus.ATTEMPTED: "🔶",
    ProblemStatus.SOLVED: "✅",
}

_MAX_TITLE_LEN = 20


class ProblemListWidget(QWidget):
    """Sidebar showing all problems with status indicators and navigation."""

    problem_selected = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Next/Prev buttons
        nav_row = QHBoxLayout()
        self._prev_button = QPushButton("◀ Prev")
        self._prev_button.clicked.connect(self._on_prev)
        nav_row.addWidget(self._prev_button)

        self._next_button = QPushButton("Next ▶")
        self._next_button.clicked.connect(self._on_next)
        nav_row.addWidget(self._next_button)
        layout.addLayout(nav_row)

        # Problem list
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_row_changed)
        layout.addWidget(self._list)

        self._problems: list[ProblemState] = []
        self._suppressing_signal = False

    def set_problems(self, problems: list[ProblemState]) -> None:
        """Populate the list from problem states."""
        self._problems = problems
        self._suppressing_signal = True
        self._list.clear()
        for i, ps in enumerate(problems):
            title = ps.exercise.title
            if len(title) > _MAX_TITLE_LEN:
                title = title[:_MAX_TITLE_LEN] + "..."
            icon = _STATUS_ICONS[ps.status]
            self._list.addItem(f"{icon} {i + 1}. {title}")
        self._suppressing_signal = False

    def set_current(self, index: int) -> None:
        """Highlight the given problem index."""
        self._suppressing_signal = True
        self._list.setCurrentRow(index)
        self._suppressing_signal = False

    def update_status(self, index: int, status: ProblemStatus) -> None:
        """Update the status icon for a single problem."""
        if 0 <= index < len(self._problems):
            self._problems[index].status = status
            item = self._list.item(index)
            if item is not None:
                title = self._problems[index].exercise.title
                if len(title) > _MAX_TITLE_LEN:
                    title = title[:_MAX_TITLE_LEN] + "..."
                icon = _STATUS_ICONS[status]
                item.setText(f"{icon} {index + 1}. {title}")

    def _on_row_changed(self, row: int) -> None:
        if not self._suppressing_signal and row >= 0:
            self.problem_selected.emit(row)

    def _on_prev(self) -> None:
        current = self._list.currentRow()
        if current > 0:
            self._list.setCurrentRow(current - 1)

    def _on_next(self) -> None:
        current = self._list.currentRow()
        if current < self._list.count() - 1:
            self._list.setCurrentRow(current + 1)
