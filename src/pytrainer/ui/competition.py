"""Competition window — main workspace layout for active sessions."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from pytrainer.ui.editor import EditorWidget
from pytrainer.ui.output import OutputPanel
from pytrainer.ui.problem import ProblemPanel
from pytrainer.ui.timer_widget import TimerWidget


class CompetitionWindow(QWidget):
    """Main competition workspace with problem, editor, output, and timer."""

    run_requested = pyqtSignal()
    submit_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        root_layout = QVBoxLayout(self)

        # Timer at top center
        self.timer_widget = TimerWidget(self)
        root_layout.addWidget(self.timer_widget)

        # Main horizontal splitter: problem panel (left) | editor+output (right)
        self._main_splitter = QSplitter(Qt.Orientation.Horizontal, self)

        # Left: problem panel
        self.problem_panel = ProblemPanel(self)
        self._main_splitter.addWidget(self.problem_panel)

        # Right: vertical splitter — editor on top, output below
        self._right_splitter = QSplitter(Qt.Orientation.Vertical, self)

        # Editor + button bar in a container
        editor_container = QWidget(self)
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)

        self.editor = EditorWidget(self)
        editor_layout.addWidget(self.editor)

        # Button bar
        button_bar = QHBoxLayout()
        button_bar.addStretch()

        self.run_button = QPushButton("Run")
        self.run_button.setMinimumSize(80, 32)
        self.run_button.clicked.connect(self.run_requested)
        button_bar.addWidget(self.run_button)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setMinimumSize(80, 32)
        self.submit_button.clicked.connect(self.submit_requested)
        button_bar.addWidget(self.submit_button)

        editor_layout.addLayout(button_bar)
        self._right_splitter.addWidget(editor_container)

        # Output panel
        self.output_panel = OutputPanel(self)
        self._right_splitter.addWidget(self.output_panel)

        # Initial right splitter ratio: 70% editor, 30% output
        self._right_splitter.setSizes([700, 300])

        self._main_splitter.addWidget(self._right_splitter)

        # Initial main splitter ratio: 35% problem, 65% editor+output
        self._main_splitter.setSizes([350, 650])

        root_layout.addWidget(self._main_splitter)

        # Keyboard shortcut: Ctrl+Enter → Submit
        self._submit_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self._submit_shortcut.activated.connect(self.submit_requested)
