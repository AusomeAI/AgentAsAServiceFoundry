import pytest

from tools.contract import ConnectorError
from tools.erp.connector import ErpConnector
from tools.erp.tests.fixtures import FakeErpClient


@pytest.fixture()
def connector() -> ErpConnector:
    return ErpConnector(erp_client=FakeErpClient())


def test_lookup_po(connector):
    po = connector.lookup_po("erp.lookup_po", {"po_reference": "PO-90001"})
    assert po["qty"] == 500


def test_lookup_missing_po_raises_connector_error(connector):
    with pytest.raises(ConnectorError):
        connector.lookup_po("erp.lookup_po", {"po_reference": "MISSING-PO"})


def test_three_way_match_passes_on_clean_case(connector):
    """Doc 36's happy-path case: PO-90001, 500@$12, invoiced 500@$12."""
    result = connector.three_way_match(
        "erp.three_way_match",
        {"invoice": {"quantity": 500, "unit_price": 12.00}, "po_reference": "PO-90001"},
    )
    assert result["passed"] is True


def test_three_way_match_fails_on_doc36_edge_case_inv_0447():
    """Reproduces Doc 36 §1.1's exact worked example numbers: PO-44120
    ordered 1000 @ $4.20, received 600; invoiced 600 @ $4.35 — a 3.57%
    price variance, outside the 2% tolerance, AND a quantity mismatch
    against the ORDERED quantity."""
    connector = ErpConnector(erp_client=FakeErpClient())
    result = connector.three_way_match(
        "erp.three_way_match",
        {"invoice": {"quantity": 600, "unit_price": 4.35}, "po_reference": "PO-44120"},
    )
    assert result["passed"] is False
    assert result["quantity_match"] is False  # 600 invoiced vs 1000 ordered
    assert result["price_within_tolerance"] is False
    assert result["price_variance_pct"] > 2.0


def test_post_invoice_returns_document_id(connector):
    result = connector.post_invoice(
        "erp.post_invoice",
        {"vendor_id": "V-1001", "invoice_number": "INV-1", "po_reference": "PO-90001", "line_items": [], "gl_account": "6000", "cost_centre": "CC1"},
    )
    assert result["erp_document_id"] == "DOC-INV-1"


def test_reverse_invoice_posting_is_idempotent(connector):
    """Doc 53 §3.2: 'reversing an already-reversed document is a no-op
    that returns the original reversal record.'"""
    first = connector.reverse_invoice_posting("erp.reverse_invoice_posting", {"erp_document_id": "DOC-1", "reason": "test"})
    second = connector.reverse_invoice_posting("erp.reverse_invoice_posting", {"erp_document_id": "DOC-1", "reason": "test"})
    assert first["reversal_document_id"] == second["reversal_document_id"]
    assert second.get("already_reversed") is True
    assert first.get("already_reversed") is None  # first call was NOT a no-op


def test_release_payment(connector):
    result = connector.release_payment("erp.release_payment", {"erp_document_id": "DOC-1"})
    assert result["payment_id"] == "PAY-DOC-1"


def test_r3_declaration_without_human_approval_raises_at_declaration_time():
    """Doc 59 ADR-14 restated at the declaration layer (tools/contract.py)
    — constructing an R3 declaration without requires_human_approval raises
    at DECLARATION TIME. This has no exemption, unlike R2 (see below)."""
    from tools.contract import ToolDeclaration

    with pytest.raises(ValueError):
        ToolDeclaration(
            tool_id="bad.r3", version="1.0.0", risk_class="R3", description="x",
            input_schema={}, output_schema={}, auth_mode="service_principal",
        )


def test_r2_declaration_without_compensator_is_allowed_at_declaration_time():
    """Doc 59 ADR-14's 'R2 needs a compensator' rule is NOT enforced here.
    Doc 53 §3.2 documents an exemption: a tool that exists only to compensate
    another tool (e.g. erp.reverse_invoice_posting, constructed above with no
    compensating_action) needs no compensator of its own. A single
    ToolDeclaration can't tell, at construction time, whether it plays that
    role for some other declaration in the registry — so this constructor
    only checks the R3 rule, which has no such exemption. The full R2 check
    (real violation vs. documented exemption) is enforced with registry-wide
    visibility in compiler/enforcement.py — see
    compiler/tests/test_enforcement_module.py and
    compiler/tests/test_r2_r3_enforcement.py for that coverage."""
    from tools.contract import ToolDeclaration

    decl = ToolDeclaration(
        tool_id="bad.r2", version="1.0.0", risk_class="R2", description="x",
        input_schema={}, output_schema={}, auth_mode="service_principal",
    )
    assert decl.compensating_action is None
