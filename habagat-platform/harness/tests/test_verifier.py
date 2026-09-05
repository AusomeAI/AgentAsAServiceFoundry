"""Proves Doc 54 §7.3's required tests: hard-rule-always-escalates,
claim-stripping, and a basic calibration sanity check."""
from harness.domain import PolicyEnvelope, VerificationDecision
from harness.verifier import VerifierConfig, verify
from policy.hard_rules import HardRule

ENVELOPE = PolicyEnvelope(
    allowed_tools=[{"ref": "erp.post_invoice", "risk": "R2"}],
    data_scope=["acme-vendor-terms:emea"],
    value_limits={"max_invoice_amount": 25000},
    write_permitted=True,
    human_approval_required_for=[],
    max_cost_usd=0.5,
    max_steps=10,
    computed_at=0.0,
    inputs_hash="abc",
)

ALWAYS_TRUE = HardRule("always_true", "trivially passes", lambda ctx, out: True)
ALWAYS_FALSE = HardRule("always_false", "trivially fails", lambda ctx, out: False)


def high_confidence_self_check(run_context, proposed_outcome):
    return (0.98, "high confidence, no reasoning gaps")


def low_confidence_self_check(run_context, proposed_outcome):
    return (0.40, "significant ambiguity in the source documents")


def test_failed_hard_rule_always_escalates_regardless_of_confidence_and_groundedness():
    """The core test Doc 54 §7.3 names by name: 'construct a case where it
    fails and assert decision == escalate regardless of how high the
    confidence and groundedness scores are set in the same fixture.'"""
    config = VerifierConfig(hard_rules=[ALWAYS_FALSE], groundedness_min=0.0, confidence_threshold=0.0)
    result = verify(
        run_context={},
        proposed_outcome={"claims": []},  # no claims -> groundedness trivially 1.0
        config=config,
        envelope=ENVELOPE,
        self_check_fn=high_confidence_self_check,  # confidence 0.98 — should NOT matter
        retrieved_evidence=[],
        tool_results=[],
    )
    assert result.decision == VerificationDecision.ESCALATE
    assert result.hard_rules_passed is False


def test_passing_hard_rules_with_high_confidence_and_groundedness_commits():
    config = VerifierConfig(hard_rules=[ALWAYS_TRUE], groundedness_min=0.5, confidence_threshold=0.9)
    result = verify(
        run_context={},
        proposed_outcome={"claims": [{"text": "amount matches PO", "source_ref": "doc-1"}]},
        config=config,
        envelope=ENVELOPE,
        self_check_fn=high_confidence_self_check,
        retrieved_evidence=[{"id": "doc-1"}],
        tool_results=[],
    )
    assert result.decision == VerificationDecision.COMMIT
    assert result.hard_rules_passed is True


def test_claim_stripping_removes_unattributable_claims_and_records_the_gap():
    """Doc 54 §7.3: 'a proposed outcome with one attributable and one
    unattributable claim; assert the unattributable claim is removed and
    the gap is recorded, not silently dropped.'"""
    config = VerifierConfig(hard_rules=[ALWAYS_TRUE], groundedness_min=0.0, confidence_threshold=0.9)
    proposed = {
        "claims": [
            {"text": "invoice total is $4,350", "source_ref": "doc-1"},       # attributable
            {"text": "supplier pre-agreed the price change", "source_ref": None},  # NOT attributable
        ]
    }
    result = verify(
        run_context={},
        proposed_outcome=proposed,
        config=config,
        envelope=ENVELOPE,
        self_check_fn=high_confidence_self_check,
        retrieved_evidence=[{"id": "doc-1"}],
        tool_results=[],
    )
    # groundedness = 1 of 2 claims attributable = 0.5, which clears the 0.0 gate here
    assert result.groundedness_score == 0.5
    assert "supplier pre-agreed the price change" in result.unattributable_claims


def test_groundedness_below_threshold_escalates_even_with_high_confidence():
    config = VerifierConfig(hard_rules=[ALWAYS_TRUE], groundedness_min=0.9, confidence_threshold=0.0)
    proposed = {"claims": [{"text": "unsupported claim", "source_ref": None}]}
    result = verify(
        run_context={},
        proposed_outcome=proposed,
        config=config,
        envelope=ENVELOPE,
        self_check_fn=high_confidence_self_check,
        retrieved_evidence=[],
        tool_results=[],
    )
    assert result.decision == VerificationDecision.ESCALATE


def test_low_confidence_escalates_even_with_perfect_groundedness_and_hard_rules():
    config = VerifierConfig(hard_rules=[ALWAYS_TRUE], groundedness_min=0.0, confidence_threshold=0.90)
    result = verify(
        run_context={},
        proposed_outcome={"claims": []},
        config=config,
        envelope=ENVELOPE,
        self_check_fn=low_confidence_self_check,  # 0.40, below the 0.90 threshold
        retrieved_evidence=[],
        tool_results=[],
    )
    assert result.decision == VerificationDecision.ESCALATE
    assert result.confidence == 0.40


def test_write_required_but_envelope_forbids_it_escalates_as_backstop():
    """Doc 54 §7.2's belt-and-braces final check — a run that somehow
    reaches verification proposing a write despite a non-write-permitted
    envelope must still be caught here, independent of the Policy Engine."""
    no_write_envelope = PolicyEnvelope(
        allowed_tools=[],
        data_scope=[],
        value_limits={},
        write_permitted=False,
        human_approval_required_for=[],
        max_cost_usd=0.0,
        max_steps=0,
        computed_at=0.0,
        inputs_hash="x",
    )
    config = VerifierConfig(hard_rules=[ALWAYS_TRUE], groundedness_min=0.0, confidence_threshold=0.0)
    result = verify(
        run_context={},
        proposed_outcome={"claims": []},
        config=config,
        envelope=no_write_envelope,
        self_check_fn=high_confidence_self_check,
        retrieved_evidence=[],
        tool_results=[],
        outcome_requires_write=True,
    )
    assert result.decision == VerificationDecision.ESCALATE
