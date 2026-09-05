"""Traces to Doc 53 §4.2's worked example — this test uses that exact document
as the positive fixture, since Doc 53 states it "exercises every feature."
"""
import copy

import pytest
import yaml

from spec import validate_agent_spec

VALID_SPEC = yaml.safe_load("""
apiVersion: habagat.dev/v1
kind: Agent
metadata:
  name: ap-invoice-agent
  blueprint: invoice-ap@4.2.0
  owner: pod-finance-ops
  archetype: A2
  useCase: X02
spec:
  objective: >
    Extract, validate and post supplier invoices against purchase orders,
    escalating exceptions to a human reviewer with a reason code, and never
    releasing payment autonomously.
  models:
    primary:  { deployment: gpt-frontier, version: "2026-05-01", maxTokens: 4096 }
    fallback: { deployment: gpt-mid,      version: "2026-04-10" }
    routing: cascade-v2
  memory:
    shortTerm: thread
    longTerm:
      store: cosmos
      scope: entity
      ttlDays: 400
      redact: [pii.email, pii.phone]
  tools:
    - ref: docintel.extract_invoice_fields
      risk: R0
    - ref: erp.lookup_po
      risk: R0
    - ref: erp.three_way_match
      risk: R0
    - ref: erp.post_invoice
      risk: R2
      compensatingAction: erp.reverse_invoice_posting
    - ref: erp.release_payment
      risk: R3
      requiresHumanApproval: true
  retrieval:
    index: acme-vendor-terms
    strategy: hybrid+semantic-rank
    topK: 8
    groundednessMin: 0.85
    citationRequired: true
  autonomy:
    default: L2
    maxPermitted: L3
    blastRadius: B3
  policy:
    bundle: finance/ap-v4
    preconditions:
      - three-way-match.passed
      - amount <= tenant.limits.autoPostCeiling
      - duplicate-check.clear
      - bank-details-unchanged
    humanApprovalRequired: ["amount > 25000", "vendor.new == true", "confidence < 0.90"]
  eval:
    suites: [regression-ap-core, tenant-acme-exceptions]
    gates: { field_accuracy: 0.97, hard_rule_adherence: 1.00, false_post_rate: 0.000 }
  budgets:
    maxSteps: 24
    maxCostPerRunUsd: 0.85
    costPerSuccessfulRunUsd: 0.42
    alertAtPct: 115
  observability:
    traceLevel: full
    retentionDays: tenant_policy
""")


def test_doc53_worked_example_is_valid():
    errors = validate_agent_spec(VALID_SPEC)
    assert errors == [], f"The Doc 53 §4.2 worked example must validate cleanly: {errors}"


def test_r2_tool_without_compensator_is_rejected():
    doc = copy.deepcopy(VALID_SPEC)
    del doc["spec"]["tools"][3]["compensatingAction"]  # erp.post_invoice, R2
    errors = validate_agent_spec(doc)
    assert any("compensatingAction" in e for e in errors)


def test_r3_tool_without_human_approval_flag_is_rejected():
    doc = copy.deepcopy(VALID_SPEC)
    del doc["spec"]["tools"][4]["requiresHumanApproval"]  # erp.release_payment, R3
    errors = validate_agent_spec(doc)
    assert any("requiresHumanApproval" in e for e in errors)


def test_r3_tool_with_requires_human_approval_false_is_rejected():
    """The schema pins requiresHumanApproval to the literal `true` for R3 —
    a spec author cannot declare the field present but set to false."""
    doc = copy.deepcopy(VALID_SPEC)
    doc["spec"]["tools"][4]["requiresHumanApproval"] = False
    errors = validate_agent_spec(doc)
    assert any("requiresHumanApproval" in e or "True" in e for e in errors)


def test_additional_top_level_property_is_rejected():
    """additionalProperties: false at spec.spec — a stray field must fail,
    not be silently ignored. This is the concrete test for Doc 52 §4's
    'schema not conventions' claim, at the spec-authoring layer."""
    doc = copy.deepcopy(VALID_SPEC)
    doc["spec"]["someRandomField"] = "should not be allowed"
    errors = validate_agent_spec(doc)
    assert errors != []


def test_autonomy_default_above_max_permitted_not_caught_by_schema_alone():
    """Doc 52 §1.2's invariant 'autonomy_default <= autonomy_max_permitted'
    is NOT expressible in JSON Schema's enum-only comparison — this is a
    documented limitation, enforced instead in compiler/enforcement.py.
    This test exists to prove the schema does NOT catch it (so nobody
    assumes it's covered here) and points at where it actually is."""
    doc = copy.deepcopy(VALID_SPEC)
    doc["spec"]["autonomy"] = {"default": "L4", "maxPermitted": "L2", "blastRadius": "B3"}
    errors = validate_agent_spec(doc)
    assert errors == [], "schema-level validation cannot express this ordering constraint"
    # See compiler/tests/test_r2_r3_enforcement.py::test_autonomy_default_exceeds_max_permitted_fails_compile
