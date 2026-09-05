"""ERP connector — the service-principal, promoted-container reference
(Doc 57 §2.2). Implements the exact tool set the invoice-ap blueprint
declares: lookup_po, three_way_match, post_invoice, reverse_invoice_posting,
release_payment.
"""
from __future__ import annotations

from typing import Any, Callable

from tools.contract import ConnectorError, ToolDeclaration

DECLARATIONS = [
    ToolDeclaration(
        tool_id="erp.lookup_po",
        version="2.1.0",
        risk_class="R0",
        description="Retrieves a purchase order and goods-receipt history.",
        input_schema={"type": "object", "additionalProperties": False, "required": ["po_reference"], "properties": {"po_reference": {"type": "string"}}},
        output_schema={"type": "object"},
        auth_mode="service_principal",
    ),
    ToolDeclaration(
        tool_id="erp.three_way_match",
        version="2.1.0",
        risk_class="R0",
        description="Compares invoice, PO and goods receipt within tolerance.",
        input_schema={"type": "object", "additionalProperties": False, "required": ["invoice", "po_reference"], "properties": {"invoice": {"type": "object"}, "po_reference": {"type": "string"}}},
        output_schema={"type": "object"},
        auth_mode="service_principal",
    ),
    ToolDeclaration(
        tool_id="erp.post_invoice",
        version="2.1.0",
        risk_class="R2",
        description="Posts a validated invoice as approved-for-payment. Does NOT release payment.",
        input_schema={"type": "object", "additionalProperties": False, "required": ["vendor_id", "invoice_number", "po_reference", "line_items", "gl_account", "cost_centre"],
                      "properties": {"vendor_id": {"type": "string"}, "invoice_number": {"type": "string"}, "po_reference": {"type": "string"},
                                     "line_items": {"type": "array"}, "gl_account": {"type": "string"}, "cost_centre": {"type": "string"}}},
        output_schema={"type": "object"},
        auth_mode="service_principal",
        compensating_action="erp.reverse_invoice_posting",
    ),
    ToolDeclaration(
        tool_id="erp.reverse_invoice_posting",
        version="2.1.0",
        risk_class="R2",
        description="Reverses a posting made by erp.post_invoice. Idempotent.",
        input_schema={"type": "object", "additionalProperties": False, "required": ["erp_document_id", "reason"], "properties": {"erp_document_id": {"type": "string"}, "reason": {"type": "string"}}},
        output_schema={"type": "object"},
        auth_mode="service_principal",
        compensating_action=None,
    ),
    ToolDeclaration(
        tool_id="erp.release_payment",
        version="2.1.0",
        risk_class="R3",
        description="Releases payment. IRREVERSIBLE. Always requires human approval.",
        input_schema={"type": "object", "additionalProperties": False, "required": ["erp_document_id"], "properties": {"erp_document_id": {"type": "string"}}},
        output_schema={"type": "object"},
        auth_mode="service_principal",
        requires_human_approval=True,
    ),
]

TOLERANCE_PCT = 0.02  # Doc 36's inv-edge-0447 example: 2% unit-price variance tolerance


class ErpConnector:
    """Reference execution adapter. `erp_client` is injected — see Doc 57
    §6.1: connectors are tested against sandbox/mock accounts, never live
    production ERP systems."""

    def __init__(self, erp_client: Any) -> None:
        self._client = erp_client
        self._reversed_documents: set[str] = set()  # tracks idempotent reversal state

    def lookup_po(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            return self._client.get_purchase_order(arguments["po_reference"])
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"erp.lookup_po failed: {e}") from e

    def three_way_match(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Orchestrates several reads plus a comparison in the connector's
        own code (Doc 57 §2.2's note) — R0 because it only reads and
        computes, never writes."""
        po = self.lookup_po(tool_id, {"po_reference": arguments["po_reference"]})
        invoice = arguments["invoice"]

        # Doc 36 §1.1's inv-edge-0447 case matches invoiced quantity against
        # the PO's ORDERED quantity, not the (possibly partial) received
        # quantity: PO-44120 was ordered 1000, only 600 received, and an
        # invoice for 600 is still flagged as a quantity mismatch — the
        # three-way match's job is to catch "vendor invoiced for less than
        # the PO commits to" as much as "more than was received", so it is
        # deliberately stricter than a received-quantity-only check.
        qty_match = invoice.get("quantity") == po.get("qty")
        price_variance = abs(invoice.get("unit_price", 0) - po.get("unit_price", 0)) / max(po.get("unit_price", 1), 0.01)
        price_within_tolerance = price_variance <= TOLERANCE_PCT

        return {
            "passed": qty_match and price_within_tolerance,
            "quantity_match": qty_match,
            "quantity_ordered": po.get("qty"),
            "quantity_received": po.get("received"),
            "quantity_invoiced": invoice.get("quantity"),
            "price_variance_pct": round(price_variance * 100, 2),
            "price_within_tolerance": price_within_tolerance,
        }

    def post_invoice(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            return self._client.post_invoice(arguments)
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"erp.post_invoice failed: {e}") from e

    def reverse_invoice_posting(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Idempotent per Doc 53 §3.2: reversing an already-reversed
        document is a no-op returning the original reversal record."""
        doc_id = arguments["erp_document_id"]
        if doc_id in self._reversed_documents:
            return {"reversal_document_id": f"REV-{doc_id}", "already_reversed": True}
        try:
            result = self._client.reverse_posting(doc_id, arguments["reason"])
            self._reversed_documents.add(doc_id)
            return result
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"erp.reverse_invoice_posting failed: {e}") from e

    def release_payment(self, tool_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
        # Reachable ONLY after human approval — enforced by the Policy
        # Engine's envelope (harness/policy_engine.py) and the compiler
        # (Doc 59 ADR-14), never by this connector itself. This function
        # trusts that it is only ever called within that already-approved
        # context, which is precisely why R3 approval enforcement lives
        # upstream, not here.
        try:
            return self._client.release_payment(arguments["erp_document_id"])
        except Exception as e:  # noqa: BLE001
            raise ConnectorError(f"erp.release_payment failed: {e}") from e

    def executors(self) -> dict[str, Callable[[str, dict], dict]]:
        return {
            "erp.lookup_po": self.lookup_po,
            "erp.three_way_match": self.three_way_match,
            "erp.post_invoice": self.post_invoice,
            "erp.reverse_invoice_posting": self.reverse_invoice_posting,
            "erp.release_payment": self.release_payment,
        }
