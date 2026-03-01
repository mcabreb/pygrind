"""Session configuration screen — difficulty selection before starting."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from pytrainer.models.session import DifficultyMode

_MODE_INFO = {
    "Beginner": ("Hints visible, solutions available", DifficultyMode.BEGINNER),
    "Medium": ("Hints on request, no solutions", DifficultyMode.MEDIUM),
    "Difficult": ("No hints, no solutions", DifficultyMode.DIFFICULT),
}


class SessionConfigScreen(QWidget):
    """Pre-session screen for selecting difficulty mode."""

    mode_selected = pyqtSignal(DifficultyMode)
    back_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._button_group = QButtonGroup(self)
        self._mode_map: dict[int, DifficultyMode] = {}

        for idx, (label, (desc, mode)) in enumerate(_MODE_INFO.items()):
            radio = QRadioButton(label)
            self._button_group.addButton(radio, idx)
            self._mode_map[idx] = mode
            layout.addWidget(radio)

            desc_label = QLabel(desc)
            desc_label.setContentsMargins(24, 0, 0, 8)
            layout.addWidget(desc_label)

        # Default: Medium
        self._button_group.button(1).setChecked(True)

        layout.addSpacing(20)

        btn_row = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setMinimumSize(120, 40)
        back_btn.clicked.connect(self.back_requested)
        btn_row.addWidget(back_btn)

        start_btn = QPushButton("Start Session")
        start_btn.setMinimumSize(120, 40)
        start_btn.clicked.connect(self._on_start)
        btn_row.addWidget(start_btn)

        layout.addLayout(btn_row)

    def _on_start(self) -> None:
        checked_id = self._button_group.checkedId()
        mode = self._mode_map[checked_id]
        self.mode_selected.emit(mode)
