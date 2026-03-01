"""QScintilla-based Python code editor widget."""

import sys

from PyQt6.Qsci import QsciLexerPython, QsciScintilla
from PyQt6.QtGui import QFont


def _monospace_font() -> QFont:
    """Return a platform-appropriate monospace font."""
    if sys.platform == "win32":
        family = "Consolas"
    elif sys.platform == "darwin":
        family = "Menlo"
    else:
        family = "DejaVu Sans Mono"
    return QFont(family, 11)


class EditorWidget(QsciScintilla):
    """Python code editor with syntax highlighting, line numbers, and zoom."""

    SCI_GETZOOM = 2374

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        font = _monospace_font()
        self.setFont(font)

        # Python lexer for syntax highlighting
        lexer = QsciLexerPython(self)
        lexer.setFont(font)
        self.setLexer(lexer)

        # Line numbers
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, "0000")

        # Indentation
        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setIndentationGuides(True)

        # Brace matching
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)

    # -- Zoom -----------------------------------------------------------------

    def zoom_in(self) -> None:
        self.zoomIn()

    def zoom_out(self) -> None:
        self.zoomOut()

    # -- API access ------------------------------------------------------------

    def get_code(self) -> str:
        return self.text()

    def set_code(self, text: str) -> None:
        self.setText(text)

    def clear(self) -> None:
        self.setText("")
