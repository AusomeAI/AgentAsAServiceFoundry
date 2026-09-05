"""Runs the eval harness against the real invoice-ap corpus (all 5 bands),
using a rule-based stub agent_fn standing in for a live Foundry call —
per Doc 57 §6.1's fixture-only discipline, no test in this suite calls a
live model or a live system."""
from pathlib import Path

from eval.graders import GradeResult
from eval.runner import evaluate_gate, load_cases, run_suite

CORPUS_DIR = Path(__file__).parent.parent.parent / "blueprints" / "invoice-ap" / "evals"


def stub_agent_fn(case: dict) -> dict:
    """A deliberately simple, deterministic stand-in for the real agent:
    replays the case's OWN `expected` block as the actual outcome for the
    happy/variation/should_escalate/adversarial bands, and DELIBERATELY
    gets the edge case wrong (to prove the runner correctly reports a
    failure rather than always reporting success — see
    test_deliberately_wrong_case_is_reported_as_failed)."""
    expected = case["expected"]
    if case["id"] == "inv-edge-0447":
        # Deliberately wrong: commits instead of escalating.
        return {"outcome": "commit", "reason": "wrong_reason", "actions_taken": ["post_to_erp"], "identified_factors": []}
    return {
        "outcome": expected["outcome"],
        "reason": expected["reason"],
        "actions_taken": [],
        "identified_factors": expected.get("mustIdentify", []),
    }


def test_load_cases_finds_all_five_bands():
    cases = load_cases(CORPUS_DIR)
    bands = {c["band"] for c in cases}
    assert bands == {"happy_path", "common_variation", "edge", "adversarial", "should_escalate"}


def test_correct_cases_pass():
    suite = run_suite(CORPUS_DIR, stub_agent_fn)
    non_edge = [r for r in suite.case_results if r.case_id != "inv-edge-0447"]
    assert all(r.passed for r in non_edge), [(r.case_id, r.grades) for r in non_edge if not r.passed]


def test_deliberately_wrong_case_is_reported_as_failed():
    """Proves the runner actually discriminates pass/fail rather than
    always reporting success — the edge case's stub deliberately commits
    instead of escalating, and mustNotDo includes post_to_erp."""
    suite = run_suite(CORPUS_DIR, stub_agent_fn)
    edge_result = next(r for r in suite.case_results if r.case_id == "inv-edge-0447")
    assert edge_result.passed is False
    hard_rule_grade = next(g for g in edge_result.grades if g.grader_name == "hard_rule_adherence")
    assert hard_rule_grade.passed is False


def test_gate_evaluation_blocks_on_should_escalate_regression():
    """Doc 36 §4.1's core regression rule."""
    baseline_agent_fn = lambda case: {
        "outcome": case["expected"]["outcome"],
        "reason": case["expected"]["reason"],
        "actions_taken": [],
        "identified_factors": case["expected"].get("mustIdentify", []),
    }
    baseline = run_suite(CORPUS_DIR, baseline_agent_fn)  # 100% pass on all bands

    def regressed_agent_fn(case: dict) -> dict:
        if case["band"] == "should_escalate":
            return {"outcome": "commit", "reason": "wrong", "actions_taken": ["post_to_erp"], "identified_factors": []}
        return baseline_agent_fn(case)

    current = run_suite(CORPUS_DIR, regressed_agent_fn)
    decision = evaluate_gate(current, baseline, declared_gates={"hard_rule_adherence": 1.0})

    assert decision.passed is False
    assert any("should_escalate" in r for r in decision.reasons)


def test_gate_evaluation_passes_when_no_regression_and_gates_met():
    baseline_agent_fn = lambda case: {
        "outcome": case["expected"]["outcome"],
        "reason": case["expected"]["reason"],
        "actions_taken": [],
        "identified_factors": case["expected"].get("mustIdentify", []),
    }
    baseline = run_suite(CORPUS_DIR, baseline_agent_fn)
    current = run_suite(CORPUS_DIR, baseline_agent_fn)  # identical — no regression
    decision = evaluate_gate(current, baseline, declared_gates={"hard_rule_adherence": 1.0})
    assert decision.passed is True
