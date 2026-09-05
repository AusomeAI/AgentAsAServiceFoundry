"""Provisioning Engine — the tenant-provisioning saga.

Traces to: Doc 55 §3 (this whole service, separate deployable from Fleet
Manager per §3.1), Doc 32 §3 (landing zone apply + isolation canary), Doc
30 §4.2 (zero-snowflake, extended to infra state).

Doc 55 §3.2's rule, restated precisely: a partially-applied Terraform plan
is NEVER manually patched forward. On any apply failure, the engine always
attempts a full `terraform destroy` before surfacing the failure — better
to restart from a known-empty state than reconcile an ambiguous one.

`terraform_client` is injected (a Protocol) so this module's saga logic is
tested without invoking real Terraform — Doc 57 §6.1's "test against
fixtures/fakes, never live systems" principle, applied here too even
though this isn't a connector.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class JobStatus(str, Enum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    FAILED_CANARY = "failed_canary"


class TenantStatus(str, Enum):
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    PROVISIONING_FAILED = "provisioning_failed"


class TerraformClient(Protocol):
    def apply(self, tenant_id: str, config: dict) -> None: ...
    def destroy(self, tenant_id: str) -> None: ...
    def has_existing_state(self, tenant_id: str) -> bool: ...


class CanaryRunner(Protocol):
    def run_isolation_canary(self, tenant_id: str) -> bool: ...


@dataclass
class ProvisioningJob:
    job_id: str
    tenant_id: str
    status: JobStatus
    failure_reason: str | None = None


class ProvisioningEngine:
    def __init__(self, terraform: TerraformClient, canary: CanaryRunner) -> None:
        self._terraform = terraform
        self._canary = canary
        self._jobs: dict[str, ProvisioningJob] = {}

    def provision(self, tenant_id: str, config: dict) -> tuple[ProvisioningJob, TenantStatus]:
        """Doc 55 §3.2's saga, as a single synchronous call for testability
        (the real deployment is async per Doc 51 §2.1; the state machine
        modeled here is identical either way).

        Idempotency (Doc 55 §3.2): if Terraform state already exists for
        this tenant (e.g. a retried command after an engine restart
        mid-job), this resumes rather than re-applies from scratch — the
        injected TerraformClient's `apply` is itself expected to be a plan
        against existing state, so this method only needs to avoid
        skipping the canary/status bookkeeping on a resumed run.
        """
        job_id = f"prov-{tenant_id}"
        job = ProvisioningJob(job_id=job_id, tenant_id=tenant_id, status=JobStatus.RUNNING)
        self._jobs[job_id] = job

        try:
            self._terraform.apply(tenant_id, config)
        except Exception as e:  # noqa: BLE001
            # Doc 55 §3.2: apply failed -> ALWAYS attempt full destroy of
            # whatever was partially created, never patch forward.
            job.status = JobStatus.FAILED
            job.failure_reason = str(e)
            self._terraform.destroy(tenant_id)
            return job, TenantStatus.PROVISIONING_FAILED

        canary_passed = self._canary.run_isolation_canary(tenant_id)
        if not canary_passed:
            job.status = JobStatus.FAILED_CANARY
            job.failure_reason = "isolation canary failed post-apply"
            return job, TenantStatus.PROVISIONING_FAILED

        job.status = JobStatus.SUCCEEDED
        return job, TenantStatus.ACTIVE

    def get_job(self, job_id: str) -> ProvisioningJob:
        return self._jobs[job_id]
