"""Main application window with screen navigation."""

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget


class MainWindow(QMainWindow):
    """Top-level window hosting all UI screens via QStackedWidget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Python Competition Trainer")
        self.resize(1200, 800)

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        # Placeholder screens — replaced when actual screen widgets are registered
        self._menu_screen: QWidget | None = None
        self._config_screen: QWidget | None = None
        self._competition_screen: QWidget | None = None
        self._results_screen: QWidget | None = None

    # -- Screen registration ---------------------------------------------------

    def register_menu(self, widget: QWidget) -> None:
        self._menu_screen = widget
        self._stack.addWidget(widget)

    def register_config(self, widget: QWidget) -> None:
        self._config_screen = widget
        self._stack.addWidget(widget)

    def register_competition(self, widget: QWidget) -> None:
        self._competition_screen = widget
        self._stack.addWidget(widget)

    def register_results(self, widget: QWidget) -> None:
        self._results_screen = widget
        self._stack.addWidget(widget)

    # -- Navigation ------------------------------------------------------------

    def show_menu(self) -> None:
        if self._menu_screen is not None:
            self._stack.setCurrentWidget(self._menu_screen)

    def show_config(self) -> None:
        if self._config_screen is not None:
            self._stack.setCurrentWidget(self._config_screen)

    def show_competition(self) -> None:
        if self._competition_screen is not None:
            self._stack.setCurrentWidget(self._competition_screen)

    def show_results(self) -> None:
        if self._results_screen is not None:
            self._stack.setCurrentWidget(self._results_screen)
