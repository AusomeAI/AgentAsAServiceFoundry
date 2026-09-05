import pytest

from controlplane.registry.service import (
    BlueprintRegistry, DuplicateDigestError, InvalidPromotionError,
    Requirements, UnsignedBundleError,
)


def _reqs(**overrides) -> Requirements:
    base = dict(
        model_tiers_used=["mid"], connector_types=["sap-erp"],
        requires_search_index=False, requires_document_intelligence=True,
        max_autonomy_permitted="L2", risk_class_ceiling="R2",
    )
    base.update(overrides)
    return Requirements(**base)


def test_propose_version_requires_gates_passed():
    registry = BlueprintRegistry()
    with pytest.raises(UnsignedBundleError):
        registry.propose_version(
            blueprint_id="invoice-ap", version="4.2.0", content_digest="sha256:abc",
            requirements=_reqs(), eval_results_summary={}, gates_passed=False,
        )


def test_propose_version_signs_and_registers_at_ring_r0():
    registry = BlueprintRegistry()
    bp_version = registry.propose_version(
        blueprint_id="invoice-ap", version="4.2.0", content_digest="sha256:abc",
        requirements=_reqs(), eval_results_summary={"pass_rate": 0.95}, gates_passed=True,
    )
    assert bp_version.signed is True
    assert bp_version.signature == "sig::sha256:abc"
    assert bp_version.ring == "R0"


def test_duplicate_digest_rejected():
    registry = BlueprintRegistry()
    registry.propose_version(
        blueprint_id="invoice-ap", version="4.2.0", content_digest="sha256:abc",
        requirements=_reqs(), eval_results_summary={}, gates_passed=True,
    )
    with pytest.raises(DuplicateDigestError):
        registry.propose_version(
            blueprint_id="invoice-ap", version="4.2.1", content_digest="sha256:abc",
            requirements=_reqs(), eval_results_summary={}, gates_passed=True,
        )


def test_get_requirements_returns_the_closed_vocabulary_shape():
    """Doc 60 §5.3.2: this is the exact object registry_lookup.tf's
    data "http" block decodes at plan time."""
    registry = BlueprintRegistry()
    registry.propose_version(
        blueprint_id="invoice-ap", version="4.2.0", content_digest="sha256:abc",
        requirements=_reqs(risk_class_ceiling="R3"), eval_results_summary={}, gates_passed=True,
    )
    reqs = registry.get_requirements("invoice-ap", "4.2.0")
    assert reqs.to_dict()["risk_class_ceiling"] == "R3"


def test_promotion_must_advance_one_ring_forward():
    registry = BlueprintRegistry()
    registry.propose_version(
        blueprint_id="invoice-ap", version="4.2.0", content_digest="sha256:abc",
        requirements=_reqs(), eval_results_summary={}, gates_passed=True,
    )
    registry.promote("invoice-ap", "4.2.0", "R1")  # R0 -> R1: fine

    with pytest.raises(InvalidPromotionError):
        registry.promote("invoice-ap", "4.2.0", "R3")  # R1 -> R3: skips R2


def test_promotion_never_regresses():
    registry = BlueprintRegistry()
    registry.propose_version(
        blueprint_id="invoice-ap", version="4.2.0", content_digest="sha256:abc",
        requirements=_reqs(), eval_results_summary={}, gates_passed=True,
    )
    registry.promote("invoice-ap", "4.2.0", "R1")
    with pytest.raises(InvalidPromotionError):
        registry.promote("invoice-ap", "4.2.0", "R0")
