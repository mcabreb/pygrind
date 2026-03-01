"""Tests for E4-S07: Timer Widget."""

from PyQt6.QtWidgets import QLabel

from pytrainer.ui.timer_widget import TimerWidget


class TestTimeFormat:
    """AC: Displays time in HH:MM:SS format with large, bold font (20pt+)."""

    def test_format_full_time(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(10800)  # 3 hours
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "03:00:00" in lb.text()]
        assert len(time_labels) >= 1

    def test_format_minutes_seconds(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(754)  # 12:34
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "00:12:34" in lb.text()]
        assert len(time_labels) >= 1

    def test_format_zero(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(0)
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "00:00:00" in lb.text()]
        assert len(time_labels) >= 1

    def test_font_is_large(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(3600)
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "01:00:00" in lb.text()]
        assert time_labels[0].font().pointSize() >= 20

    def test_font_is_bold(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(3600)
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "01:00:00" in lb.text()]
        assert time_labels[0].font().bold()


class TestDefaultColor:
    """AC: Default color: standard text color."""

    def test_default_color_above_1800(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(3600)  # 1 hour — above 30min
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "01:00:00" in lb.text()]
        # No orange or red styling
        style = time_labels[0].styleSheet()
        assert "#FF9800" not in style
        assert "#f44336" not in style


class TestWarningColor:
    """AC: At 30 minutes remaining (1800s): text turns yellow/orange."""

    def test_warning_at_1800(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(1800)
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "00:30:00" in lb.text()]
        style = time_labels[0].styleSheet()
        assert "#FF9800" in style or "orange" in style.lower() or "yellow" in style.lower()

    def test_warning_at_900(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(900)  # 15 min — still in warning range
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "00:15:00" in lb.text()]
        style = time_labels[0].styleSheet()
        assert "#FF9800" in style or "orange" in style.lower()


class TestUrgentColor:
    """AC: At 5 minutes remaining (300s): text turns red and bold."""

    def test_urgent_at_300(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(300)
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "00:05:00" in lb.text()]
        style = time_labels[0].styleSheet()
        assert "#f44336" in style or "red" in style.lower()

    def test_urgent_at_60(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(60)
        labels = widget.findChildren(QLabel)
        time_labels = [lb for lb in labels if "00:01:00" in lb.text()]
        style = time_labels[0].styleSheet()
        assert "#f44336" in style or "red" in style.lower()


class TestPauseIndicator:
    """AC: When paused: shows pause icon or 'PAUSED' indicator."""

    def test_paused_shows_indicator(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.set_paused(True)
        labels = widget.findChildren(QLabel)
        texts = " ".join(lb.text() for lb in labels)
        assert "PAUSED" in texts or "⏸" in texts

    def test_unpaused_hides_indicator(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.set_paused(True)
        widget.set_paused(False)
        labels = widget.findChildren(QLabel)
        visible_texts = " ".join(lb.text() for lb in labels if lb.isVisible())
        assert "PAUSED" not in visible_texts


class TestUpdateTimeMethod:
    """AC: update_time(remaining_secs: int) method refreshes the display."""

    def test_update_changes_display(self, qtbot):
        widget = TimerWidget()
        qtbot.addWidget(widget)
        widget.update_time(7200)
        labels = widget.findChildren(QLabel)
        assert any("02:00:00" in lb.text() for lb in labels)

        widget.update_time(3661)
        labels = widget.findChildren(QLabel)
        assert any("01:01:01" in lb.text() for lb in labels)
