"""Proves Doc 59 ADR-14 and CTO Doc 03 §3.5: 'a spec missing a compensator on
an R2 tool must fail compile, not just fail a later review.'

Every test here calls compile_agent_spec() — the full pipeline — not just
enforcement.run_all_checks() in isolation, because the requirement is
specifically that COMPILATION fails, not merely that a checker function
would report an error if someone remembered to call it.
"""
import copy
from pathlib import Path

import pytest
import yaml

from compiler.compile import CompileError, compile_agent_spec

GOOD_SPEC = yaml.safe_load("""
apiVersion: habagat.dev/v1
kind: Agent
metadata:
  name: ap-invoice-agent
  blueprint: invoice-ap@4.2.0
  owner: pod-finance-ops
  archetype: A2
  useCase: X02
spec:
  objective: "Extract, validate and post supplier invoices against purchase orders."
  models:
    primary:  { deployment: gpt-frontier, version: "2026-05-01" }
    fallback: { deployment: gpt-mid, version: "2026-04-10" }
  tools:
    - ref: erp.lookup_po
      risk: R0
    - ref: erp.post_invoice
      risk: R2
      compensatingAction: erp.reverse_invoice_posting
    - ref: erp.release_payment
      risk: R3
      requiresHumanApproval: true
  autonomy: { default: L2, maxPermitted: L3, blastRadius: B3 }
  policy: { bundle: finance/ap-v4 }
  eval:
    suites: [regression-ap-core]
    gates: { hard_rule_adherence: 1.0 }
  budgets: { maxSteps: 24, maxCostPerRunUsd: 0.85 }
""")

TOOL_REGISTRY = {
    "erp.lookup_po": {"tool_id": "erp.lookup_po", "risk_class": "R0", "input_schema": {}, "output_schema": {}},
    "erp.post_invoice": {"tool_id": "erp.post_invoice", "risk_class": "R2", "input_schema": {}, "output_schema": {}},
    "erp.release_payment": {"tool_id": "erp.release_payment", "risk_class": "R3", "input_schema": {}, "output_schema": {}},
    "erp.reverse_invoice_posting": {"tool_id": "erp.reverse_invoice_posting", "risk_class": "R2", "input_schema": {}, "output_schema": {}},
}
POLICY_BUNDLES = {"finance/ap-v4": {"hardRules": ["arithmetic_foots", "bank_details_unchanged"]}}


@pytest.fixture()
def spec_path(tmp_path: Path) -> Path:
    p = tmp_path / "agent.yaml"
    p.write_text(yaml.dump(GOOD_SPEC))
    return p


def _write(tmp_path: Path, doc: dict) -> Path:
    p = tmp_path / "agent.yaml"
    p.write_text(yaml.dump(doc))
    return p


def test_good_spec_compiles_successfully(spec_path):
    bundle = compile_agent_spec(spec_path, TOOL_REGISTRY, POLICY_BUNDLES)
    assert bundle.content_digest  # non-empty — digest was actually computed
    assert len(bundle.resolved_tools) == 3


def test_r2_tool_missing_compensator_fails_compile(tmp_path):
    """THE core proof this test suite exists for."""
    doc = copy.deepcopy(GOOD_SPEC)
    del doc["spec"]["tools"][1]["compensatingAction"]  # erp.post_invoice, R2
    path = _write(tmp_path, doc)

    with pytest.raises(CompileError) as exc_info:
        compile_agent_spec(path, TOOL_REGISTRY, POLICY_BUNDLES)

    # Caught by JSON Schema's allOf/if/then (Doc 53 §4.1) — the FIRST layer of
    # the two independent enforcement mechanisms described in
    # compiler/enforcement.py's module docstring. compiler/enforcement.py's
    # own check_r2_tools_have_compensators is the second, redundant layer,
    # exercised directly by test_enforcement_module.py.
    assert "compensatingAction" in str(exc_info.value)


def test_r3_tool_missing_human_approval_fails_compile(tmp_path):
    doc = copy.deepcopy(GOOD_SPEC)
    del doc["spec"]["tools"][2]["requiresHumanApproval"]  # erp.release_payment, R3
    path = _write(tmp_path, doc)

    with pytest.raises(CompileError) as exc_info:
        compile_agent_spec(path, TOOL_REGISTRY, POLICY_BUNDLES)

    assert "requiresHumanApproval" in str(exc_info.value)


