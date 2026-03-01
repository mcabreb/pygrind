"""Tests for E4-S03: Session Configuration Dialog."""

from PyQt6.QtWidgets import QLabel, QPushButton, QRadioButton

from pytrainer.models.session import DifficultyMode
from pytrainer.ui.session_config import SessionConfigScreen


class TestRadioButtons:
    """AC: Shows 3 radio buttons: Beginner, Medium, Difficult."""

    def test_three_radio_buttons(self, qtbot):
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        radios = screen.findChildren(QRadioButton)
        assert len(radios) == 3

    def test_radio_labels(self, qtbot):
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        radios = screen.findChildren(QRadioButton)
        texts = {r.text() for r in radios}
        assert "Beginner" in texts
        assert "Medium" in texts
        assert "Difficult" in texts

    def test_default_selection_is_medium(self, qtbot):
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        radios = screen.findChildren(QRadioButton)
        medium = [r for r in radios if r.text() == "Medium"][0]
        assert medium.isChecked()


class TestModeDescriptions:
    """AC: Each mode has description text."""

    def test_beginner_description(self, qtbot):
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        labels = screen.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert "Hints visible" in texts
        assert "solutions available" in texts

    def test_medium_description(self, qtbot):
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        labels = screen.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert "Hints on request" in texts
        assert "no solutions" in texts

    def test_difficult_description(self, qtbot):
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        labels = screen.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert "No hints" in texts
        assert "no solutions" in texts.lower()


class TestSessionConfigSignals:
    """AC: Start and Back buttons emit correct signals."""

    def test_start_emits_mode_selected_with_difficulty(self, qtbot):
        """AC: 'Start Session' button emits signal with selected DifficultyMode enum."""
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        # Select Beginner
        radios = screen.findChildren(QRadioButton)
        beginner = [r for r in radios if r.text() == "Beginner"][0]
        beginner.setChecked(True)

        received = []
        screen.mode_selected.connect(lambda mode: received.append(mode))

        buttons = screen.findChildren(QPushButton)
        start_btn = [b for b in buttons if b.text() == "Start Session"][0]
        start_btn.click()

        assert len(received) == 1
        assert received[0] == DifficultyMode.BEGINNER

    def test_start_emits_medium_by_default(self, qtbot):
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)

        received = []
        screen.mode_selected.connect(lambda mode: received.append(mode))

        buttons = screen.findChildren(QPushButton)
        start_btn = [b for b in buttons if b.text() == "Start Session"][0]
        start_btn.click()

        assert received[0] == DifficultyMode.MEDIUM

    def test_back_button_emits_signal(self, qtbot):
        """AC: 'Back' button returns to main menu."""
        screen = SessionConfigScreen()
        qtbot.addWidget(screen)
        with qtbot.waitSignal(screen.back_requested, timeout=1000):
            buttons = screen.findChildren(QPushButton)
            back_btn = [b for b in buttons if b.text() == "Back"][0]
            back_btn.click()
