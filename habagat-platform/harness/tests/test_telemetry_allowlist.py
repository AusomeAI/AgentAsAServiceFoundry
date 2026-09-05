"""Proves Doc 53 §6.3's mandatory contract test: construct an event with
every allowed field populated AND a disallowed field injected; assert the
disallowed field is absent from the output. This is the concrete
implementation of Doc 59 ADR-15's isolation-boundary claim, made testable."""
from harness.telemetry_emitter import (
    ALLOWED_BILLING_FIELDS,
    ALLOWED_RUN_TELEMETRY_FIELDS,
    emit_billing_event,
    emit_run_completed,
)


def test_run_completed_drops_disallowed_field():
    event = {
        "event_type": "run.completed",
        "event_id": "evt-1",
        "occurred_at": "2026-03-11T14:22:03Z",
        "tenant_id": "contoso-prod",
        "run_id": "run-1",
        "instance_id": "inst-1",
        "blueprint_id": "invoice-ap",
        "blueprint_version": "4.2.0",
        "outcome": "committed",
        "autonomy_level_used": "L2",
        "cost_usd": 0.2333,
        "duration_ms": 4210,
        "step_count": 6,
        "escalation_reason": None,
        # THE DISALLOWED FIELDS — the whole point of this test:
        "document_content": "Invoice INV-4471, supplier Acme Corp, address 123 Main St...",
        "prompt_text": "the full system prompt used for this run",
        "tool_call_arguments": {"po_ref": "PO-44120", "customer_email": "priya@contoso.com"},
    }
    result = emit_run_completed(event)

    assert "document_content" not in result
    assert "prompt_text" not in result
    assert "tool_call_arguments" not in result
    assert set(result.keys()) <= ALLOWED_RUN_TELEMETRY_FIELDS
    # And every ALLOWED field that was present is preserved:
    assert result["run_id"] == "run-1"
    assert result["cost_usd"] == 0.2333


def test_billing_event_drops_disallowed_field():
    event = {
        "event_type": "agent_run.billable",
        "event_id": "evt-2",
        "occurred_at": "2026-03-11T14:22:03Z",
        "tenant_id": "contoso-prod",
        "run_id": "run-1",
        "agent_id": "invoice-ap",
        "blueprint_version": "4.2.0",
        "outcome": "committed",
        "cost_usd": 0.2333,
        "invoice_number": "INV-4471",  # DISALLOWED — customer content
    }
    result = emit_billing_event(event)
    assert "invoice_number" not in result
    assert set(result.keys()) <= ALLOWED_BILLING_FIELDS


def test_no_customer_content_field_pattern_ever_in_allowlist():
    """A structural sanity check on the allowlist itself: none of its field
    names suggest free-text customer content (Doc 52 §4's schema-level
    exclusion, restated as a lint on the allowlist definition)."""
    suspicious_substrings = ["content", "text", "document", "prompt", "argument", "email", "name", "address"]
    for field_name in ALLOWED_RUN_TELEMETRY_FIELDS | ALLOWED_BILLING_FIELDS:
        for s in suspicious_substrings:
            assert s not in field_name.lower(), f"Allowlist field '{field_name}' looks like it could carry content"
