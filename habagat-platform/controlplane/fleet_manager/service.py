"""Fleet Manager — tenant inventory, ring advance orchestration, drift.

Traces to: Doc 55 §2 (this whole service), CTO Doc 03 §4.1/§4.2 (fleet
coordinate, automated halt criteria), Doc 33 §2.2/§2.3 (advance criteria,
drift), Doc 52 §1.2 (AgentInstance).

GAP RECORDED (Doc 60 §7 item 1 / §5.3.4 table row 3): Doc 55 §2.4's drift
table does not name "AgentInstance vs. tenant config (.habagat-lock)
divergence" as an explicit drift class — it only names Terraform-state
drift and isolation-canary drift. Doc 60 §5.3.4 explicitly instructs the
Software Engineer Agent to add this class and flag the addition rather
than silently extending Doc 55. Done here: `DriftStatus.AGENT_INSTANCE_DRIFT`
and `check_agent_instance_drift()` below. See BUILD_LOG.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

Ring = Literal["R0", "R1", "R2", "R3"]
_RING_ORDER = ["R0", "R1", "R2", "R3"]


class DriftStatus(str, Enum):
    CLEAN = "clean"
    DRIFTING = "drifting"                    # Terraform-state drift, Doc 55 §2.4
    REMEDIATING = "remediating"
    # Added per Doc 60 §7 item 1 — see module docstring.
    AGENT_INSTANCE_DRIFT = "agent_instance_drift"


@dataclass
class FleetCoordinate:
    """Doc 55 §2.1's exact fields, restated as a dataclass."""

    tenant_id: str
    platform_version: str
    blueprint_versions: list[dict] = field(default_factory=list)  # [{blueprint_id, version, ring, autonomy_current}]
    model_versions: list[dict] = field(default_factory=list)
    module_version: str = ""
    ring: Ring = "R0"
    last_reconciled_at: str | None = None
    drift_status: DriftStatus = DriftStatus.CLEAN


class HaltError(Exception):
    """Raised when a mid-soak halt criterion fires (CTO Doc 03 §4.1) —
    evaluated continuously during a soak, not only at soak-end, per Doc
    55 §2.2's explicit note that these are real-time triggers."""


@dataclass
class AdvanceCriteria:
    """Doc 33 §2.2's four advance criteria, checked as booleans by the
    caller (the actual SLO/eval/cost data pipelines are out of this
    module's scope — this module only encodes the decision rule)."""

    no_slo_regression: bool
    no_eval_regression: bool
    no_new_error_classes: bool
    no_unexplained_cost_movement: bool

    def met(self) -> bool:
        return all([
            self.no_slo_regression, self.no_eval_regression,
            self.no_new_error_classes, self.no_unexplained_cost_movement,
        ])


class FleetManager:
    def __init__(self) -> None:
        self._coordinates: dict[str, FleetCoordinate] = {}

    def register_tenant(self, coordinate: FleetCoordinate) -> None:
        self._coordinates[coordinate.tenant_id] = coordinate

    def get_coordinate(self, tenant_id: str) -> FleetCoordinate:
        return self._coordinates[tenant_id]

    def propose_ring_advance(
        self, tenant_id: str, blueprint_id: str, to_ring: Ring, criteria: AdvanceCriteria,
    ) -> bool:
        """Doc 55 §2.2's flow: Fleet Manager PROPOSES, a human CONFIRMS
        (Doc 30 §2.2) — this method returns whether the proposal is even
        eligible to be put to a human; it never itself performs the
        registry-level ring mutation (that is Doc 55 §1.3's Registry.promote,
        called only after human confirmation)."""
        if not criteria.met():
            return False  # HALT — advance criteria not met, per Doc 55 §2.2's CHECK step
        coord = self._coordinates[tenant_id]
        for bv in coord.blueprint_versions:
            if bv["blueprint_id"] == blueprint_id:
                current_idx = _RING_ORDER.index(bv["ring"])
                target_idx = _RING_ORDER.index(to_ring)
                if target_idx != current_idx + 1:
                    return False
        return True

    def check_mid_soak_halt(self, criteria: AdvanceCriteria) -> None:
        """Doc 55 §2.2: a mid-soak breach halts immediately, not at
        soak-window-end."""
        if not criteria.met():
            raise HaltError("Automated halt criterion breached mid-soak (CTO Doc 03 §4.1).")

    def check_agent_instance_drift(
        self, tenant_id: str, declared_enabled_agents: list[str], actual_agent_instances: list[str],
    ) -> DriftStatus:
        """The drift class added per Doc 60 §7 item 1 (see module
        docstring): a tenant's Terraform `enabled_agents` (its
        `.habagat-lock`, CTO Doc 03 §1.2) and its actual deployed
        AgentInstance set have diverged. Symmetric difference — an agent
        declared-but-not-deployed OR deployed-but-no-longer-declared both
        count, since Doc 60 §5.3.4's row 4 requires the "removed from
        enabled_agents" case to be caught too (never silently orphaned)."""
        declared = set(declared_enabled_agents)
        actual = set(actual_agent_instances)
        coord = self._coordinates[tenant_id]
        if declared != actual:
            coord.drift_status = DriftStatus.AGENT_INSTANCE_DRIFT
            return DriftStatus.AGENT_INSTANCE_DRIFT
        coord.drift_status = DriftStatus.CLEAN
        return DriftStatus.CLEAN
