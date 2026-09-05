"""Evaluation Service — corpus storage, grading orchestration, gate history.

Traces to: Doc 55 §4 (this whole service), Doc 36 (eval-as-a-gate),
Doc 59 ADR-19 (tenant-scoped eval compute placement — resolved here, see
below).

This module wraps eval/runner.py's evaluate_gate() (already built and
tested against the real invoice-ap corpus) with the two things that are
specifically this SERVICE's job, not the eval engine's: (a) treating a
gate result as an immutable, appended fact (Doc 55 §4.3), and (b) refusing
LLM-as-judge scores as gate-eligible without a calibration record meeting
the kappa >= 0.75 bar (Doc 55 §4.4, eval/graders.py's JudgeCalibration).

RESOLVED GAP (Doc 60 §7 item 2 / Doc 55 §6 open question 1 / Doc 59 ADR-19):
tenant-scoped evaluation compute placement was left open — "a temporary job
the control-plane Evaluation Service deploys into the tenant per run, or a
standing capability of the Harness itself." Doc 55 §6's own recommendation
(reuse the Harness's existing model/tool-calling infrastructure rather than
a second execution path) is adopted here: `TenantEvalInvoker` below is the
control-plane-side client for a Harness-internal endpoint
(`POST /internal/v1/evaluate`), which this build adds to
harness/run_manager.py's surface as `RunManager` does not yet expose it —
flagged in BUILD_LOG.md as a real endpoint addition, not merely a comment.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol

from eval.graders import JudgeCalibration
from eval.runner import GateDecision, SuiteResult, evaluate_gate


@dataclass(frozen=True)
class GateHistoryRecord:
    """Doc 55 §4.3: an EvalResult/gate decision is never updated after
    graded_at — a re-grade produces a NEW row referencing the same
    case_id/blueprint_version, never an edit."""

    blueprint_id: str
    version: str
    graded_at: str
    decision: GateDecision
    judge_version: str | None = None


class GateHistoryImmutabilityError(Exception):
    pass


class JudgeNotCalibratedError(Exception):
    """Doc 55 §4.4: refuses to accept LLM-as-judge scores as gate-eligible
    without a calibration record at kappa >= 0.75."""


class TenantEvalInvoker(Protocol):
    """The control-plane-side client for the Harness-internal endpoint
    this build adds per the resolved ADR-19 gap above. Injected so this
    service's orchestration logic is tested without a real Harness."""

    def invoke_tenant_eval(self, tenant_id: str, blueprint_id: str, version: str, suite: str) -> SuiteResult: ...


class EvaluationService:
    def __init__(self) -> None:
        self._gate_history: list[GateHistoryRecord] = []
        self._calibrations: dict[str, JudgeCalibration] = {}

    def record_judge_calibration(self, judge_version: str, calibration: JudgeCalibration) -> None:
        self._calibrations[judge_version] = calibration

    def _require_judge_calibrated_if_used(self, judge_version: str | None) -> None:
        if judge_version is None:
            return
        calibration = self._calibrations.get(judge_version)
        if calibration is None or not calibration.is_gate_eligible():
            raise JudgeNotCalibratedError(
                f"Judge '{judge_version}' has no calibration record with kappa >= 0.75 "
                f"— its scores are not gate-eligible (Doc 55 §4.4)."
            )

    def evaluate_and_record_gate(
        self,
        *,
        blueprint_id: str,
        version: str,
        current: SuiteResult,
        baseline: SuiteResult | None,
        declared_gates: dict[str, float],
        judge_version: str | None = None,
    ) -> GateHistoryRecord:
        """Runs the shared eval/runner.py gate logic, then appends an
        immutable GateHistoryRecord (Doc 55 §4.3) — never updates a prior
        record for this (blueprint_id, version)."""
        self._require_judge_calibrated_if_used(judge_version)
        decision = evaluate_gate(current, baseline, declared_gates)
        record = GateHistoryRecord(
            blueprint_id=blueprint_id,
            version=version,
            graded_at=datetime.now(timezone.utc).isoformat(),
            decision=decision,
            judge_version=judge_version,
        )
        self._gate_history.append(record)
        return record

    def gate_history_for(self, blueprint_id: str, version: str) -> list[GateHistoryRecord]:
        """Every re-grade is a NEW entry — this can legitimately return
        more than one record for the same (blueprint_id, version)."""
        return [r for r in self._gate_history if r.blueprint_id == blueprint_id and r.version == version]
