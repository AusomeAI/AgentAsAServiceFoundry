"""The Telemetry Emitter — implements the control-plane allowlist as CODE.

Traces to: Doc 53 §6 (the allowlist contract, copied here near-verbatim
since it is normative), Doc 59 ADR-15 (enforcement lives at the SOURCE,
inside the tenant, before anything crosses the network boundary).
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("habagat.telemetry")

# Doc 53 §6.1 — the ONLY place new fields may be added to what crosses the
# isolation boundary. A field not listed here is dropped, not forwarded.
ALLOWED_RUN_TELEMETRY_FIELDS = frozenset(
    {
        "event_type", "event_id", "occurred_at", "tenant_id", "run_id",
        "instance_id", "blueprint_id", "blueprint_version", "outcome",
        "autonomy_level_used", "cost_usd", "duration_ms", "step_count",
        "escalation_reason",
    }
)

ALLOWED_DRIFT_TELEMETRY_FIELDS = frozenset(
    {"event_type", "event_id", "occurred_at", "tenant_id", "drift_type", "resource_type", "config_hash", "expected_hash"}
)

ALLOWED_BILLING_FIELDS = frozenset(
    {"event_type", "event_id", "occurred_at", "tenant_id", "run_id", "agent_id", "blueprint_version", "outcome", "cost_usd"}
)


def enforce_allowlist(event: dict[str, Any], allowlist: frozenset[str]) -> dict[str, Any]:
    """The single function every outbound control-plane event passes
    through, applied INSIDE the tenant before the event ever reaches the
    network boundary (Doc 59 ADR-15) — never on the receiving end."""
    disallowed = set(event.keys()) - allowlist
    if disallowed:
        logger.warning("telemetry field dropped (never forwarded)", extra={"fields": sorted(disallowed)})
    return {k: v for k, v in event.items() if k in allowlist}


def emit_run_completed(event: dict[str, Any]) -> dict[str, Any]:
    return enforce_allowlist(event, ALLOWED_RUN_TELEMETRY_FIELDS)


def emit_drift_signal(event: dict[str, Any]) -> dict[str, Any]:
    return enforce_allowlist(event, ALLOWED_DRIFT_TELEMETRY_FIELDS)


def emit_billing_event(event: dict[str, Any]) -> dict[str, Any]:
    return enforce_allowlist(event, ALLOWED_BILLING_FIELDS)