def test_r3_tool_with_human_approval_false_fails_compile(tmp_path):
    """Setting the field to false (present, but wrong value) must ALSO fail —
    only the schema's `requiresHumanApproval` field absent case is caught by
    JSON Schema's `required`; the value-is-false case is caught by the const
    constraint in $defs.toolReference AND independently by enforcement.py."""
    doc = copy.deepcopy(GOOD_SPEC)
    doc["spec"]["tools"][2]["requiresHumanApproval"] = False
    path = _write(tmp_path, doc)

    with pytest.raises(CompileError):
        compile_agent_spec(path, TOOL_REGISTRY, POLICY_BUNDLES)


def test_autonomy_default_exceeds_max_permitted_fails_compile(tmp_path):
    """The cross-field invariant JSON Schema cannot express (see
    spec/tests/test_schema_validation.py's documented gap) IS caught here,
    at the compiler layer, per compiler/enforcement.py."""
    doc = copy.deepcopy(GOOD_SPEC)
    doc["spec"]["autonomy"] = {"default": "L4", "maxPermitted": "L2", "blastRadius": "B3"}
    path = _write(tmp_path, doc)

    with pytest.raises(CompileError) as exc_info:
        compile_agent_spec(path, TOOL_REGISTRY, POLICY_BUNDLES)

    assert "autonomy.default" in str(exc_info.value)


def test_lenient_hard_rule_adherence_gate_fails_compile(tmp_path):
    """Doc 36 §3: hard_rule_adherence must be exactly 1.0, never lower —
    a blueprint author cannot loosen this gate even slightly."""
    doc = copy.deepcopy(GOOD_SPEC)
    doc["spec"]["eval"]["gates"]["hard_rule_adherence"] = 0.99
    path = _write(tmp_path, doc)

    with pytest.raises(CompileError) as exc_info:
        compile_agent_spec(path, TOOL_REGISTRY, POLICY_BUNDLES)

    assert "hard_rule_adherence" in str(exc_info.value)


def test_unresolvable_tool_reference_fails_compile(tmp_path):
    doc = copy.deepcopy(GOOD_SPEC)
    doc["spec"]["tools"].append({"ref": "nonexistent.tool", "risk": "R0"})
    path = _write(tmp_path, doc)

    with pytest.raises(CompileError) as exc_info:
        compile_agent_spec(path, TOOL_REGISTRY, POLICY_BUNDLES)

    assert "nonexistent.tool" in str(exc_info.value)


def test_missing_policy_bundle_fails_compile(tmp_path):
    doc = copy.deepcopy(GOOD_SPEC)
    doc["spec"]["policy"]["bundle"] = "does-not-exist"
    path = _write(tmp_path, doc)

    with pytest.raises(CompileError):
        compile_agent_spec(path, TOOL_REGISTRY, POLICY_BUNDLES)


def test_digest_is_stable_for_identical_input(spec_path):
    """Doc 52 §1.2: 'two versions with identical compiled output have the
    same digest and are deduplicated.'"""
    b1 = compile_agent_spec(spec_path, TOOL_REGISTRY, POLICY_BUNDLES)
    b2 = compile_agent_spec(spec_path, TOOL_REGISTRY, POLICY_BUNDLES)
    assert b1.content_digest == b2.content_digest


def test_digest_changes_when_spec_changes(tmp_path):
    doc1 = copy.deepcopy(GOOD_SPEC)
    doc2 = copy.deepcopy(GOOD_SPEC)
    doc2["spec"]["budgets"]["maxSteps"] = 30

    dir_a, dir_b = tmp_path / "a", tmp_path / "b"
    dir_a.mkdir()
    dir_b.mkdir()
    b1 = compile_agent_spec(_write(dir_a, doc1), TOOL_REGISTRY, POLICY_BUNDLES)
    b2 = compile_agent_spec(_write(dir_b, doc2), TOOL_REGISTRY, POLICY_BUNDLES)
    assert b1.content_digest != b2.content_digest
