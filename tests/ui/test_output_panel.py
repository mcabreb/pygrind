"""Tests for E4-S06: Output Panel."""

from PyQt6.QtWidgets import QLabel

from pytrainer.ui.output import OutputPanel


class TestPassFailDisplay:
    """AC: Shows pass/fail status per test case with green checkmark / red X."""

    def test_show_results_pass(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        results = [{"status": "pass", "test_num": 1}]
        panel.show_results(results)
        labels = panel.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        # Should contain a pass indicator
        assert any(c in texts for c in ["✓", "Pass", "PASS", "pass", "✔"])

    def test_show_results_fail(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        results = [
            {
                "status": "fail",
                "test_num": 1,
                "expected": "8",
                "actual": "9",
            }
        ]
        panel.show_results(results)
        labels = panel.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert any(c in texts for c in ["✗", "Fail", "FAIL", "fail", "✘", "✖"])

    def test_show_results_multiple(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        results = [
            {"status": "pass", "test_num": 1},
            {"status": "fail", "test_num": 2, "expected": "8", "actual": "9"},
        ]
        panel.show_results(results)
        labels = panel.findChildren(QLabel)
        # Should have labels for both test cases
        assert len(labels) >= 2


class TestErrorDisplay:
    """AC: Displays error messages and tracebacks in monospace red text."""

    def test_show_error(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        panel.show_error("NameError: name 'foo' is not defined")
        labels = panel.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert "NameError" in texts

    def test_error_has_red_style(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        panel.show_error("SyntaxError: invalid syntax")
        labels = panel.findChildren(QLabel)
        error_labels = [lb for lb in labels if "SyntaxError" in lb.text()]
        assert len(error_labels) >= 1
        style = error_labels[0].styleSheet()
        assert "red" in style.lower() or "#f44336" in style.lower() or "#ff" in style.lower()


class TestDiffDisplay:
    """AC: Shows expected vs actual diff on output mismatch."""

    def test_diff_shown_on_mismatch(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        results = [
            {
                "status": "fail",
                "test_num": 1,
                "expected": "8",
                "actual": "9",
            }
        ]
        panel.show_results(results)
        labels = panel.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert "8" in texts
        assert "9" in texts


class TestTimeoutDisplay:
    """AC: Shows 'Time Limit Exceeded (10s)' message on timeout."""

    def test_show_timeout(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        panel.show_timeout()
        labels = panel.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert "Time Limit Exceeded" in texts
        assert "10s" in texts


class TestClear:
    """AC: clear() method resets the panel between executions."""

    def test_clear_removes_content(self, qtbot):
        panel = OutputPanel()
        qtbot.addWidget(panel)
        panel.show_error("some error")
        labels_before = panel.findChildren(QLabel)
        assert len(labels_before) > 0
        panel.clear()
        labels_after = panel.findChildren(QLabel)
        assert len(labels_after) == 0
