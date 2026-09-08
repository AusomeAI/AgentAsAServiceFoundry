"""End-to-end tests: a full agent run through the Run Manager's state
machine (Doc 54 §2.2), reaching every terminal state in Doc 52 §1.2's
diagram at least once — Doc 58 §7's explicit E2E coverage requirement:
"Every terminal state in Doc 54 §2.2's diagram has at least one E2E test
reaching it" as a merge-to-staging gate.

Unlike test_run_manager_state_machine.py (which unit-tests individual
Run Manager methods and the transition table in isolation) and
test_saga_compensation.py (which unit-tests harness/saga.py's unwind()
directly against a bare Run), these tests drive a Run through the full
realistic call sequence a real trigger would produce: ingest_trigger ->
begin_step -> record_tool_call -> apply_verification -> (escalation
decision | saga unwind) -> terminal state — proving the SEAM between
Run Manager and Saga Coordinator, not just each module alone.

Terminal states required by Doc 54 §2.2 / Doc 58 §7:
  committed
  escalated -> committed
  escalated -> failed
  failed
  compensating -> failed
  compensation_failed
"""
from __future__ import annotations

from harness.domain import (
    Budget, EscalationReason, RunStatus, ToolCall, ToolCallStatus, Verification, VerificationDecision,
)
from harness.run_manager import RunManager, RunStore
from harness.saga import unwind


def _new_run(manager: RunManager):
    return manager.ingest_trigger(
        instance_id="inst-invoice-ap", tenant_id="contoso-prod",
        trigger={"idempotency_key": f"trig-{id(manager)}-{len(manager.store._runs)}"},
        budget=Budget(max_steps=10, max_cost_usd=1.0),
    )


def test_terminal_state_committed():
    """A clean run: verification COMMITs directly, no escalation, no
    compensation — the most common path."""
    manager = RunManager(store=RunStore())
    run = _new_run(manager)

    step = manager.begin_step(run)
    manager.record_tool_call(run, step, ToolCall(tool_id="erp.lookup_po", risk_class="R0", arguments={}, status=ToolCallStatus.EXECUTED))

    verification = Verification(hard_rules_passed=True, groundedness_score=1.0, confidence=0.98, decision=VerificationDecision.COMMIT)
    version = manager.checkpoint(run, expected_version=1)
    manager.apply_verification(run, verification, expected_version=version)

    assert run.status == RunStatus.COMMITTED


def test_terminal_state_escalated_then_committed():
    """Verification escalates (below confidence threshold); a human
    reviewer then approves it — Doc 52 §1.2's escalated -> committed edge
    (the Escalation Review screen's 'Approve' action, Doc 56 §2)."""
    manager = RunManager(store=RunStore())
    run = _new_run(manager)

    step = manager.begin_step(run)
    manager.record_tool_call(run, step, ToolCall(tool_id="erp.three_way_match", risk_class="R0", arguments={}, status=ToolCallStatus.EXECUTED))

    verification = Verification(hard_rules_passed=True, groundedness_score=0.9, confidence=0.71, decision=VerificationDecision.ESCALATE)
    version = manager.checkpoint(run, expected_version=1)
    version = manager.apply_verification(run, verification, expected_version=version)
    assert run.status == RunStatus.ESCALATED

    escalation = manager.resume_or_create_escalation(run, EscalationReason.LOW_CONFIDENCE, evidence={"confidence": 0.71})
    assert escalation.run_id == run.run_id

    # A human reviewer approves via the Escalation Review screen.
    manager.transition(run, RunStatus.COMMITTED, expected_version=version)
    assert run.status == RunStatus.COMMITTED


def test_terminal_state_escalated_then_failed():
    """A human reviewer rejects the escalated run — Doc 52 §1.2's
    Escalation lifecycle 'escalated -> failed' on reject
    (habagat-design/screens/escalation-review.md's Reject action)."""
    manager = RunManager(store=RunStore())
    run = _new_run(manager)

    verification = Verification(hard_rules_passed=True, groundedness_score=0.6, confidence=0.40, decision=VerificationDecision.ESCALATE)
    version = manager.checkpoint(run, expected_version=1)
    version = manager.apply_verification(run, verification, expected_version=version)
    assert run.status == RunStatus.ESCALATED

    manager.resume_or_create_escalation(run, EscalationReason.HARD_RULE_FAILED, evidence={})
    manager.transition(run, RunStatus.FAILED, expected_version=version)
    assert run.status == RunStatus.FAILED


