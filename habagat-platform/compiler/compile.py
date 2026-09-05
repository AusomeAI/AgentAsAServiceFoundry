"""Agent Spec -> signed, content-addressed Agent Bundle.

Traces to: Doc 51 §4.3 (compiler container), Doc 55 §1.2 (versioning and
signing flow), CTO Doc 03 §1.2 (compiler/targets/foundry, targets/portable),
CTO Doc 01 bet B1 (provider-neutral spec, a second compiler target kept warm).

Pipeline (Doc 55 §1.2 sequence diagram):
  1. Parse + JSON-Schema-validate agent.yaml (spec/__init__.py)
  2. Run compile-time safety checks (compiler/enforcement.py) — HALTS on failure
  3. Resolve tool/policy/eval references into a flattened, self-contained document
     (Doc 55 §1.4: "the Agent Bundle is a fully-resolved, self-contained artifact")
  4. Compute the content digest (SHA-256) — Doc 52 §1.2 BlueprintVersion.content_digest
  5. Emit ONE bundle per configured target (targets/foundry primary, targets/portable
     warm spare, CTO Doc 01 bet B1) — NOT signed yet; signing is Doc 55 §1.2's
     Registry-owned final step, deliberately kept out of this module so the
     compiler can be run standalone (e.g. by `habagat eval run`, cli/) without
     requiring HSM signing credentials.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from compiler.enforcement import ComplianceError, run_all_checks
from spec import validate_agent_spec


@dataclass
class AgentBundle:
    """A fully-resolved, self-contained compiled artifact (Doc 55 §1.4).
    The Harness loads exactly this shape at startup (Doc 54's StepExecutor) —
    it never re-resolves blueprint/tool/policy references at runtime."""

    metadata: dict[str, Any]
    spec: dict[str, Any]
    resolved_tools: list[dict[str, Any]]      # full tool declarations, not just refs — Doc 53 §3.1
    policy_bundle: dict[str, Any]              # the hard-rule set this spec's policy.bundle resolves to
    eval_suite_refs: list[str]
    content_digest: str = field(default="")   # set by compute_digest()
    target: str = "foundry"                    # "foundry" (primary) | "portable" (warm spare, bet B1)

    def compute_digest(self) -> str:
        """SHA-256 over the canonical (sorted-keys) JSON of everything except
        the digest field itself and `target` — two targets compiled from the
        same source spec should be traceable to the same logical version even
        though their runtime-specific wiring differs (Doc 52 §1.2: 'two
        versions with identical compiled output have the same digest')."""
        canonical = {
            "metadata": self.metadata,
            "spec": self.spec,
            "resolved_tools": self.resolved_tools,
            "policy_bundle": self.policy_bundle,
            "eval_suite_refs": sorted(self.eval_suite_refs),
        }
        blob = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.content_digest = hashlib.sha256(blob).hexdigest()
        return self.content_digest

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "spec": self.spec,
            "resolved_tools": self.resolved_tools,
            "policy_bundle": self.policy_bundle,
            "eval_suite_refs": self.eval_suite_refs,
            "content_digest": self.content_digest,
            "target": self.target,
        }


class CompileError(Exception):
    """Raised for any failure that halts compilation — parse errors, schema
    violations, or ComplianceError (re-raised as this for a uniform CLI
    exit path). Never silently continues past a failure."""


def load_agent_yaml(path: Path) -> dict[str, Any]:
    try:
        return yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        raise CompileError(f"Failed to parse {path}: {e}") from e


def resolve_tools(spec_doc: dict, tool_registry: dict[str, dict]) -> list[dict[str, Any]]:
    """Resolve each `tools[].ref` to its full declaration from the tool
    registry (Doc 53 §3.1 shape). `tool_registry` is injected (not looked up
    live) so this function is a pure, unit-testable transform — the live
    registry lookup (a filesystem scan of tools/*/declarations/*.json in
    this monorepo, or eventually a Blueprint-Registry-side lookup, Doc 55
    §1.4) is compiler/registry_loader.py's job, kept separate on purpose."""
    resolved = []
    for ref in spec_doc["spec"]["tools"]:
        tool_id = ref["ref"]
        if tool_id not in tool_registry:
            raise CompileError(
                f"Tool '{tool_id}' referenced in agent.yaml but not found in the "
                f"tool registry — Doc 53 §3.1 declarations must exist before a "
                f"blueprint may reference them."
            )
        declaration = dict(tool_registry[tool_id])
        # The blueprint's own risk/compensator/approval OVERRIDE the tool's
        # declared defaults only where the blueprint's is at least as strict —
        # enforcement.py already validated the blueprint's own values are
        # internally consistent (R2->compensator, R3->approval); here we
        # simply carry the blueprint's chosen risk class forward, since a
        # single tool implementation (e.g. a generic REST connector) can be
        # instantiated by different blueprints at different risk classes.
        declaration["risk"] = ref["risk"]
        if "compensatingAction" in ref:
            declaration["compensatingAction"] = ref["compensatingAction"]
        if "requiresHumanApproval" in ref:
            declaration["requiresHumanApproval"] = ref["requiresHumanApproval"]
        resolved.append(declaration)
    return resolved


def compile_agent_spec(
    agent_yaml_path: Path,
    tool_registry: dict[str, dict],
    policy_bundles: dict[str, dict],
    target: str = "foundry",
) -> AgentBundle:
    """The single entry point. Raises CompileError on ANY failure — there is
    no partial-success return value, matching Doc 30 P5 ('nothing ships
    without an eval') and Doc 59 ADR-14 (compile-time, not runtime, failure)."""
    spec_doc = load_agent_yaml(agent_yaml_path)

    schema_errors = validate_agent_spec(spec_doc)
    if schema_errors:
        raise CompileError(
            "agent.yaml failed JSON Schema validation against "
            "spec/agent_spec.schema.json:\n  " + "\n  ".join(schema_errors)
        )

    check_result = run_all_checks(spec_doc)
    if not check_result.passed:
        raise CompileError(
            "agent.yaml failed compile-time safety checks (Doc 59 ADR-14):\n  "
            + "\n  ".join(check_result.errors)
        )

    resolved_tools = resolve_tools(spec_doc, tool_registry)

    policy_ref = spec_doc["spec"]["policy"]["bundle"]
    if policy_ref not in policy_bundles:
        raise CompileError(f"Policy bundle '{policy_ref}' not found (Doc 53 §4.1 policy.bundle).")

    bundle = AgentBundle(
        metadata=spec_doc["metadata"],
        spec=spec_doc["spec"],
        resolved_tools=resolved_tools,
        policy_bundle=policy_bundles[policy_ref],
        eval_suite_refs=spec_doc["spec"]["eval"]["suites"],
        target=target,
    )
    bundle.compute_digest()
    return bundle
