"""QProcess-based code runner for executing user Python code in a subprocess."""

import contextlib
import sys
import tempfile
import textwrap
from pathlib import Path

from PyQt6.QtCore import QObject, QProcess, QTimer, pyqtSignal

_MEMORY_LIMIT_BYTES = 256 * 1024 * 1024  # 256 MB


class CodeRunner(QObject):
    """Runs user Python code in an isolated subprocess via QProcess."""

    finished = pyqtSignal(str, str, int)  # stdout, stderr, exit_code
    timeout = pyqtSignal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._process: QProcess | None = None
        self._temp_path: str | None = None
        self._timer: QTimer | None = None
        self._timed_out = False
        self._timeout_ms = 10000
        self._python_cmd = "python" if sys.platform == "win32" else "python3"

    def run(self, code: str, stdin_text: str) -> None:
        """Execute code in a subprocess, feeding stdin_text as input."""
        wrapped = self._wrap_with_limits(code)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(wrapped)
            self._temp_path = tmp.name

        self._timed_out = False

        # Set up QProcess
        self._process = QProcess(self)
        self._process.finished.connect(self._on_finished)

        self._process.start(self._python_cmd, [self._temp_path])

        # Feed stdin
        if stdin_text:
            self._process.write(stdin_text.encode("utf-8"))
        self._process.closeWriteChannel()

        # Start timeout timer
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_timeout)
        self._timer.start(self._timeout_ms)

    def _wrap_with_limits(self, code: str) -> str:
        """Wrap code with resource limits on Unix platforms."""
        if sys.platform == "win32":
            return code
        return (
            textwrap.dedent(f"""\
            import resource
            resource.setrlimit(resource.RLIMIT_AS, ({_MEMORY_LIMIT_BYTES}, {_MEMORY_LIMIT_BYTES}))
        """)
            + code
        )

    def _on_timeout(self) -> None:
        """Handle execution timeout: kill process and emit timeout signal."""
        self._timed_out = True
        if self._process is not None and self._process.state() != QProcess.ProcessState.NotRunning:
            self._process.kill()

    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        """Handle process completion: capture output, cleanup, emit signal."""
        # Cancel the timer
        if self._timer is not None:
            self._timer.stop()
            self._timer = None

        stdout = ""
        stderr = ""
        if self._process is not None:
            stdout = bytes(self._process.readAllStandardOutput()).decode("utf-8", errors="replace")
            stderr = bytes(self._process.readAllStandardError()).decode("utf-8", errors="replace")

        self._cleanup_temp()

        if self._timed_out:
            self.timeout.emit()
        else:
            self.finished.emit(stdout, stderr, exit_code)

    def _cleanup_temp(self) -> None:
        """Remove the temporary file if it exists."""
        if self._temp_path is not None:
            with contextlib.suppress(OSError):
                Path(self._temp_path).unlink(missing_ok=True)
