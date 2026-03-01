"""PyTrainer application entry point."""

import logging
import logging.handlers
import sys
import traceback
from pathlib import Path

from platformdirs import user_data_dir

# Lazy import to allow tests to import functions without full Qt init
QMessageBox = None


def _get_qmessagebox():
    global QMessageBox  # noqa: N814
    if QMessageBox is None:
        from PyQt6.QtWidgets import QMessageBox  # noqa: N814

    return QMessageBox


def configure_logging() -> logging.Logger:
    """Configure rotating file logging at platformdirs user_data_dir."""
    log_dir = Path(user_data_dir("pytrainer"))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "pytrainer.log"

    logger = logging.getLogger("pytrainer")
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers on repeated calls
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) for h in logger.handlers):
        handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
        )
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def install_exception_handler() -> None:
    """Install a global exception handler that logs and shows a dialog."""

    def _handle_exception(exc_type, exc_value, exc_tb):
        logger = logging.getLogger("pytrainer")
        tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        logger.critical("Unhandled exception:\n%s", tb_text)

        msgbox = _get_qmessagebox()
        msgbox.critical(
            None,
            "Unexpected Error",
            f"{exc_type.__name__}: {exc_value}",
        )

    sys.excepthook = _handle_exception


def main(argv: list[str] | None = None) -> None:
    """Launch the PyTrainer application.

    With ``--version`` or without a GUI environment, prints version info and exits.
    """
    if argv is None:
        argv = sys.argv

    if "--version" in argv or "-V" in argv:
        from pytrainer import __version__

        print(f"PyTrainer v{__version__} — Python Competition Trainer")
        sys.exit(0)

    from PyQt6.QtWidgets import QApplication

    from pytrainer.ui.main_window import MainWindow

    app = QApplication(argv)

    configure_logging()
    install_exception_handler()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