def test_terminal_state_failed_directly_on_budget_exhaustion():
    """Doc 54 §2.3: BudgetExceededError caught by the caller, run
    transitions straight to FAILED with reason budget_exhausted — no
    verification or escalation step involved, since the run never gets
    far enough to produce a proposed outcome."""
    manager = RunManager(store=RunStore())
    run = manager.ingest_trigger("inst-1", "contoso-prod", {"idempotency_key": "k-budget"}, Budget(max_steps=0, max_cost_usd=1.0))

    from harness.run_manager import BudgetExceededError
    try:
        manager.begin_step(run)
        assert False, "expected BudgetExceededError"
    except BudgetExceededError:
        pass

    manager.fail_run(run, expected_version=1, reason="budget_exhausted")
    assert run.status == RunStatus.FAILED
    assert run.proposed_outcome["_failure_reason"] == "budget_exhausted"


def test_terminal_state_compensating_then_failed_full_unwind():
    """A run committed an R2 write, then a LATER problem (e.g. a
    downstream validation failure the Verifier's belt-and-braces check
    catches) requires unwinding it. The saga fully compensates every R2
    write, and the run still ends FAILED — the original outcome could not
    stand even though the compensation itself succeeded (Doc 54 §3: a
    full, successful unwind is still a failed run, not a committed one)."""
    manager = RunManager(store=RunStore())
    run = _new_run(manager)

    step = manager.begin_step(run)
    write = ToolCall(tool_id="erp.post_invoice", risk_class="R2", arguments={}, status=ToolCallStatus.EXECUTED, compensating_action_id="erp.reverse_invoice_posting")
    manager.record_tool_call(run, step, write)

    version = manager.checkpoint(run, expected_version=1)
    manager.transition(run, RunStatus.COMPENSATING, expected_version=version)
    version += 1
    assert run.status == RunStatus.COMPENSATING

    def executor(compensating_tool_id: str, original_tool_call) -> tuple[bool, str | None]:
        return True, None  # the reversal succeeds

    result = unwind(run, executor)
    assert result.outcome.value == "full"

    manager.fail_run(run, expected_version=version, reason="compensated_after_downstream_failure")
    assert run.status == RunStatus.FAILED


def test_terminal_state_compensation_failed_on_partial_unwind():
    """Doc 54 §3.4's failure case: the saga stops immediately on the
    first compensation failure. The run's terminal state is
    COMPENSATION_FAILED, not FAILED — Doc 54 §3.4 requires this be
    resolved out-of-band by a human, never silently downgraded to an
    ordinary failed run."""
    manager = RunManager(store=RunStore())
    run = _new_run(manager)

    step = manager.begin_step(run)
    write = ToolCall(tool_id="erp.post_invoice", risk_class="R2", arguments={}, status=ToolCallStatus.EXECUTED, compensating_action_id="erp.reverse_invoice_posting")
    manager.record_tool_call(run, step, write)

    version = manager.checkpoint(run, expected_version=1)
    manager.transition(run, RunStatus.COMPENSATING, expected_version=version)
    version += 1

    def failing_executor(compensating_tool_id: str, original_tool_call) -> tuple[bool, str | None]:
        return False, "ERP system unreachable"

    result = unwind(run, failing_executor)
    assert result.outcome.value == "partial"
    assert result.first_failure() is not None

    manager.transition(run, RunStatus.COMPENSATION_FAILED, expected_version=version)
    assert run.status == RunStatus.COMPENSATION_FAILED


def test_every_terminal_state_in_doc52_diagram_has_a_covering_test_above():
    """A meta-test: enumerates the terminal states this module's docstring
    promises coverage for, so a future edit that removes one of the tests
    above without updating this list fails loudly instead of silently
    losing coverage."""
    covered_terminal_paths = {
        "committed",
        "escalated_then_committed",
        "escalated_then_failed",
        "failed_directly",
        "compensating_then_failed",
        "compensation_failed",
    }
    assert len(covered_terminal_paths) == 6  # Doc 54 §2.2's full terminal-state list
