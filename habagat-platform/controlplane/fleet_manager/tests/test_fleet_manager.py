import pytest

from controlplane.fleet_manager.service import (
    AdvanceCriteria, DriftStatus, FleetCoordinate, FleetManager, HaltError,
)


def _good_criteria() -> AdvanceCriteria:
    return AdvanceCriteria(True, True, True, True)


def _bad_criteria() -> AdvanceCriteria:
    return AdvanceCriteria(False, True, True, True)


@pytest.fixture()
def fm() -> FleetManager:
    manager = FleetManager()
    manager.register_tenant(FleetCoordinate(
        tenant_id="acme", platform_version="1.0.0",
        blueprint_versions=[{"blueprint_id": "invoice-ap", "version": "4.2.0", "ring": "R0", "autonomy_current": "L2"}],
    ))
    return manager


def test_propose_ring_advance_succeeds_when_criteria_met(fm):
    assert fm.propose_ring_advance("acme", "invoice-ap", "R1", _good_criteria()) is True


def test_propose_ring_advance_halts_when_criteria_not_met(fm):
    assert fm.propose_ring_advance("acme", "invoice-ap", "R1", _bad_criteria()) is False


def test_propose_ring_advance_rejects_a_skip(fm):
    assert fm.propose_ring_advance("acme", "invoice-ap", "R2", _good_criteria()) is False


def test_mid_soak_halt_raises_immediately_on_breach(fm):
    """Doc 55 §2.2: a mid-soak breach halts immediately, not at soak-end."""
    with pytest.raises(HaltError):
        fm.check_mid_soak_halt(_bad_criteria())
    fm.check_mid_soak_halt(_good_criteria())  # no raise


def test_agent_instance_drift_detected_when_declared_and_actual_diverge(fm):
    """Doc 60 §7 item 1's added drift class."""
    status = fm.check_agent_instance_drift(
        "acme",
        declared_enabled_agents=["invoice-ap@4.2.0", "support-triage@3.0.1"],
        actual_agent_instances=["invoice-ap@4.2.0"],  # support-triage never actually deployed
    )
    assert status == DriftStatus.AGENT_INSTANCE_DRIFT
    assert fm.get_coordinate("acme").drift_status == DriftStatus.AGENT_INSTANCE_DRIFT


def test_agent_instance_drift_clean_when_declared_and_actual_match(fm):
    status = fm.check_agent_instance_drift(
        "acme", declared_enabled_agents=["invoice-ap@4.2.0"], actual_agent_instances=["invoice-ap@4.2.0"],
    )
    assert status == DriftStatus.CLEAN


def test_agent_instance_drift_detects_orphaned_removed_agent(fm):
    """Doc 60 §5.3.4 row 4: removing an agent must never leave it silently
    orphaned and still running — caught here as drift too."""
    status = fm.check_agent_instance_drift(
        "acme", declared_enabled_agents=[], actual_agent_instances=["invoice-ap@4.2.0"],
    )
    assert status == DriftStatus.AGENT_INSTANCE_DRIFT
