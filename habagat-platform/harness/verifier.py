"""The Verifier — three-layer check between a proposed outcome and any commit.

Traces to: Doc 54 §7.1 (the exact algorithm), Doc 31 §2.5 (hard rules,
grounding check, confidence/self-check), Doc 52 §1.2 Verification invariant
("if hard_rules_passed == false, decision MUST equal escalate").
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol

from harness.domain import PolicyEnvelope, Verification, VerificationDecision
from policy.hard_rules import HardRule


@dataclass
class VerifierConfig:
    hard_rules: list[HardRule]
    groundedness_min: float
    confidence_threshold: float


class SelfCheckFn(Protocol):
    def __call__(self, run_context: dict[str, Any], proposed_outcome: dict[str, Any]) -> tuple[float, str]:
        """Returns (confidence, notes)."""
        ...


def _extract_claims(proposed_outcome: dict[str, Any]) -> list[dict[str, Any]]:
    """Doc 54 §7.1: 'claims = extract_claims(proposed_outcome)'. A claim is
    any field the outcome asserts as fact — this reference implementation
    treats every leaf value in the outcome's `claims` list (a blueprint
    author populates this explicitly when drafting the outcome schema) as
    one claim; blueprints that don't populate `claims` are treated as having
    none, which trivially passes groundedness (nothing to attribute) but is
    flagged as a build-time lint concern for that blueprint, not a verifier
    defect (see BUILD_LOG.md)."""
    return proposed_outcome.get("claims", [])


def _has_source(claim: dict[str, Any], retrieved_evidence: list[dict], tool_results: list[dict]) -> bool:
    """Doc 30 Rule 2 ('citation or silence'): a claim is attributable if its
    `source_ref` matches an id present in either retrieved evidence or a
    tool result recorded in this run."""
    source_ref = claim.get("source_ref")
    if not source_ref:
        return False
    evidence_ids = {e.get("id") for e in retrieved_evidence}
    tool_result_ids = {t.get("id") for t in tool_results}
    return source_ref in evidence_ids or source_ref in tool_result_ids


def _strip_claims(proposed_outcome: dict[str, Any], unattributable: list[dict]) -> dict[str, Any]:
    """Doc 31 §2.5: unattributable claims are 'stripped and the gap is
    stated explicitly' — never silently dropped without a trace."""
    result = dict(proposed_outcome)
    remaining = [c for c in result.get("claims", []) if c not in unattributable]
    result["claims"] = remaining
    result["_stripped_claim_gaps"] = [c.get("text", "<unlabeled claim>") for c in unattributable]
    return result


def verify(
    run_context: dict[str, Any],
    proposed_outcome: dict[str, Any],
    config: VerifierConfig,
    envelope: PolicyEnvelope,
    self_check_fn: SelfCheckFn,
    retrieved_evidence: list[dict],
    tool_results: list[dict],
    outcome_requires_write: bool = False,
) -> Verification:
    """Doc 54 §7.1's algorithm, in the exact layer order specified.

    Layer 1 — hard rules (deterministic, model not consulted).
    Layer 2 — grounding check (claims must trace to evidence or tool results).
    Layer 3 — confidence and self-check.
    Final — belt-and-braces autonomy/write-permission re-check (Doc 54 §7.2's
    defense-in-depth: this duplicates a check the Policy Engine already made,
    deliberately, as a backstop against a bug elsewhere in the loop).
    """
    # Layer 1 — hard rules. NEVER "reasoned around" (Doc 31 §2.5).
    hard_rule_results = [
        {"rule_id": rule.rule_id, "passed": rule.evaluate(run_context, proposed_outcome)} for rule in config.hard_rules
    ]
    hard_rules_passed = all(r["passed"] for r in hard_rule_results)

    if not hard_rules_passed:
        # Doc 52 §1.2 invariant: hard_rules_passed=False -> decision MUST be
        # "escalate". This is not a suggestion — a failed hard rule is
        # NEVER committed, regardless of what layers 2/3 would otherwise say.
        return Verification(
            hard_rules_checked=hard_rule_results,
            hard_rules_passed=False,
            decision=VerificationDecision.ESCALATE,
            self_check_notes="Escalated: one or more hard rules failed (Doc 31 §2.5). Layers 2/3 not evaluated.",
        )

    # Layer 2 — grounding check.
    claims = _extract_claims(proposed_outcome)
    attributable = [c for c in claims if _has_source(c, retrieved_evidence, tool_results)]
    unattributable = [c for c in claims if not _has_source(c, retrieved_evidence, tool_results)]
    groundedness_score = len(attributable) / len(claims) if claims else 1.0
    cleaned_outcome = _strip_claims(proposed_outcome, unattributable)

    if groundedness_score < config.groundedness_min:
        return Verification(
            hard_rules_checked=hard_rule_results,
            hard_rules_passed=True,
            groundedness_score=groundedness_score,
            unattributable_claims=[c.get("text", "<unlabeled>") for c in unattributable],
            decision=VerificationDecision.ESCALATE,
            self_check_notes=f"Escalated: groundedness {groundedness_score:.2f} below "
            f"threshold {config.groundedness_min:.2f}.",
        )

    # Layer 3 — confidence and self-check.
    confidence, notes = self_check_fn(run_context, cleaned_outcome)

    if confidence < config.confidence_threshold:
        return Verification(
            hard_rules_checked=hard_rule_results,
            hard_rules_passed=True,
            groundedness_score=groundedness_score,
            unattributable_claims=[c.get("text", "<unlabeled>") for c in unattributable],
            confidence=confidence,
            self_check_notes=notes,
            decision=VerificationDecision.ESCALATE,
        )

    # Final belt-and-braces check (Doc 54 §7.2): re-verify write permission
    # even though the Policy Engine's envelope already gated every tool call
    # that got us here — this catches a bug ELSEWHERE in the loop, not a
    # bug in this function's own reasoning.
    unattributable_texts = [c.get("text", "<unlabeled>") for c in unattributable]

    if outcome_requires_write and not envelope.write_permitted:
        return Verification(
            hard_rules_checked=hard_rule_results,
            hard_rules_passed=True,
            groundedness_score=groundedness_score,
            unattributable_claims=unattributable_texts,
            confidence=confidence,
            self_check_notes="Escalated: proposed outcome requires a write, "
            "but the current envelope does not permit one (belt-and-braces check, Doc 54 §7.2).",
            decision=VerificationDecision.ESCALATE,
        )

    # COMMIT still carries forward any stripped-but-below-gate claims (Doc
    # 31 §2.5: the gap is recorded even when the run isn't escalated over it —
    # groundedness cleared the THRESHOLD, but individual unattributable
    # claims were still stripped and their absence should remain visible in
    # the audit trail, not disappear once the decision is "commit").
    return Verification(
        hard_rules_checked=hard_rule_results,
        hard_rules_passed=True,
        groundedness_score=groundedness_score,
        unattributable_claims=unattributable_texts,
        confidence=confidence,
        self_check_notes=notes,
        decision=VerificationDecision.COMMIT,
    )
