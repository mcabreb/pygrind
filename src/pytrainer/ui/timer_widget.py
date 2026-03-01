"""Timer widget — countdown display with color thresholds and pause indicator."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class TimerWidget(QWidget):
    """Prominent countdown display in HH:MM:SS format."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._time_label = QLabel("00:00:00")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self._time_label.setFont(font)
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._time_label)

        self._pause_label = QLabel("PAUSED")
        pause_font = QFont()
        pause_font.setPointSize(14)
        pause_font.setBold(True)
        self._pause_label.setFont(pause_font)
        self._pause_label.setStyleSheet("color: #FF9800;")
        self._pause_label.setVisible(False)
        layout.addWidget(self._pause_label)

    def update_time(self, remaining_secs: int) -> None:
        """Refresh the display with the given remaining seconds."""
        hours = remaining_secs // 3600
        minutes = (remaining_secs % 3600) // 60
        seconds = remaining_secs % 60
        self._time_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        if remaining_secs <= 300:
            self._time_label.setStyleSheet("color: #f44336; font-weight: bold;")
        elif remaining_secs <= 1800:
            self._time_label.setStyleSheet("color: #FF9800;")
        else:
            self._time_label.setStyleSheet("")

    def set_paused(self, paused: bool) -> None:
        """Toggle the PAUSED indicator."""
        self._pause_label.setVisible(paused)
