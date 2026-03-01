"""Tests for E4-S05: Problem Display Panel."""

from PyQt6.QtWidgets import QLabel, QTextEdit

from pytrainer.models.exercise import Exercise, TestCase
from pytrainer.ui.problem import ProblemPanel


def _make_exercise(tmp_path):
    """Create a minimal Exercise for testing."""
    in_file = tmp_path / "01.in"
    out_file = tmp_path / "01.out"
    in_file.write_text("5 3\n")
    out_file.write_text("8\n")
    tc = TestCase(input_path=in_file, output_path=out_file)
    return Exercise(
        id="test-ex",
        title="Sum Two Numbers",
        tier=2,
        topic="math",
        description="Given two integers, print their sum.",
        time_estimate=5,
        test_cases=[tc],
    )


class TestTitleDisplay:
    """AC: Displays exercise title in bold, large font."""

    def test_title_shown_after_set_exercise(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        labels = panel.findChildren(QLabel)
        title_labels = [lb for lb in labels if "Sum Two Numbers" in lb.text()]
        assert len(title_labels) >= 1

    def test_title_font_is_bold(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        labels = panel.findChildren(QLabel)
        title_labels = [lb for lb in labels if "Sum Two Numbers" in lb.text()]
        assert title_labels[0].font().bold()

    def test_title_font_is_large(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        labels = panel.findChildren(QLabel)
        title_labels = [lb for lb in labels if "Sum Two Numbers" in lb.text()]
        assert title_labels[0].font().pointSize() >= 16


class TestTierBadge:
    """AC: Shows tier badge with color coding."""

    def test_tier_badge_shows_tier(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        labels = panel.findChildren(QLabel)
        # Should have a label containing tier info
        tier_labels = [lb for lb in labels if "2" in lb.text() or "Tier" in lb.text()]
        assert len(tier_labels) >= 1

    def test_tier_badge_has_color(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        labels = panel.findChildren(QLabel)
        tier_labels = [lb for lb in labels if "Tier" in lb.text()]
        assert len(tier_labels) >= 1
        # Should have a stylesheet applied
        assert tier_labels[0].styleSheet() != ""


class TestDescription:
    """AC: Renders description text in a scrollable area."""

    def test_description_shown(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        text_edits = panel.findChildren(QTextEdit)
        desc_edits = [te for te in text_edits if "sum" in te.toPlainText().lower()]
        assert len(desc_edits) >= 1

    def test_description_is_readonly(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        text_edits = panel.findChildren(QTextEdit)
        desc_edits = [te for te in text_edits if "sum" in te.toPlainText().lower()]
        assert desc_edits[0].isReadOnly()


class TestSampleIO:
    """AC: Shows sample input/output in monospace font with clear labels."""

    def test_sample_input_shown(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        text_edits = panel.findChildren(QTextEdit)
        input_edits = [te for te in text_edits if "5 3" in te.toPlainText()]
        assert len(input_edits) >= 1

    def test_sample_output_shown(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        text_edits = panel.findChildren(QTextEdit)
        output_edits = [te for te in text_edits if "8" in te.toPlainText()]
        assert len(output_edits) >= 1

    def test_sample_io_labels_present(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        labels = panel.findChildren(QLabel)
        label_texts = " ".join(lb.text() for lb in labels).lower()
        assert "input" in label_texts
        assert "output" in label_texts


class TestSetExerciseMethod:
    """AC: set_exercise(exercise: Exercise) method updates all content."""

    def test_set_exercise_updates_title(self, qtbot, tmp_path):
        panel = ProblemPanel()
        qtbot.addWidget(panel)
        ex = _make_exercise(tmp_path)
        panel.set_exercise(ex)
        labels = panel.findChildren(QLabel)
        assert any("Sum Two Numbers" in lb.text() for lb in labels)
