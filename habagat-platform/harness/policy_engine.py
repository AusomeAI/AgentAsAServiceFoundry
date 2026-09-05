"""The Policy Engine — envelope computation.

Traces to: Doc 54 §4.1 (the exact algorithm, reproduced here literally,
INCLUDING THE ORDERING OF STEPS, per the task instruction "the ordering is
load-bearing, not incidental"), Doc 31 §2.2 (the envelope concept), Doc 34
§4.1 layer 1 ("the policy envelope is computed before untrusted content is
read").

The five properties Doc 31 §2.2 requires, restated as what this module must
never violate:
  1. Deny by default — allowed_tools is never wider than the ceiling.
  2. Tenant overrides intersect, never widen, the blueprint's own ceiling.
  3. The agent cannot modify its own envelope (enforced by NOT exposing any
     mutation method on PolicyEnvelope — see domain.py, a frozen-in-spirit
     dataclass with no setters used anywhere in this codebase).
  4. Every denial is logged (the caller — run_manager.py — is responsible
     for persisting ToolCall.status=denied; this module's job stops at
     producing the envelope a denial is checked against).
  5. Every failure mode fails CLOSED — narrower, never wider.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any, Protocol

from harness.domain import AUTONOMY_ORDER, Autonomy, PolicyEnvelope, RiskClass


class PolicyComputationError(Exception):
    """Raised when an input required for envelope computation is
    unreachable. Per Doc 54 §4.3: 'every failure in policy computation
    fails toward less permission, never more' — callers that catch this
    MUST treat it as 'deny everything', never as 'proceed with defaults'."""


@dataclass
class BlueprintCeiling:
    autonomy_max_permitted: Autonomy
    blast_radius: str
    tools: list[dict[str, Any]]  # each: {ref, risk, requiresHumanApproval, ...}
    retrieval_index_scope: list[str]
    value_limits: dict[str, float]


@dataclass
class TenantConfig:
    """Doc 54 §4.2's worked example inputs."""

    policy_overrides_tool_allowlist: list[str] | None  # None = no override, inherit ceiling
    value_limits_override: dict[str, float]  # tenant MAY be tighter, never looser
    operating_hours: tuple[int, int] | None  # (start_hour, end_hour), local time — None = no restriction


@dataclass
class CallerIdentity:
    identity_id: str
    entra_group_scope: list[str]  # the index/record scope this caller may see


@dataclass
class IncidentState:
    fleet_freeze_active: bool = False
    tenant_kill_switch_active: bool = False

    def snapshot(self) -> dict[str, bool]:
        return {"fleet_freeze_active": self.fleet_freeze_active, "tenant_kill_switch_active": self.tenant_kill_switch_active}


class Clock(Protocol):
    def now(self) -> float: ...
    def current_hour(self) -> int: ...


class SystemClock:
    def now(self) -> float:
        return time.time()

    def current_hour(self) -> int:
        return time.localtime().tm_hour


def _within_operating_window(clock: Clock, operating_hours: tuple[int, int] | None) -> bool:
    if operating_hours is None:
        return True
    start, end = operating_hours
    return start <= clock.current_hour() < end


