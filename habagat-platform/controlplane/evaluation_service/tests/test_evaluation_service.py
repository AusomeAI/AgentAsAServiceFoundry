import pytest

from controlplane.evaluation_service.service import (
    EvaluationService, JudgeNotCalibratedError,
)
from eval.graders import GradeResult, JudgeCalibration
from eval.runner import CaseResult, SuiteResult


def _suite(passed: bool = True, band: str = "should_escalate") -> SuiteResult:
    grade = GradeResult("hard_rule_adherence", 1.0 if passed else 0.0, passed, "x")
    return SuiteResult(case_results=[CaseResult("c1", band, [grade], 1.0 if passed else 0.0, passed)])


def test_gate_result_is_recorded_as_an_immutable_appended_fact():
    """Doc 55 §4.3: never updated in place — a re-grade is a NEW row."""
    service = EvaluationService()
    baseline = _suite(passed=True)
    current = _suite(passed=True)

    first = service.evaluate_and_record_gate(
        blueprint_id="invoice-ap", version="4.2.0",
        current=current, baseline=baseline, declared_gates={},
    )
    second = service.evaluate_and_record_gate(
        blueprint_id="invoice-ap", version="4.2.0",
        current=current, baseline=baseline, declared_gates={},
    )
    history = service.gate_history_for("invoice-ap", "4.2.0")
    assert len(history) == 2  # both calls appended, neither overwrote the other
    assert first.graded_at != "" and second.graded_at != ""


def test_should_escalate_regression_blocks_the_gate():
    service = EvaluationService()
    baseline = _suite(passed=True, band="should_escalate")
    current = _suite(passed=False, band="should_escalate")
    record = service.evaluate_and_record_gate(
        blueprint_id="invoice-ap", version="4.3.0",
        current=current, baseline=baseline, declared_gates={},
    )
    assert record.decision.passed is False


def test_uncalibrated_judge_scores_are_rejected_as_gate_eligible():
    """Doc 55 §4.4: refuses to accept LLM-as-judge scores as gate-eligible
    without a kappa >= 0.75 calibration record."""
    service = EvaluationService()
    with pytest.raises(JudgeNotCalibratedError):
        service.evaluate_and_record_gate(
            blueprint_id="invoice-ap", version="4.2.0",
            current=_suite(), baseline=None, declared_gates={},
            judge_version="judge-v3-uncalibrated",
        )


def test_calibrated_judge_at_or_above_kappa_bar_is_accepted():
    service = EvaluationService()
    service.record_judge_calibration(
        "judge-v3", JudgeCalibration(judge_version="judge-v3", human_agreement_kappa=0.80, sample_size=50)
    )
    record = service.evaluate_and_record_gate(
        blueprint_id="invoice-ap", version="4.2.0",
        current=_suite(), baseline=None, declared_gates={}, judge_version="judge-v3",
    )
    assert record.judge_version == "judge-v3"


def test_calibrated_judge_below_kappa_bar_is_still_rejected():
    service = EvaluationService()
    service.record_judge_calibration(
        "judge-v4", JudgeCalibration(judge_version="judge-v4", human_agreement_kappa=0.60, sample_size=50)
    )
    with pytest.raises(JudgeNotCalibratedError):
        service.evaluate_and_record_gate(
            blueprint_id="invoice-ap", version="4.2.0",
            current=_suite(), baseline=None, declared_gates={}, judge_version="judge-v4",
        )
