from pathlib import Path

import pytest

from cli.habagat.main import main

CORPUS_DIR = Path(__file__).resolve().parents[2] / "blueprints" / "invoice-ap" / "evals"


def test_agent_new_golden_path(capsys):
    assert main(["agent", "new", "--blueprint", "invoice-ap@4.2.0", "--tenant", "acme"]) == 0
    out = capsys.readouterr().out
    assert "invoice-ap@4.2.0" in out


def test_eval_run_golden_path_runs_real_corpus(capsys):
    assert main(["eval", "run", "--corpus", str(CORPUS_DIR)]) == 0
    out = capsys.readouterr().out
    assert "overall_pass_rate" in out


def test_eval_run_missing_corpus_directory_errors():
    assert main(["eval", "run", "--corpus", "/nonexistent/path"]) == 1


def test_tenant_provision_missing_config_errors():
    assert main(["tenant", "provision", "--config", "/nonexistent/tenant.yaml"]) == 1


def test_release_promote_golden_path(capsys):
    assert main(["release", "promote", "--agent", "ap-agent", "--to", "R2"]) == 0


@pytest.mark.parametrize("argv", [
    ["tenant", "ephemeral", "--ttl", "72h"],
    ["release", "rollback", "--tenant", "acme", "--agent", "ap-agent"],
    ["blueprint", "new"],
    ["tool", "new", "--mcp"],
])
def test_unimplemented_golden_paths_fail_clearly_not_silently(argv, capsys):
    """These are documented as not implemented (BUILD_LOG.md) — the CLI
    must exit non-zero with a clear message, never silently succeed as if
    it had done something."""
    assert main(argv) == 2
    assert "not implemented" in capsys.readouterr().err
