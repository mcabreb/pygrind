"""Tests for CompetitionWindow — E5-S02 acceptance criteria."""

import sys
from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSplitter, QWidget

# Mock QScintilla before importing competition module
_noop = lambda *a, **kw: None  # noqa: E731
_QsciBase = type(
    "QsciScintilla",
    (QWidget,),
    {
        "SCI_GETZOOM": 2374,
        "BraceMatch": type("BraceMatch", (), {"SloppyBraceMatch": 0}),
        "setLexer": _noop,
        "setFont": _noop,
        "setMarginLineNumbers": _noop,
        "setMarginWidth": _noop,
        "setAutoIndent": _noop,
        "setTabWidth": _noop,
        "setIndentationsUseTabs": _noop,
        "setIndentationGuides": _noop,
        "setBraceMatching": _noop,
        "text": lambda self: "",
        "setText": _noop,
        "zoomIn": _noop,
        "zoomOut": _noop,
    },
)
_qsci_mock = MagicMock()
_qsci_mock.QsciScintilla = _QsciBase
_qsci_mock.QsciLexerPython = MagicMock()
sys.modules.setdefault("PyQt6.Qsci", _qsci_mock)

from pytrainer.ui.competition import CompetitionWindow  # noqa: E402

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def competition_window(qtbot):
    """Create a CompetitionWindow."""
    win = CompetitionWindow()
    qtbot.addWidget(win)
    return win


# ---------------------------------------------------------------------------
# AC-1: Problem panel occupies left side (30-40% width)
# AC-2: Code editor occupies right side (60-70% width) with Run/Submit buttons
# ---------------------------------------------------------------------------


class TestLayout:
    def test_has_horizontal_splitter(self, competition_window):
        """AC-1/2: Main layout uses QSplitter for left/right."""
        splitters = competition_window.findChildren(QSplitter)
        h_splitters = [s for s in splitters if s.orientation() == Qt.Orientation.Horizontal]
        assert len(h_splitters) >= 1, "No horizontal QSplitter found"

    def test_problem_panel_on_left(self, competition_window):
        """AC-1: Problem panel is present."""
        assert competition_window.problem_panel is not None

    def test_editor_on_right(self, competition_window):
        """AC-2: Editor widget exists."""
        assert competition_window.editor is not None

    def test_run_button_exists(self, competition_window):
        """AC-2: Run button exists."""
        assert competition_window.run_button is not None
        assert competition_window.run_button.text() == "Run"

    def test_submit_button_exists(self, competition_window):
        """AC-2: Submit button exists."""
        assert competition_window.submit_button is not None
        assert competition_window.submit_button.text() == "Submit"


# ---------------------------------------------------------------------------
# AC-3: Output panel below the editor (collapsible or resizable)
# ---------------------------------------------------------------------------


class TestOutputPanel:
    def test_output_panel_exists(self, competition_window):
        """AC-3: Output panel widget exists."""
        assert competition_window.output_panel is not None

    def test_right_side_has_vertical_splitter(self, competition_window):
        """AC-3: Right side uses vertical splitter for editor/output."""
        splitters = competition_window.findChildren(QSplitter)
        vertical = [s for s in splitters if s.orientation() == Qt.Orientation.Vertical]
        assert len(vertical) >= 1, "No vertical QSplitter for editor/output"


# ---------------------------------------------------------------------------
# AC-4: Timer widget prominently at the top center
# ---------------------------------------------------------------------------


class TestTimerWidget:
    def test_timer_widget_exists(self, competition_window):
        """AC-4: Timer widget is present."""
        assert competition_window.timer_widget is not None


# ---------------------------------------------------------------------------
# AC-5: QSplitter allows user to resize panels
# ---------------------------------------------------------------------------


class TestSplitterResize:
    def test_main_splitter_is_resizable(self, competition_window):
        """AC-5: Main splitter has at least 2 children."""
        splitters = competition_window.findChildren(QSplitter)
        main_splitter = [s for s in splitters if s.orientation() == Qt.Orientation.Horizontal]
        assert len(main_splitter) >= 1
        assert main_splitter[0].count() >= 2


# ---------------------------------------------------------------------------
# AC-6: Ctrl+Enter triggers Submit from anywhere in the editor
# ---------------------------------------------------------------------------


class TestKeyboardShortcut:
    def test_submit_shortcut_exists(self, competition_window):
        """AC-6: Ctrl+Return shortcut is registered."""
        assert competition_window._submit_shortcut is not None


# ---------------------------------------------------------------------------
# Signal wiring tests
# ---------------------------------------------------------------------------


class TestSignals:
    def test_run_clicked_signal(self, competition_window, qtbot):
        """Run button emits run_requested signal."""
        with qtbot.waitSignal(competition_window.run_requested, timeout=1000):
            competition_window.run_button.click()

    def test_submit_clicked_signal(self, competition_window, qtbot):
        """Submit button emits submit_requested signal."""
        with qtbot.waitSignal(competition_window.submit_requested, timeout=1000):
            competition_window.submit_button.click()
