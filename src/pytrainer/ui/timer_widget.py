"""Timer widget — dual count-up display: per-problem and global session timer."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


def _format_time(secs: int) -> str:
    """Format seconds as HH:MM:SS or MM:SS depending on magnitude."""
    hours = secs // 3600
    minutes = (secs % 3600) // 60
    seconds = secs % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


class TimerWidget(QWidget):
    """Displays two count-up timers: per-problem and global session."""

    STYLE_NORMAL = ""
    STYLE_YELLOW = "color: #FF9800; font-weight: bold;"
    STYLE_RED = "color: #f44336; font-weight: bold;"
    STYLE_OVERTIME_BG = (
        "color: #f44336; font-weight: bold; "
        "background-color: #FFEBEE; border-radius: 4px; padding: 2px 6px;"
    )

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        caption_font = QFont()
        caption_font.setPointSize(12)

        # Problem timer (left)
        problem_caption = QLabel("Problem:")
        problem_caption.setFont(caption_font)
        problem_caption.setStyleSheet("color: #666;")
        layout.addWidget(problem_caption)

        self._problem_label = QLabel("00:00")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self._problem_label.setFont(font)
        self._problem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._problem_label)

        # Spacer
        layout.addWidget(QLabel("    "))

        # Session timer (right)
        session_caption = QLabel("Session:")
        session_caption.setFont(caption_font)
        session_caption.setStyleSheet("color: #666;")
        layout.addWidget(session_caption)

        self._session_label = QLabel("00:00")
        session_font = QFont()
        session_font.setPointSize(22)
        session_font.setBold(True)
        self._session_label.setFont(session_font)
        self._session_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._session_label)

        # Overtime indicator
        self._overtime_label = QLabel("OVERTIME")
        overtime_font = QFont()
        overtime_font.setPointSize(13)
        overtime_font.setBold(True)
        self._overtime_label.setFont(overtime_font)
        self._overtime_label.setStyleSheet(
            "color: #f44336; background-color: #FFEBEE; "
            "border-radius: 4px; padding: 2px 8px;"
        )
        self._overtime_label.setVisible(False)
        layout.addWidget(self._overtime_label)

        self._pause_label = QLabel("PAUSED")
        pause_font = QFont()
        pause_font.setPointSize(14)
        pause_font.setBold(True)
        self._pause_label.setFont(pause_font)
        self._pause_label.setStyleSheet("color: #FF9800;")
        self._pause_label.setVisible(False)
        layout.addWidget(self._pause_label)

    def update_problem_time(self, elapsed_secs: int) -> None:
        """Update the per-problem timer display."""
        self._problem_label.setText(_format_time(elapsed_secs))

    def update_session_time(self, elapsed_secs: int) -> None:
        """Update the global session timer display."""
        self._session_label.setText(_format_time(elapsed_secs))

    def set_session_warning(self, level: str) -> None:
        """Set session timer visual state: 'normal', 'yellow', 'red', or 'overtime'."""
        if level == "yellow":
            self._session_label.setStyleSheet(self.STYLE_YELLOW)
            self._overtime_label.setVisible(False)
        elif level == "red":
            self._session_label.setStyleSheet(self.STYLE_RED)
            self._overtime_label.setVisible(False)
        elif level == "overtime":
            self._session_label.setStyleSheet(self.STYLE_OVERTIME_BG)
            self._overtime_label.setVisible(True)
        else:
            self._session_label.setStyleSheet(self.STYLE_NORMAL)
            self._overtime_label.setVisible(False)

    def set_paused(self, paused: bool) -> None:
        """Toggle the PAUSED indicator."""
        self._pause_label.setVisible(paused)
