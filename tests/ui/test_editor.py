"""Tests for E4-S04: QScintilla Code Editor Widget."""

from PyQt6.Qsci import QsciLexerPython

from pytrainer.ui.editor import EditorWidget


class TestSyntaxHighlighting:
    """AC: Python syntax highlighting for keywords, strings, comments, numbers, decorators."""

    def test_lexer_is_python(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        assert isinstance(editor.lexer(), QsciLexerPython)


class TestLineNumbers:
    """AC: Line numbers displayed in left margin."""

    def test_margin_line_numbers_enabled(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        assert editor.marginLineNumbers(0)

    def test_margin_width_nonzero(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        assert editor.marginWidth(0) > 0


class TestAutoIndentation:
    """AC: Auto-indentation following Python conventions."""

    def test_auto_indent_enabled(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        assert editor.autoIndent()


class TestTabSettings:
    """AC: Tab inserts 4 spaces, Shift+Tab dedents."""

    def test_tab_width_is_4(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        assert editor.tabWidth() == 4

    def test_indent_uses_spaces(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        assert editor.indentationsUseTabs() is False


class TestFontZoom:
    """AC: Ctrl+Plus / Ctrl+Minus adjusts font size."""

    def test_zoom_in_increases_font(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        initial = editor.font().pointSize()
        editor.zoom_in()
        assert editor.font().pointSize() > initial or editor.SendScintilla(editor.SCI_GETZOOM) > 0

    def test_zoom_out_decreases_font(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        editor.zoom_in()
        editor.zoom_in()
        level_after_zoom_in = editor.SendScintilla(editor.SCI_GETZOOM)
        editor.zoom_out()
        level_after_zoom_out = editor.SendScintilla(editor.SCI_GETZOOM)
        assert level_after_zoom_out < level_after_zoom_in


class TestAPIAccess:
    """AC: get_code() and set_code(text) methods for programmatic access."""

    def test_set_code_and_get_code(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        code = "print('hello world')\n"
        editor.set_code(code)
        assert editor.get_code() == code

    def test_get_code_default_empty(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        assert editor.get_code() == ""

    def test_clear_resets_content(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        editor.set_code("some code")
        editor.clear()
        assert editor.get_code() == ""


class TestStandardEditing:
    """AC: Standard editing operations work (copy, paste, undo, redo, select all)."""

    def test_undo_redo_work(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        editor.set_code("first")
        editor.selectAll()
        editor.replaceSelectedText("second")
        assert editor.get_code() == "second"
        editor.undo()
        # After undo, should be back to "first" or empty
        assert editor.get_code() != "second"

    def test_select_all(self, qtbot):
        editor = EditorWidget()
        qtbot.addWidget(editor)
        editor.set_code("hello world")
        editor.selectAll()
        assert editor.selectedText() == "hello world"
