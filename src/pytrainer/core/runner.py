"""QProcess-based code runner for executing user Python code in a subprocess."""

import contextlib
import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QObject, QProcess, pyqtSignal


class CodeRunner(QObject):
    """Runs user Python code in an isolated subprocess via QProcess."""

    finished = pyqtSignal(str, str, int)  # stdout, stderr, exit_code

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._process: QProcess | None = None
        self._temp_path: str | None = None
        self._python_cmd = "python" if sys.platform == "win32" else "python3"

    def run(self, code: str, stdin_text: str) -> None:
        """Execute code in a subprocess, feeding stdin_text as input."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(code)
            self._temp_path = tmp.name

        # Set up QProcess
        self._process = QProcess(self)
        self._process.finished.connect(self._on_finished)

        self._process.start(self._python_cmd, [self._temp_path])

        # Feed stdin
        if stdin_text:
            self._process.write(stdin_text.encode("utf-8"))
        self._process.closeWriteChannel()

    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        """Handle process completion: capture output, cleanup, emit signal."""
        stdout = ""
        stderr = ""
        if self._process is not None:
            stdout = bytes(self._process.readAllStandardOutput()).decode("utf-8", errors="replace")
            stderr = bytes(self._process.readAllStandardError()).decode("utf-8", errors="replace")

        self._cleanup_temp()
        self.finished.emit(stdout, stderr, exit_code)

    def _cleanup_temp(self) -> None:
        """Remove the temporary file if it exists."""
        if self._temp_path is not None:
            with contextlib.suppress(OSError):
                Path(self._temp_path).unlink(missing_ok=True)
