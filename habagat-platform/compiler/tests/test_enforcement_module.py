"""Direct unit tests of compiler/enforcement.py's individual checks, in
isolation from JSON Schema — proves the second, redundant enforcement layer
(Doc 54 §7.2's defense-in-depth philosophy applied to the compiler) actually
catches these violations on its own, independent of the schema layer."""
import copy

from compiler.enforcement import run_all_checks

GOOD = {
    "spec": {
        "tools": [
            {"ref": "erp.post_invoice", "risk": "R2", "compensatingAction": "erp.reverse_invoice_posting"},
            {"ref": "erp.release_payment", "risk": "R3", "requiresHumanApproval": True},
        ],
        "autonomy": {"default": "L2", "maxPermitted": "L3"},
        "eval": {"gates": {"hard_rule_adherence": 1.0}},
    }
}


def test_good_spec_passes_all_checks():
    assert run_all_checks(GOOD).passed


def test_r2_without_compensator_caught_by_enforcement_module_directly():
    doc = copy.deepcopy(GOOD)
    del doc["spec"]["tools"][0]["compensatingAction"]
    result = run_all_checks(doc)
    assert not result.passed
    assert any("R2" in e for e in result.errors)


def test_r3_without_approval_caught_by_enforcement_module_directly():
    doc = copy.deepcopy(GOOD)
    del doc["spec"]["tools"][1]["requiresHumanApproval"]
    result = run_all_checks(doc)
    assert not result.passed
    assert any("R3" in e for e in result.errors)


def test_all_errors_collected_in_one_pass():
    """Doc 55 §1's 'collect all errors' philosophy — a spec with THREE
    independent violations reports all three, not just the first."""
    doc = copy.deepcopy(GOOD)
    del doc["spec"]["tools"][0]["compensatingAction"]
    del doc["spec"]["tools"][1]["requiresHumanApproval"]
    doc["spec"]["autonomy"] = {"default": "L4", "maxPermitted": "L1"}
    result = run_all_checks(doc)
    assert not result.passed
    assert len(result.errors) == 3
