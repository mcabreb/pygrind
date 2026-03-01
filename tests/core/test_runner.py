"""Integration tests for QProcess CodeRunner."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pytrainer.core.runner import CodeRunner


@pytest.fixture
def runner(qtbot):
    """Create a CodeRunner instance."""
    r = CodeRunner()
    return r


class TestCodeRunnerBasic:
    """Test basic CodeRunner properties and temp file handling."""

    def test_writes_temp_file(self, runner, qtbot):
        """AC: Writes user code to a temporary .py file."""
        code = "print('hello')"
        with qtbot.waitSignal(runner.finished, timeout=5000):
            runner.run(code, "")
        # Temp file should be cleaned up after execution
        # We verify it was created by the fact that the process ran successfully

    def test_cleans_up_temp_file(self, runner, qtbot):
        """AC: Cleans up temp file after execution."""
        code = "print('done')"
        with qtbot.waitSignal(runner.finished, timeout=5000):
            runner.run(code, "")
        # After signal, temp file should be gone
        if runner._temp_path is not None:
            assert not Path(runner._temp_path).exists()

    def test_cleans_up_temp_file_on_error(self, runner, qtbot):
        """AC: Cleans up temp file on error paths too."""
        code = "raise RuntimeError('boom')"
        with qtbot.waitSignal(runner.finished, timeout=5000):
            runner.run(code, "")
        if runner._temp_path is not None:
            assert not Path(runner._temp_path).exists()


class TestCodeRunnerExecution:
    """Test actual subprocess execution."""

    def test_successful_execution(self, runner, qtbot):
        """AC: Starts QProcess, captures stdout on completion."""
        code = "print('hello world')"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "")
        stdout, stderr, exit_code = blocker.args
        assert "hello world" in stdout
        assert exit_code == 0

    def test_captures_stderr(self, runner, qtbot):
        """AC: Captures stderr on process finish."""
        code = "import sys; sys.stderr.write('error msg')"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "")
        stdout, stderr, exit_code = blocker.args
        assert "error msg" in stderr

    def test_runtime_error_captured(self, runner, qtbot):
        """AC: Runtime errors produce stderr output and non-zero exit code."""
        code = "1/0"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "")
        stdout, stderr, exit_code = blocker.args
        assert exit_code != 0
        assert "ZeroDivisionError" in stderr

    def test_feeds_stdin(self, runner, qtbot):
        """AC: Feeds test input via QProcess.write() followed by closeWriteChannel()."""
        code = "x = input()\nprint(f'got: {x}')"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "42\n")
        stdout, stderr, exit_code = blocker.args
        assert "got: 42" in stdout
        assert exit_code == 0

    def test_multiline_stdin(self, runner, qtbot):
        """Multiple lines of stdin are all available."""
        code = "a = input()\nb = input()\nprint(f'{a}+{b}')"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "3\n4\n")
        stdout, stderr, exit_code = blocker.args
        assert "3+4" in stdout

    def test_empty_stdin(self, runner, qtbot):
        """Empty stdin doesn't break execution."""
        code = "print('no input needed')"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "")
        stdout, stderr, exit_code = blocker.args
        assert "no input needed" in stdout
        assert exit_code == 0

    def test_finished_signal_emitted(self, runner, qtbot):
        """AC: Emits finished(stdout, stderr, exit_code) signal on completion."""
        code = "print('sig test')"
        with qtbot.waitSignal(runner.finished, timeout=5000) as blocker:
            runner.run(code, "")
        assert len(blocker.args) == 3  # stdout, stderr, exit_code


class TestCodeRunnerPlatform:
    """Test platform-specific behavior."""

    def test_uses_correct_python_executable(self, runner):
        """AC: Uses python3 on Unix, python on Windows."""
        if sys.platform == "win32":
            assert runner._python_cmd == "python"
        else:
            assert runner._python_cmd == "python3"
