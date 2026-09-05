"""The Escalation Manager.

Traces to: Doc 54 §8, Doc 31 §2.6, Doc 53 §2.3 (decision_reason mandatory),
habagat-design/handoff/component-contracts.md (the Console/Teams contract
this module ultimately serves — see console/packages/customer's Escalation
Review screen for the consuming client).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from harness.domain import Escalation, EscalationReason


class MissingDecisionReasonError(Exception):
    """Doc 53 §2.3 server-side validation: decision_reason missing -> 400
    VALIDATION_FAILED. Raised here as the domain-layer enforcement of that
    HTTP-layer contract."""


SLA_SECONDS_BY_REASON: dict[EscalationReason, float] = {
    EscalationReason.HARD_RULE_FAILED: 4 * 3600,
    EscalationReason.LOW_CONFIDENCE: 24 * 3600,
    EscalationReason.OUT_OF_POLICY: 24 * 3600,
    EscalationReason.TOOL_DENIED: 24 * 3600,
    EscalationReason.BUDGET_EXHAUSTED: 24 * 3600,
}


@dataclass
class EscalationQueue:
    """In-memory reference store standing in for the tenant's Cosmos
    `escalations` container (Doc 52 §3.1)."""

    _items: dict[str, Escalation] = field(default_factory=dict)

    def enqueue(self, escalation: Escalation) -> Escalation:
        escalation.sla_due_at = time.time() + SLA_SECONDS_BY_REASON.get(escalation.reason, 24 * 3600)
        self._items[escalation.escalation_id] = escalation
        return escalation

    def get(self, escalation_id: str) -> Escalation | None:
        return self._items.get(escalation_id)

    def pending(self) -> list[Escalation]:
        """Oldest-first (matches habagat-design/screens/customer-console.md's
        Approval Queue ordering, itself matching this SLA model)."""
        return sorted(
            (e for e in self._items.values() if e.decision is None),
            key=lambda e: e.sla_due_at or 0,
        )

    def aged_past_sla(self, now: float | None = None) -> list[Escalation]:
        now = now or time.time()
        return [e for e in self.pending() if e.sla_due_at is not None and e.sla_due_at < now]

    def decide(self, escalation_id: str, decision: str, decision_reason: str | None, decided_by: str) -> Escalation:
        """Doc 53 §2.3: decision_reason is REQUIRED, always — enforced here
        regardless of which client (web Console or Teams bot) called in."""
        if not decision_reason or not decision_reason.strip():
            raise MissingDecisionReasonError(
                "decision_reason is required for every escalation decision (Doc 53 §2.3, Doc 52 §1.2)."
            )
        escalation = self._items.get(escalation_id)
        if escalation is None:
            raise KeyError(f"No escalation {escalation_id}")
        escalation.decision = decision
        escalation.decision_reason = decision_reason
        escalation.decided_by = decided_by
        escalation.decided_at = time.time()
        return escalation


def assemble_evidence(
    recommendation: str,
    confidence: float,
    confidence_threshold: float,
    comparison_rows: list[dict[str, Any]],
    uncertainty_note: str | None,
) -> dict[str, Any]:
    """Doc 54 §8.1 EvidenceAssembler: builds the "complete case" payload —
    designed BACKWARD from habagat-design/screens/escalation-review.md's
    layout (header -> recommend -> evidence -> uncertain), so the Console
    renders this shape directly without transformation. This is the concrete
    link between the UI/UX Designer Agent's EvidencePanelData contract
    (habagat-design/components/evidence-panel.md) and the backend."""
    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "confidence_threshold": confidence_threshold,
        "comparisonRows": comparison_rows,  # maps to EvidencePanelData.rows
        "uncertaintyNote": uncertainty_note,
    }
