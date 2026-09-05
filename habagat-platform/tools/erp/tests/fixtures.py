"""Recorded/synthetic ERP fixtures, matching Doc 36's own inv-edge-0447 and
inv-should-escalate-0001 cases so the connector's three_way_match logic is
tested against the SAME numbers the eval corpus uses (Doc 57 §6.2)."""


class FakeErpClient:
    _POS = {
        "PO-90001": {"qty": 500, "unit_price": 12.00, "received": 500},
        "PO-44120": {"qty": 1000, "unit_price": 4.20, "received": 600},  # Doc 36's edge case
        "MISSING-PO": None,
    }

    def get_purchase_order(self, po_reference: str) -> dict:
        po = self._POS.get(po_reference)
        if po is None:
            raise RuntimeError(f"PO {po_reference} not found")
        return po

    def post_invoice(self, arguments: dict) -> dict:
        return {"erp_document_id": f"DOC-{arguments['invoice_number']}", "posted_at": "2026-03-11T14:00:00Z", "status": "posted"}

    def reverse_posting(self, erp_document_id: str, reason: str) -> dict:
        return {"reversal_document_id": f"REV-{erp_document_id}", "reversed_at": "2026-03-11T15:00:00Z"}

    def release_payment(self, erp_document_id: str) -> dict:
        return {"payment_id": f"PAY-{erp_document_id}", "released_at": "2026-03-11T16:00:00Z"}
