"""Tests for E4-S02: Main Menu Screen."""

from PyQt6.QtWidgets import QApplication, QLabel, QPushButton

from pytrainer.ui.main_menu import MainMenuScreen


class TestMainMenuDisplay:
    """AC: Shows application title 'Python Competition Trainer' in large font."""

    def test_title_label_text(self, qtbot):
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        labels = screen.findChildren(QLabel)
        title_labels = [lb for lb in labels if "Python Competition Trainer" in lb.text()]
        assert len(title_labels) == 1

    def test_title_label_large_font(self, qtbot):
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        labels = screen.findChildren(QLabel)
        title_labels = [lb for lb in labels if "Python Competition Trainer" in lb.text()]
        assert title_labels[0].font().pointSize() >= 24


class TestMainMenuButtons:
    """AC: 3 buttons — Start Competition, Session History, Quit."""

    def test_start_button_exists(self, qtbot):
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        buttons = screen.findChildren(QPushButton)
        texts = [b.text() for b in buttons]
        assert "Start Competition" in texts

    def test_history_button_exists(self, qtbot):
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        buttons = screen.findChildren(QPushButton)
        texts = [b.text() for b in buttons]
        assert "Session History" in texts

    def test_quit_button_exists(self, qtbot):
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        buttons = screen.findChildren(QPushButton)
        texts = [b.text() for b in buttons]
        assert "Quit" in texts


class TestMainMenuSignals:
    """AC: Buttons emit correct signals or perform correct actions."""

    def test_start_button_emits_signal(self, qtbot):
        """AC: 'Start Competition' button navigates to session config dialog."""
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        with qtbot.waitSignal(screen.start_requested, timeout=1000):
            buttons = screen.findChildren(QPushButton)
            start_btn = [b for b in buttons if b.text() == "Start Competition"][0]
            start_btn.click()

    def test_history_button_emits_signal(self, qtbot):
        """AC: 'Session History' button navigates to history screen."""
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        with qtbot.waitSignal(screen.history_requested, timeout=1000):
            buttons = screen.findChildren(QPushButton)
            history_btn = [b for b in buttons if b.text() == "Session History"][0]
            history_btn.click()

    def test_quit_button_calls_quit(self, qtbot, monkeypatch):
        """AC: 'Quit' button exits the application cleanly."""
        screen = MainMenuScreen()
        qtbot.addWidget(screen)
        quit_called = []
        monkeypatch.setattr(QApplication, "quit", lambda: quit_called.append(True))
        buttons = screen.findChildren(QPushButton)
        quit_btn = [b for b in buttons if b.text() == "Quit"][0]
        quit_btn.click()
        assert quit_called
