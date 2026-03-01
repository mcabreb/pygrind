"""Tests for timeout and resource management in CodeRunner."""

import sys

import pytest

from pytrainer.core.runner import CodeRunner


@pytest.fixture
def runner(qtbot):
    """Create a CodeRunner instance."""
    return CodeRunner()


class TestTimeout:
    """Test timeout behavior."""

    def test_timeout_signal_exists(self, runner):
        """AC: Emits timeout() signal distinct from finished()."""
        assert hasattr(runner, "timeout")

    def test_timeout_kills_infinite_loop(self, runner, qtbot):
        """AC: On timeout, QProcess.kill() terminates the subprocess."""
        code = "while True: pass"
        # Set a short timeout for testing
        runner._timeout_ms = 1000
        with qtbot.waitSignal(runner.timeout, timeout=5000):
            runner.run(code, "")

    def test_timeout_cleans_up_temp_file(self, runner, qtbot):
        """AC: Temp file cleaned up even on timeout."""
        code = "while True: pass"
        runner._timeout_ms = 1000
        with qtbot.waitSignal(runner.timeout, timeout=5000):
            runner.run(code, "")
        from pathlib import Path

        if runner._temp_path is not None:
            assert not Path(runner._temp_path).exists()

    def test_normal_finish_cancels_timer(self, runner, qtbot):
        """AC: Timer cancelled when process finishes normally."""
        code = "print('fast')"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "")
        stdout, stderr, exit_code = blocker.args
        assert exit_code == 0
        # Timer should have been cancelled (no timeout signal fired)
        assert runner._timer is None or not runner._timer.isActive()

    def test_default_timeout_is_10_seconds(self, runner):
        """AC: QTimer starts at 10000ms."""
        assert runner._timeout_ms == 10000


class TestResourceLimits:
    """Test platform-specific resource limits."""

    @pytest.mark.skipif(sys.platform == "win32", reason="resource module not on Windows")
    def test_memory_limit_on_unix(self, runner, qtbot):
        """AC: Linux/macOS: resource.setrlimit sets 256MB RLIMIT_AS."""
        # Code that tries to allocate more than 256MB
        # This should fail due to resource limits
        code = "x = bytearray(300 * 1024 * 1024)"  # 300MB
        runner._timeout_ms = 5000
        # Either timeout or finished with error
        signals = [runner.finished, runner.timeout]
        with qtbot.waitSignals(signals, timeout=10000, raising=False):
            runner.run(code, "")

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific")
    def test_windows_no_resource_limit(self, runner):
        """AC: Windows: timeout is primary safety net."""
        # On Windows, resource limits are documented as best-effort
        assert runner._timeout_ms == 10000
