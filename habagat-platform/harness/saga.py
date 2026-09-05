"""The Saga / Compensation Engine.

Traces to: Doc 54 §3 (the full design, including §3.4's "when a compensating
action itself fails" — the case this assignment explicitly requires be
handled completely, not left implicit), Doc 30 §5.1, Doc 31 §2.3.

Owned by the Run Manager (harness/run_manager.py calls unwind(), never the
reverse) per Doc 54 §1's "every arrow points out from the Run Manager" rule.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Protocol

from harness.domain import RiskClass, Run, ToolCall, ToolCallStatus


class UnwindOutcome(str, Enum):
    FULL = "full"                          # every R2 write successfully compensated
    PARTIAL = "partial"                    # unwinding stopped after a compensation failure
    NOTHING_TO_COMPENSATE = "nothing_to_compensate"


@dataclass
class CompensationAttempt:
    tool_call: ToolCall
    compensating_tool_id: str
    succeeded: bool
    error: str | None = None


@dataclass
class UnwindResult:
    outcome: UnwindOutcome
    attempts: list[CompensationAttempt] = field(default_factory=list)

    def first_failure(self) -> CompensationAttempt | None:
        for a in self.attempts:
            if not a.succeeded:
                return a
        return None

    def uncompensated_writes(self, all_r2_writes_newest_first: list[ToolCall]) -> list[ToolCall]:
        """Writes never even attempted because unwinding stopped early
        (Doc 54 §3.4 rule 1: 'stop unwinding further, immediately')."""
        attempted_ids = {a.tool_call.tool_call_id for a in self.attempts}
        return [tc for tc in all_r2_writes_newest_first if tc.tool_call_id not in attempted_ids]


class CompensatingActionExecutor(Protocol):
    def __call__(self, compensating_tool_id: str, original_tool_call: ToolCall) -> tuple[bool, str | None]:
        """Executes the compensating action via the Tool Gateway, using the
        idempotency key f(run_id, step, 'compensate') per Doc 54 §3.1.
        Returns (succeeded, error_message)."""
        ...


def unwind(run: Run, executor: CompensatingActionExecutor) -> UnwindResult:
    """Doc 54 §3.1: unwind every completed R2 write, in STRICT REVERSE ORDER
    of execution. Doc 54 §3.2 explains why reverse order specifically —
    a later action may depend on an earlier one's post-state, so undoing
    must be layered like a stack, not applied in arbitrary or forward order.

    Doc 54 §3.4 — the failure case:
      1. Stop unwinding further, immediately, on the FIRST compensation
         failure. Do not attempt earlier writes' compensations while a
         later one is in an unknown state.
      2. The caller (run_manager.py) is responsible for setting
         Run.status = COMPENSATION_FAILED, not this function — this
         function reports the fact; state transition ownership stays with
         the single writer (Doc 54 §2.1).
      3-6. Escalation, idempotent retry, and eval-case generation are all
         caller responsibilities (harness/escalation_manager.py,
         eval/) — kept out of this module so `unwind()` remains a pure,
         easily-testable function with no side effects beyond calling the
         injected `executor`.
    """
    r2_writes_execution_order = run.executed_r2_writes()
    if not r2_writes_execution_order:
        return UnwindResult(outcome=UnwindOutcome.NOTHING_TO_COMPENSATE)

    reverse_order = list(reversed(r2_writes_execution_order))
    attempts: list[CompensationAttempt] = []

    for tool_call in reverse_order:
        comp_id = tool_call.compensating_action_id
        if comp_id is None:
            # Should be unreachable — the compiler refuses to build a
            # blueprint with an R2 tool lacking a compensator (Doc 59
            # ADR-14). Treated as a hard failure here rather than skipped,
            # because skipping would silently leave a write uncompensated.
            attempts.append(
                CompensationAttempt(
                    tool_call=tool_call,
                    compensating_tool_id="<missing>",
                    succeeded=False,
                    error="No compensating_action_id recorded on this ToolCall — "
                    "this should be impossible for a compiled bundle (Doc 59 ADR-14). "
                    "Treating as a compensation failure.",
                )
            )
            return UnwindResult(outcome=UnwindOutcome.PARTIAL, attempts=attempts)

        succeeded, error = executor(comp_id, tool_call)
        attempts.append(
            CompensationAttempt(tool_call=tool_call, compensating_tool_id=comp_id, succeeded=succeeded, error=error)
        )

        if succeeded:
            tool_call.status = ToolCallStatus.COMPENSATED
        else:
            tool_call.status = ToolCallStatus.COMPENSATION_FAILED
            # Doc 54 §3.4 rule 1 — stop immediately, do not touch earlier writes.
            return UnwindResult(outcome=UnwindOutcome.PARTIAL, attempts=attempts)

    return UnwindResult(outcome=UnwindOutcome.FULL, attempts=attempts)


def retry_failed_compensation(
    failed_attempt: CompensationAttempt, executor: CompensatingActionExecutor
) -> CompensationAttempt:
    """Doc 54 §3.4 rule 6: 'the SagaCoordinator retries the failed
    compensating action once, automatically, after a human-triggered
    "retry compensation" action... safe because the compensating action
    itself must be idempotent.' This function does NOT resume the rest of
    the unwind automatically — per rule 1, a human must confirm the
    underlying issue is resolved before ANY further unwinding proceeds;
    resuming the remaining stack is a separate, explicit call to unwind()
    with the run's updated state."""
    succeeded, error = executor(failed_attempt.compensating_tool_id, failed_attempt.tool_call)
    if succeeded:
        failed_attempt.tool_call.status = ToolCallStatus.COMPENSATED
    return CompensationAttempt(
        tool_call=failed_attempt.tool_call,
        compensating_tool_id=failed_attempt.compensating_tool_id,
        succeeded=succeeded,
        error=error,
    )
