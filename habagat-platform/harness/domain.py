"""Domain entities for a single agent run, per Doc 52 §1.2.

This module is deliberately dependency-light (dataclasses + enums only) so
policy_engine.py, run_manager.py, verifier.py, and saga.py can all import it
without a circular dependency — it is the shared vocabulary Doc 51 §3's
"Run" bounded context speaks, translated to Python.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class Autonomy(str, Enum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"


AUTONOMY_ORDER = [Autonomy.L0, Autonomy.L1, Autonomy.L2, Autonomy.L3, Autonomy.L4]


class RiskClass(str, Enum):
    R0 = "R0"  # read-only
    R1 = "R1"  # write to Habagat-owned state only
    R2 = "R2"  # reversible write to a customer system — compensator required
    R3 = "R3"  # irreversible / external-facing / moves money — human approval mandatory below L4


class RunStatus(str, Enum):
    RECEIVED = "received"
    RUNNING = "running"
    CHECKPOINTED = "checkpointed"
    AWAITING_TOOL = "awaiting_tool"
    VERIFYING = "verifying"
    ESCALATED = "escalated"
    COMMITTED = "committed"
    COMPENSATING = "compensating"
    COMPENSATION_FAILED = "compensation_failed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DUPLICATE = "duplicate"


class ToolCallStatus(str, Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    DENIED = "denied"
    FAILED = "failed"
    COMPENSATED = "compensated"
    COMPENSATION_FAILED = "compensation_failed"


class EscalationReason(str, Enum):
    LOW_CONFIDENCE = "low_confidence"
    OUT_OF_POLICY = "out_of_policy"
    HARD_RULE_FAILED = "hard_rule_failed"
    TOOL_DENIED = "tool_denied"
    BUDGET_EXHAUSTED = "budget_exhausted"


class VerificationDecision(str, Enum):
    COMMIT = "commit"
    ESCALATE = "escalate"


@dataclass
class Budget:
    max_steps: int
    max_cost_usd: float
    spent_steps: int = 0
    spent_cost_usd: float = 0.0

    def within_budget(self) -> bool:
        return self.spent_steps < self.max_steps and self.spent_cost_usd < self.max_cost_usd

    def remaining_steps(self) -> int:
        return max(0, self.max_steps - self.spent_steps)

    def remaining_cost_usd(self) -> float:
        return max(0.0, self.max_cost_usd - self.spent_cost_usd)


@dataclass
class ToolCall:
    tool_id: str
    risk_class: RiskClass
    arguments: dict[str, Any]
    tool_call_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    result: dict[str, Any] | None = None
    status: ToolCallStatus = ToolCallStatus.PENDING
    denial_reason: str | None = None
    compensating_action_id: str | None = None
    idempotency_key: str = ""
    step_number: int = 0


@dataclass
class Step:
    step_number: int
    tool_calls: list[ToolCall] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)
    completed_at: float | None = None


@dataclass
class Verification:
    hard_rules_checked: list[dict[str, Any]] = field(default_factory=list)
    hard_rules_passed: bool = False
    groundedness_score: float = 0.0
    unattributable_claims: list[str] = field(default_factory=list)
    confidence: float = 0.0
    self_check_notes: str = ""
    decision: VerificationDecision = VerificationDecision.ESCALATE


@dataclass
class Escalation:
    run_id: str
    reason: EscalationReason
    evidence: dict[str, Any]
    escalation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sla_due_at: float | None = None
    assigned_to: str | None = None
    decision: str | None = None  # "approve" | "modify" | "reject"
    decision_reason: str | None = None
    decided_by: str | None = None
    decided_at: float | None = None


@dataclass
class PolicyEnvelope:
    """Doc 54 §4.1's output shape — immutable for the life of the run
    (Doc 52 §1.2). Constructed ONLY by policy_engine.compute_envelope()."""

    allowed_tools: list[dict[str, Any]]
    data_scope: list[str]
    value_limits: dict[str, Any]
    write_permitted: bool
    human_approval_required_for: list[str]
    max_cost_usd: float
    max_steps: int
    computed_at: float
    inputs_hash: str


@dataclass
class Run:
    instance_id: str
    tenant_id: str
    trigger: dict[str, Any]
    budget: Budget
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: RunStatus = RunStatus.RECEIVED
    steps: list[Step] = field(default_factory=list)
    proposed_outcome: dict[str, Any] | None = None
    verification: Verification | None = None
    envelope: PolicyEnvelope | None = None
    started_at: float = field(default_factory=time.time)
    completed_at: float | None = None
    cost_usd: float = 0.0
    retrieved_evidence: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)

    def all_tool_calls(self) -> list[ToolCall]:
        return [tc for step in self.steps for tc in step.tool_calls]

    def executed_r2_writes(self) -> list[ToolCall]:
        """Doc 54 §3.1: the saga's input — completed R2 ToolCalls, in the
        order they executed (callers reverse this for unwind order)."""
        return [
            tc
            for tc in self.all_tool_calls()
            if tc.risk_class == RiskClass.R2 and tc.status == ToolCallStatus.EXECUTED
        ]
