"""Tests for E4-S01: Application Shell & Screen Navigation."""

import logging
from unittest.mock import patch

from PyQt6.QtWidgets import QStackedWidget, QWidget

from pytrainer.ui.main_window import MainWindow


class TestMainWindowCreation:
    """AC: QApplication starts and shows main window with title 'Python Competition Trainer'."""

    def test_window_title(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert window.windowTitle() == "Python Competition Trainer"

    def test_window_default_size(self, qtbot):
        """AC: Window size defaults to 1200x800, resizable."""
        window = MainWindow()
        qtbot.addWidget(window)
        assert window.width() == 1200
        assert window.height() == 800

    def test_window_is_resizable(self, qtbot):
        """AC: Window is resizable."""
        window = MainWindow()
        qtbot.addWidget(window)
        # Not fixed size — max size should be the Qt default (16777215)
        assert window.maximumWidth() == 16777215


class TestStackedWidget:
    """AC: QStackedWidget enables switching between screens without window recreation."""

    def test_central_widget_is_stacked(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert isinstance(window.centralWidget(), QStackedWidget)

    def test_show_menu_switches_screen(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        menu = QWidget()
        config = QWidget()
        window.register_menu(menu)
        window.register_config(config)
        window.show_config()
        window.show_menu()
        stacked = window.centralWidget()
        assert stacked.currentWidget() is menu

    def test_show_config_switches_screen(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        menu = QWidget()
        config = QWidget()
        window.register_menu(menu)
        window.register_config(config)
        window.show_menu()
        window.show_config()
        stacked = window.centralWidget()
        assert stacked.currentWidget() is config

    def test_screen_navigation_methods_exist(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert callable(getattr(window, "show_menu", None))
        assert callable(getattr(window, "show_config", None))
        assert callable(getattr(window, "show_competition", None))
        assert callable(getattr(window, "show_results", None))


class TestExceptionHandler:
    """AC: Top-level exception handler catches unhandled errors and shows QMessageBox dialog."""

    def test_exception_handler_exists(self, qtbot):
        """The app module should provide an install_exception_handler function."""
        from pytrainer.app import install_exception_handler

        assert callable(install_exception_handler)

    def test_exception_handler_logs_error(self, qtbot, tmp_path):
        """Exception handler should log the exception."""
        from pytrainer.app import install_exception_handler

        with patch("pytrainer.app.QMessageBox") as mock_msgbox:
            install_exception_handler()
            import sys

            handler = sys.excepthook
            try:
                raise ValueError("test error")
            except ValueError:
                exc_info = sys.exc_info()
                handler(exc_info[0], exc_info[1], exc_info[2])
            mock_msgbox.critical.assert_called_once()
            call_args = mock_msgbox.critical.call_args
            assert "test error" in call_args[0][2]


class TestLogging:
    """AC: Logging configured to file at platformdirs user_data_dir with 5MB rotation."""

    def test_configure_logging_creates_handler(self):
        from pytrainer.app import configure_logging

        logger = configure_logging()
        assert isinstance(logger, logging.Logger)
        # Should have at least one handler (RotatingFileHandler)
        rotating_handlers = [
            h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        assert len(rotating_handlers) >= 1

    def test_log_file_rotation_size(self):
        from pytrainer.app import configure_logging

        logger = configure_logging()
        rotating_handlers = [
            h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        handler = rotating_handlers[0]
        assert handler.maxBytes == 5 * 1024 * 1024  # 5MB

    def test_log_file_path_uses_platformdirs(self):
        from pytrainer.app import configure_logging

        logger = configure_logging()
        rotating_handlers = [
            h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        handler = rotating_handlers[0]
        assert "pytrainer" in handler.baseFilename
