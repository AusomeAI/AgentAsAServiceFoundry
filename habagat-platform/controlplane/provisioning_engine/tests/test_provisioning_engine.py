import pytest

from controlplane.provisioning_engine.service import (
    JobStatus, ProvisioningEngine, TenantStatus,
)


class FakeTerraform:
    def __init__(self, fail_apply: bool = False):
        self.fail_apply = fail_apply
        self.applied: list[str] = []
        self.destroyed: list[str] = []

    def apply(self, tenant_id: str, config: dict) -> None:
        self.applied.append(tenant_id)
        if self.fail_apply:
            raise RuntimeError("quota exhausted")

    def destroy(self, tenant_id: str) -> None:
        self.destroyed.append(tenant_id)

    def has_existing_state(self, tenant_id: str) -> bool:
        return tenant_id in self.applied


class FakeCanary:
    def __init__(self, passes: bool = True):
        self.passes = passes
        self.checked: list[str] = []

    def run_isolation_canary(self, tenant_id: str) -> bool:
        self.checked.append(tenant_id)
        return self.passes


def test_successful_provision_reaches_active():
    tf, canary = FakeTerraform(), FakeCanary(passes=True)
    engine = ProvisioningEngine(tf, canary)
    job, status = engine.provision("acme", {"region": "swedencentral"})
    assert job.status == JobStatus.SUCCEEDED
    assert status == TenantStatus.ACTIVE
    assert tf.destroyed == []


def test_apply_failure_always_destroys_before_surfacing_failure():
    """Doc 55 §3.2's core rule: never patch forward, always destroy."""
    tf, canary = FakeTerraform(fail_apply=True), FakeCanary()
    engine = ProvisioningEngine(tf, canary)
    job, status = engine.provision("acme", {})
    assert job.status == JobStatus.FAILED
    assert status == TenantStatus.PROVISIONING_FAILED
    assert tf.destroyed == ["acme"]  # destroy WAS attempted
    assert canary.checked == []  # canary never runs — apply never succeeded


def test_canary_failure_marks_provisioning_failed_without_destroy():
    """Doc 55 §3.2's diagram: canary failure surfaces as
    provisioning_failed distinctly from an apply failure — it does not
    trigger the apply-failure destroy path (the infrastructure itself
    applied cleanly; it's the isolation guarantee that failed verification,
    which is an alerting/investigation case, not an auto-teardown case)."""
    tf, canary = FakeTerraform(fail_apply=False), FakeCanary(passes=False)
    engine = ProvisioningEngine(tf, canary)
    job, status = engine.provision("acme", {})
    assert job.status == JobStatus.FAILED_CANARY
    assert status == TenantStatus.PROVISIONING_FAILED
    assert tf.destroyed == []
