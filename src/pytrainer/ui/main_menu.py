"""Main menu screen — landing page with Start, History, Quit buttons."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class MainMenuScreen(QWidget):
    """Landing screen with Start Competition, Session History, and Quit."""

    start_requested = pyqtSignal()
    history_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        from PyQt6.QtWidgets import QLabel

        title = QLabel("Python Competition Trainer")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(40)

        # Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_btn = QPushButton("Start Competition")
        start_btn.setMinimumSize(250, 50)
        start_btn.clicked.connect(self.start_requested)
        btn_layout.addWidget(start_btn)

        history_btn = QPushButton("Session History")
        history_btn.setMinimumSize(250, 50)
        history_btn.clicked.connect(self.history_requested)
        btn_layout.addWidget(history_btn)

        quit_btn = QPushButton("Quit")
        quit_btn.setMinimumSize(250, 50)
        quit_btn.clicked.connect(lambda: QApplication.quit())
        btn_layout.addWidget(quit_btn)

        # Center the button column
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addLayout(btn_layout)
        h_layout.addStretch()
        layout.addLayout(h_layout)
