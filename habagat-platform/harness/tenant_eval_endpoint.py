"""The Harness-internal evaluation endpoint — `POST /internal/v1/evaluate`.

RESOLVES: Doc 55 §6 open question 1 / Doc 59 ADR-19 / Doc 60 §7 item 2 —
"tenant-scoped evaluation compute's exact endpoint" was left unresolved.
Doc 55 §4.2 states tenant-scoped grading compute must run *inside* the
tenant, and Doc 55 §6's own recommendation is adopted here rather than
re-litigated: this is a standing Harness capability, not a temporary job
the control plane deploys per run — it reuses the Harness's own
model-calling and tool-calling infrastructure (the same `agent_fn` seam
eval/runner.py already defines) instead of introducing a second execution
path. The control-plane Evaluation Service (controlplane/evaluation_service)
is the ORCHESTRATOR — it calls this endpoint and receives back only the
aggregate SuiteResult, never raw case content, per Doc 53 §6's allowlist
discipline extended to eval results (Doc 55 §4.2's "only the aggregate
score is returned to the control plane").
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from eval.runner import SuiteResult, run_suite


def handle_evaluate_request(
    corpus_dir: Path,
    agent_fn: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """The Harness-side handler for `POST /internal/v1/evaluate`.

    `corpus_dir` is a TENANT-LOCAL path (tenant-scoped cases never leave
    the tenant, Doc 52 §3.2) and `agent_fn` is the Harness's own
    already-running blueprint invocation — not a separate execution
    engine. Returns only the aggregate shape the control plane is allowed
    to see: per-band pass rates, never case content or model output.
    """
    result: SuiteResult = run_suite(corpus_dir, agent_fn)
    bands = {r.band for r in result.case_results}
    return {
        "overall_pass_rate": result.overall_pass_rate(),
        "band_pass_rates": {band: result.band_pass_rate(band) for band in sorted(bands)},
        "case_count": len(result.case_results),
    }