def _min_elementwise(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    """Doc 54 §4.1 step 3: 'value_limits = min_elementwise(blueprint default,
    tenant override if present)'. A key present in only one dict passes
    through unchanged — the intersection is over shared keys' VALUES, not
    over the key set."""
    result = dict(a)
    for key, val in b.items():
        result[key] = min(result.get(key, val), val)
    return result


def _hash_inputs(*parts: Any) -> str:
    blob = json.dumps(parts, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def compute_envelope(
    ceiling: BlueprintCeiling,
    tenant_config: TenantConfig,
    caller: CallerIdentity | None,
    budget_spent_steps: int,
    budget_max_steps: int,
    budget_spent_cost_usd: float,
    budget_max_cost_usd: float,
    incident_state: IncidentState | None,
    instance_current_autonomy: Autonomy,
    clock: Clock | None = None,
) -> PolicyEnvelope:
    """Doc 54 §4.1's algorithm, step-for-step. Do not reorder these steps —
    each one narrows what the previous step produced, and the FINAL step
    (incident/kill-switch check) is deliberately last and unconditional so
    it can never be defeated by an earlier step's logic.

    FAIL-CLOSED CONTRACT (Doc 54 §4.3): if `caller` is None, or
    `tenant_config` cannot be resolved by the calling code, this function
    raises PolicyComputationError rather than returning a permissive
    envelope. The caller (run_manager.py) MUST treat that exception as "deny
    the run entirely" — there is no silent fallback path here or anywhere
    else in this module.
    """
    clock = clock or SystemClock()

    # Step 1 — start from the blueprint's own ceiling. Nothing computed
    # later in this function may ever WIDEN beyond what the blueprint permits.
    ceiling_autonomy = ceiling.autonomy_max_permitted
    ceiling_tools = ceiling.tools
    ceiling_data_scope = ceiling.retrieval_index_scope

    # Step 2 — apply the AgentInstance's current autonomy (may be lower than
    # the ceiling, e.g. mid-ramp per CTO Doc 03 §3.5 "autonomy ramp").
    effective_autonomy = min(
        ceiling_autonomy, instance_current_autonomy, key=lambda a: AUTONOMY_ORDER.index(a)
    )

    # Step 3 — apply tenant policy overrides. INTERSECTION ONLY.
    if tenant_config.policy_overrides_tool_allowlist is not None:
        allowed_refs = {t["ref"] for t in ceiling_tools} & set(tenant_config.policy_overrides_tool_allowlist)
        allowed_tools = [t for t in ceiling_tools if t["ref"] in allowed_refs]
    else:
        allowed_tools = list(ceiling_tools)

    value_limits = _min_elementwise(ceiling.value_limits, tenant_config.value_limits_override)

    # Step 4 — apply caller entitlements. FAIL CLOSED if caller is missing
    # (Doc 54 §4.3: "no envelope is computed without a resolvable caller
    # identity, because Step 4's data-scope trimming has nothing to trim
    # against").
    if caller is None:
        raise PolicyComputationError(
            "Cannot compute a policy envelope without a resolvable caller identity "
            "(Doc 54 §4.3 fail-closed rule). Deny the run."
        )
    data_scope = [s for s in ceiling_data_scope if s in caller.entra_group_scope]

    # Step 5 — time-of-day / operating-window policy. R2/R3 tools are
    # stripped ENTIRELY outside the operating window; R0/R1 remain.
    if not _within_operating_window(clock, tenant_config.operating_hours):
        allowed_tools = [t for t in allowed_tools if t.get("risk") in (RiskClass.R0.value, RiskClass.R1.value)]

    # Step 6 — budget remaining.
    max_cost_remaining = max(0.0, budget_max_cost_usd - budget_spent_cost_usd)
    max_steps_remaining = max(0, budget_max_steps - budget_spent_steps)

    # Step 7 — the global kill switch / incident state OVERRIDES EVERYTHING
    # above. Checked LAST, unconditionally. FAIL CLOSED if incident_state is
    # unreachable — treated as though an incident IS active (Doc 54 §4.3:
    # "if we cannot confirm it is NOT an incident, we behave as though it is").
    if incident_state is None:
        incident_state = IncidentState(fleet_freeze_active=True, tenant_kill_switch_active=False)

    if incident_state.fleet_freeze_active or incident_state.tenant_kill_switch_active:
        allowed_tools = []
        write_permitted = False
    else:
        write_permitted = any(t.get("risk") in (RiskClass.R2.value, RiskClass.R3.value) for t in allowed_tools)

    # Step 8 — assemble and hash for audit.
    envelope = PolicyEnvelope(
        allowed_tools=allowed_tools,
        data_scope=data_scope,
        value_limits=value_limits,
        write_permitted=write_permitted,
        human_approval_required_for=[t["ref"] for t in allowed_tools if t.get("requiresHumanApproval")],
        max_cost_usd=max_cost_remaining,
        max_steps=max_steps_remaining,
        computed_at=clock.now(),
        inputs_hash=_hash_inputs(
            [t["ref"] for t in ceiling_tools],
            tenant_config.value_limits_override,
            caller.identity_id,
            budget_spent_steps,
            budget_spent_cost_usd,
            incident_state.snapshot(),
        ),
    )
    return envelope


def check_tool_allowed(envelope: PolicyEnvelope, tool_ref: str) -> tuple[bool, str | None]:
    """Doc 54 §5.2's Tool Gateway call sequence: 'check(tool_id, risk_class,
    envelope)'. Deny-by-default — a tool not in allowed_tools cannot be
    called regardless of what the model produces (Doc 31 §2.2 property 1)."""
    # `write_permitted` is a summary flag for convenience/telemetry only —
    # the AUTHORITATIVE check is membership in allowed_tools, below. A tool
    # already excluded by an earlier narrowing step (Steps 3/5/7) is simply
    # absent from allowed_tools by the time this function runs.
    for t in envelope.allowed_tools:
        if t["ref"] == tool_ref:
            return True, None
    return False, f"Tool '{tool_ref}' is not in the computed policy envelope (denied)."
