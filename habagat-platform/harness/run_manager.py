"""The Run Manager — the single writer of Run state.

Traces to: Doc 54 §2 (the full spec), Doc 51 §2.2 (why the Run Manager is
the only component permitted to advance run state — the justification for
the harness being one deployable), Doc 52 §1.2 (the Run lifecycle state
machine, reproduced here as executable transition rules).

Every other harness subsystem (Policy Engine, Tool Gateway, Memory Manager,
Verifier, Escalation Manager, Telemetry Emitter, Saga Coordinator) is
CONSULTED by the Run Manager and returns a result to it — none of them
advance Run.status directly. This module is that single writer.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Callable

from harness.domain import (
    Budget,
    Escalation,
    EscalationReason,
    Run,
    RunStatus,
    Step,
    ToolCall,
    ToolCallStatus,
    Verification,
    VerificationDecision,
)


class IllegalTransitionError(Exception):
    """Raised when code attempts a Run status transition not present in the
    state machine (Doc 52 §1.2's diagram). This is a defect, always — the
    state machine is meant to make illegal transitions structurally
    impossible, and this exception is the enforcement of that intent in a
    plain-dataclass implementation (a full type-state machine is a
    reasonable future refinement — see BUILD_LOG.md)."""


# Doc 52 §1.2's diagram, as an explicit adjacency set. Any transition not
# listed here is illegal and raises IllegalTransitionError.
LEGAL_TRANSITIONS: dict[RunStatus, set[RunStatus]] = {
    RunStatus.RECEIVED: {RunStatus.RUNNING, RunStatus.DUPLICATE},
    RunStatus.RUNNING: {
        RunStatus.CHECKPOINTED,
        RunStatus.AWAITING_TOOL,
        RunStatus.VERIFYING,
        RunStatus.COMPENSATING,
        RunStatus.FAILED,
        RunStatus.CANCELLED,
    },
    RunStatus.CHECKPOINTED: {RunStatus.RUNNING},
    RunStatus.AWAITING_TOOL: {RunStatus.RUNNING},  # after policy check + execution, folds back to RUNNING/CHECKPOINTED
    RunStatus.VERIFYING: {RunStatus.COMMITTED, RunStatus.ESCALATED},
    RunStatus.ESCALATED: {RunStatus.COMMITTED, RunStatus.FAILED},
    RunStatus.COMPENSATING: {RunStatus.FAILED, RunStatus.COMPENSATION_FAILED},
    RunStatus.CANCELLED: {RunStatus.COMPENSATING},  # if prior R2 writes exist
    RunStatus.COMMITTED: set(),   # terminal
    RunStatus.FAILED: set(),      # terminal
    RunStatus.COMPENSATION_FAILED: set(),  # terminal — resolved out-of-band by a human (Doc 54 §3.4)
    RunStatus.DUPLICATE: set(),   # terminal — return existing run_id, no new run created
}


class BudgetExceededError(Exception):
    """Raised by BudgetGuard.check_before_step() — the Run Manager MUST
    catch this and transition to FAILED with reason 'budget_exceeded',
    never silently continue (Doc 54 §2.3)."""


class RunStore:
    """In-memory reference implementation of Doc 52 §3.1's Cosmos DB
    `runs` container access pattern (point-read/write by run_id, optimistic
    concurrency via a version counter standing in for Cosmos's `_etag`).
    A production implementation swaps this for an actual Cosmos client
    behind the same interface — see BUILD_LOG.md for why this boundary is
    drawn here."""

    def __init__(self) -> None:
        self._runs: dict[str, Run] = {}
        self._versions: dict[str, int] = {}
        self._idempotency_index: dict[str, str] = {}  # idempotency_key -> run_id

    def get_by_idempotency_key(self, key: str) -> Run | None:
        run_id = self._idempotency_index.get(key)
        return self._runs.get(run_id) if run_id else None

    def create(self, run: Run) -> None:
        self._runs[run.run_id] = run
        self._versions[run.run_id] = 0
        key = run.trigger.get("idempotency_key")
        if key:
            self._idempotency_index[key] = run.run_id

    def get(self, run_id: str) -> Run | None:
        return self._runs.get(run_id)

    def save(self, run: Run, expected_version: int) -> int:
        """Optimistic concurrency check (Doc 54 §2.3: 'a replica that loses
        a write race backs off and does not retry the same step'). Raises
        if the version has moved since the caller last read it."""
        current = self._versions.get(run.run_id, 0)
        if current != expected_version:
            raise RuntimeError(
                f"Optimistic concurrency conflict on run {run.run_id}: "
                f"expected version {expected_version}, found {current}. "
                f"Treated as a P2 defect per Doc 54 §2.3 — retry against the fresh document."
            )
        self._versions[run.run_id] = current + 1
        self._runs[run.run_id] = run
        return self._versions[run.run_id]


class BudgetGuard:
    @staticmethod
    def check_before_step(run: Run) -> None:
        """Doc 54 §2.1: checked BEFORE every step executes, not after."""
        if not run.budget.within_budget():
            raise BudgetExceededError(
                f"Run {run.run_id} exhausted its budget "
                f"(steps: {run.budget.spent_steps}/{run.budget.max_steps}, "
                f"cost: ${run.budget.spent_cost_usd:.4f}/${run.budget.max_cost_usd:.4f})"
            )


@dataclass
class RunManager:
    store: RunStore

    def transition(self, run: Run, new_status: RunStatus, expected_version: int) -> int:
        legal = LEGAL_TRANSITIONS.get(run.status, set())
        if new_status not in legal:
            raise IllegalTransitionError(
                f"Illegal transition {run.status.value} -> {new_status.value} for run {run.run_id} "
                f"(Doc 52 §1.2 state machine)."
            )
        run.status = new_status
        return self.store.save(run, expected_version)

    def ingest_trigger(self, instance_id: str, tenant_id: str, trigger: dict[str, Any], budget: Budget) -> Run:
        """Doc 53 §2.1's trigger-ingestion endpoint, at the domain layer.
        Doc 52 §1.2: 'A trigger carries an idempotency key. Replays return
        the original result rather than re-executing.'"""
        key = trigger.get("idempotency_key")
        if key:
            existing = self.store.get_by_idempotency_key(key)
            if existing is not None:
                return existing  # caller inspects .status == DUPLICATE semantics via identity, not a new object

        run = Run(instance_id=instance_id, tenant_id=tenant_id, trigger=trigger, budget=budget, status=RunStatus.RECEIVED)
        self.store.create(run)
        self.transition(run, RunStatus.RUNNING, expected_version=0)
        return run

    def begin_step(self, run: Run) -> Step:
        """Doc 54 §2.1 StepExecutor: check budget BEFORE the step, then
        create it. Raises BudgetExceededError if exhausted — caller must
        catch and fail the run cleanly (Doc 54 §2.3)."""
        BudgetGuard.check_before_step(run)
        step = Step(step_number=len(run.steps))
        run.steps.append(step)
        return step

    def record_tool_call(self, run: Run, step: Step, tool_call: ToolCall) -> None:
        step.tool_calls.append(tool_call)
        if tool_call.status == ToolCallStatus.EXECUTED:
            run.budget.spent_steps += 1

    def checkpoint(self, run: Run, expected_version: int) -> int:
        """Doc 54 §2.1: 'state is persisted after every step, not only at
        natural boundaries.'"""
        return self.store.save(run, expected_version)

    def apply_verification(self, run: Run, verification: Verification, expected_version: int) -> int:
        run.verification = verification
        target = RunStatus.COMMITTED if verification.decision == VerificationDecision.COMMIT else RunStatus.ESCALATED
        # VERIFYING is a transient logical state; we fold the transition
        # RUNNING -> VERIFYING -> {COMMITTED, ESCALATED} into one call here
        # for callers that call apply_verification directly after proposing
        # an outcome, matching Doc 52 §1.2's diagram where VERIFYING has no
        # externally-observable dwell time of its own.
        if run.status == RunStatus.RUNNING:
            self.transition(run, RunStatus.VERIFYING, expected_version)
            expected_version += 1
        return self.transition(run, target, expected_version)

    def fail_run(self, run: Run, expected_version: int, reason: str) -> int:
        run.proposed_outcome = run.proposed_outcome or {}
        run.proposed_outcome["_failure_reason"] = reason
        return self.transition(run, RunStatus.FAILED, expected_version)

    def resume_or_create_escalation(self, run: Run, reason: EscalationReason, evidence: dict[str, Any]) -> Escalation:
        """Called after apply_verification() moves a run to ESCALATED —
        constructs the Escalation record the Escalation Manager (Doc 54 §8)
        then enqueues. Kept here, not in escalation_manager.py, because it
        reads Run-internal state (verification notes, tool call history)
        that only the Run Manager should reach into directly."""
        return Escalation(run_id=run.run_id, reason=reason, evidence=evidence)
