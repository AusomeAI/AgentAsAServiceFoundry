from pathlib import Path

from harness.tenant_eval_endpoint import handle_evaluate_request

CORPUS_DIR = Path(__file__).resolve().parents[2] / "blueprints" / "invoice-ap" / "evals"


def _always_escalate(case: dict) -> dict:
    return {"outcome": "escalated", "reason": "test stub", "actions_taken": [], "identified_factors": []}


def test_evaluate_endpoint_returns_only_aggregate_shape_no_case_content():
    """Doc 55 §4.2: only the aggregate score crosses the control-plane
    boundary — this proves the returned shape carries no raw case content,
    same allowlist discipline as harness/telemetry_emitter.py."""
    result = handle_evaluate_request(CORPUS_DIR, _always_escalate)
    assert set(result.keys()) == {"overall_pass_rate", "band_pass_rates", "case_count"}
    assert result["case_count"] == 5  # the 5 real cases across all 5 bands
    assert isinstance(result["overall_pass_rate"], float)
