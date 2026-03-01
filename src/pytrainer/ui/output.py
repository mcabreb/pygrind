"""Output panel — shows execution results, errors, diffs, and timeouts."""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


def _mono_label(text: str, color: str | None = None) -> QLabel:
    """Create a monospace QLabel with optional color."""
    label = QLabel(text)
    font = QFont("monospace")
    font.setStyleHint(QFont.StyleHint.Monospace)
    label.setFont(font)
    if color:
        label.setStyleSheet(f"color: {color};")
    label.setWordWrap(True)
    return label


class OutputPanel(QWidget):
    """Panel displaying execution results per test case."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)

        self._container = QWidget()
        self._layout = QVBoxLayout(self._container)
        scroll.setWidget(self._container)

    # -- Public API ------------------------------------------------------------

    def show_results(self, results: list[dict]) -> None:
        """Display pass/fail per test case with diff on mismatch."""
        self.clear()
        for r in results:
            num = r.get("test_num", "?")
            status = r.get("status", "unknown")
            if status == "pass":
                label = QLabel(f"✔ Test {num}: Pass")
                label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            else:
                label = QLabel(f"✘ Test {num}: Fail")
                label.setStyleSheet("color: #f44336; font-weight: bold;")
                self._layout.addWidget(label)
                expected = r.get("expected", "")
                actual = r.get("actual", "")
                diff = _mono_label(f"Expected: {expected}\nGot:      {actual}")
                self._layout.addWidget(diff)
                continue
            self._layout.addWidget(label)

    def show_error(self, message: str) -> None:
        """Display an error/traceback message in red monospace."""
        self.clear()
        label = _mono_label(message, color="#f44336")
        self._layout.addWidget(label)

    def show_timeout(self) -> None:
        """Display a timeout indicator."""
        self.clear()
        label = QLabel("⏱ Time Limit Exceeded (10s)")
        label.setStyleSheet("color: #FF9800; font-weight: bold; font-size: 14px;")
        self._layout.addWidget(label)

    def show_safety_violation(self, violations: list[str]) -> None:
        """Display safety scanner violations."""
        self.clear()
        header = QLabel("⚠ Safety Violation")
        header.setStyleSheet("color: #f44336; font-weight: bold;")
        self._layout.addWidget(header)
        for v in violations:
            self._layout.addWidget(_mono_label(v, color="#f44336"))

    def clear(self) -> None:
        """Remove all result widgets."""
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
