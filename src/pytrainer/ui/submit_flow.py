"""Submit flow controller — wires Run/Submit actions to pipeline and session."""

import logging

from PyQt6.QtCore import QObject, pyqtSignal

from pytrainer.core.pipeline import ExecutionPipeline, PipelineResult
from pytrainer.core.session_mgr import SessionManager
from pytrainer.ui.competition import CompetitionWindow

log = logging.getLogger(__name__)


class SubmitFlowController(QObject):
    """Orchestrates Run and Submit actions between UI and pipeline."""

    problem_solved = pyqtSignal(int)  # emitted with the solved problem index

    def __init__(
        self,
        session_mgr: SessionManager,
        window: CompetitionWindow,
        pipeline: ExecutionPipeline,
        timer_controller: QObject | None = None,
        score_frozen_check: "callable | None" = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._session_mgr = session_mgr
        self._window = window
        self._pipeline = pipeline
        self._timer_controller = timer_controller
        self._score_frozen_check = score_frozen_check or (lambda: False)
        self._run_mode: bool = False

        # Wire button signals
        window.run_requested.connect(self.on_run)
        window.submit_requested.connect(self.on_submit)
        pipeline.execution_complete.connect(self._on_execution_complete)

    def on_run(self) -> None:
        """Execute code against first test case only (quick test)."""
        self._run_mode = True
        self._start_execution()

    def on_submit(self) -> None:
        """Execute code against all test cases (official attempt)."""
        self._run_mode = False
        self._start_execution()

    def _start_execution(self) -> None:
        """Common execution start: disable buttons, pause timer, invoke pipeline."""
        self._window.run_button.setEnabled(False)
        self._window.submit_button.setEnabled(False)

        if self._timer_controller is not None:
            self._timer_controller.pause()

        code = self._window.editor.text()
        ps = self._session_mgr.current_problem

        self._pipeline.execute(
            code=code,
            exercise=ps.exercise,
            attempts=ps.attempts,
            time_spent=ps.time_spent,
        )

    def _on_execution_complete(self, result: PipelineResult) -> None:
        """Handle pipeline completion — update UI and session state."""
        # Re-enable buttons
        self._window.run_button.setEnabled(True)
        self._window.submit_button.setEnabled(True)

        # Resume timer
        if self._timer_controller is not None:
            self._timer_controller.resume()

        # Safety violation — show immediately
        if result.blocked:
            self._window.output_panel.show_safety_violation(result.violations)
            return

        # Show test results in output panel
        output_results = []
        for tr in result.test_results:
            output_results.append(
                {
                    "test_num": tr.index + 1,
                    "status": "pass" if tr.passed else "fail",
                    "expected": "",
                    "actual": tr.details if not tr.passed else "",
                }
            )
        if output_results:
            self._window.output_panel.show_results(output_results)

        # Only update session state on Submit (not Run)
        if not self._run_mode:
            idx = self._session_mgr.current_problem_index
            if self._score_frozen_check():
                # Overtime: still show pass/fail feedback but don't update score
                self._session_mgr.record_attempt(
                    idx, passed=result.all_passed, score=0
                )
            else:
                self._session_mgr.record_attempt(
                    idx,
                    passed=result.all_passed,
                    score=result.score,
                )
            if result.all_passed:
                self.problem_solved.emit(idx)
