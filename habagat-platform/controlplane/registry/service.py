"""Blueprint Registry — storage, versioning, signing, promotion.

Traces to: Doc 55 §1 (this whole service), Doc 52 §1.2 (Blueprint /
BlueprintVersion), Doc 53 §1.2 (the requirements API), Doc 59 ADR (content
digest / immutability once signed).

This module implements the domain/service logic only — the HTTP transport
(Doc 35's Azure Functions/Container Apps binding) is a thin adapter over
this, deliberately not built here: standing up a real HTTP framework to
prove request/response wiring would test infrastructure choices this build
doesn't need to make, not the Registry's actual behavior. See BUILD_LOG.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Ring = Literal["R0", "R1", "R2", "R3"]
_RING_ORDER = ["R0", "R1", "R2", "R3"]


class RegistryError(Exception):
    pass


class DuplicateDigestError(RegistryError):
    """Doc 55 §1.2: the registry verifies a proposed digest is novel before
    signing — a bundle that hashes identically to an existing version is
    a dedup, not a new version."""


class InvalidPromotionError(RegistryError):
    """Doc 55 §1.3: rings only advance forward, never skip, never regress
    via the promote endpoint."""


class UnsignedBundleError(RegistryError):
    """Doc 55 §1.2: the registry never signs an unvalidated bundle — the
    caller must have already run the full CI gate sequence."""


@dataclass
class Requirements:
    """The standardized, closed vocabulary every blueprint (present or
    future) compiles down to — Doc 60 §5.3.2's registry_lookup.tf contract.
    Terraform never learns what a blueprint DOES, only this shape."""

    model_tiers_used: list[str]
    connector_types: list[str]
    requires_search_index: bool
    requires_document_intelligence: bool
    max_autonomy_permitted: str
    risk_class_ceiling: str

    def to_dict(self) -> dict:
        return {
            "model_tiers_used": self.model_tiers_used,
            "connector_types": self.connector_types,
            "requires_search_index": self.requires_search_index,
            "requires_document_intelligence": self.requires_document_intelligence,
            "max_autonomy_permitted": self.max_autonomy_permitted,
            "risk_class_ceiling": self.risk_class_ceiling,
        }


@dataclass
class BlueprintVersion:
    blueprint_id: str
    version: str
    content_digest: str
    requirements: Requirements
    eval_results_summary: dict
    signed: bool = False
    signature: str | None = None
    ring: Ring = "R0"
    superseded_by: str | None = None


@dataclass
class SigningService:
    """Doc 34 §2.2: HSM-backed in production. Injected here — the
    signature itself is not this document's concern, only that signing
    happens strictly after gate-passage and strictly before persistence
    as an immutable version (Doc 55 §1.2)."""

    sign_fn: callable = field(default=lambda digest: f"sig::{digest}")

    def sign(self, digest: str) -> str:
        return self.sign_fn(digest)


class BlueprintRegistry:
    def __init__(self, signing_service: SigningService | None = None) -> None:
        self._signing = signing_service or SigningService()
        self._versions: dict[tuple[str, str], BlueprintVersion] = {}
        self._digests: dict[str, tuple[str, str]] = {}  # digest -> (blueprint_id, version)

    def propose_version(
        self,
        *,
        blueprint_id: str,
        version: str,
        content_digest: str,
        requirements: Requirements,
        eval_results_summary: dict,
        gates_passed: bool,
    ) -> BlueprintVersion:
        """Doc 55 §1.2's sequence: verify digest novelty -> sign -> persist
        at ring:R0. `gates_passed` stands in for "the CI pipeline's full
        gate sequence already ran" (Doc 55 §1.2's "signing is the last
        step, gated on... having already passed") — the Registry itself
        does not re-run those gates, it only refuses to sign without
        having been told they passed."""
        if not gates_passed:
            raise UnsignedBundleError(
                f"Refusing to sign {blueprint_id}@{version}: CI gate sequence has not passed."
            )
        if content_digest in self._digests:
            raise DuplicateDigestError(
                f"Digest {content_digest} already registered as "
                f"{self._digests[content_digest]} — not a new version."
            )
        signature = self._signing.sign(content_digest)
        bp_version = BlueprintVersion(
            blueprint_id=blueprint_id,
            version=version,
            content_digest=content_digest,
            requirements=requirements,
            eval_results_summary=eval_results_summary,
            signed=True,
            signature=signature,
            ring="R0",
        )
        self._versions[(blueprint_id, version)] = bp_version
        self._digests[content_digest] = (blueprint_id, version)
        return bp_version

    def get_requirements(self, blueprint_id: str, version: str) -> Requirements:
        """Doc 53 §1.2 / Doc 60 §5.3.2: GET
        /v1/blueprints/{id}/versions/{version}/requirements — the exact
        endpoint infra/tenant/registry_lookup.tf's `data "http"` block
        queries at plan time."""
        bp_version = self._versions.get((blueprint_id, version))
        if bp_version is None:
            raise RegistryError(f"No such blueprint version: {blueprint_id}@{version}")
        return bp_version.requirements

    def promote(self, blueprint_id: str, version: str, to_ring: Ring) -> BlueprintVersion:
        """Doc 55 §1.3: validates only that the ring transition is
        well-formed (forward, no skip) — does NOT itself judge whether the
        advance evidence is sufficient; that decision belongs to the Fleet
        Manager (Doc 55 §2.2) before this call is ever made."""
        bp_version = self._versions.get((blueprint_id, version))
        if bp_version is None:
            raise RegistryError(f"No such blueprint version: {blueprint_id}@{version}")
        current_idx = _RING_ORDER.index(bp_version.ring)
        target_idx = _RING_ORDER.index(to_ring)
        if target_idx != current_idx + 1:
            raise InvalidPromotionError(
                f"{blueprint_id}@{version} is at {bp_version.ring}; cannot promote to "
                f"{to_ring} (rings advance one step forward, never skip, never regress)."
            )
        bp_version.ring = to_ring
        return bp_version
