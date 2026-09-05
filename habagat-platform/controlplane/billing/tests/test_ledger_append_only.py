"""Doc 55 §5.3's three required tests, plus setup coverage."""
import sqlite3

import pytest

from controlplane.billing.ledger import BillingLedger, ReconciliationDiscrepancy


@pytest.fixture()
def ledger() -> BillingLedger:
    return BillingLedger(sqlite3.connect(":memory:"))


def _event(**overrides) -> dict:
    base = dict(
        run_id="run-1", tenant_id="acme", agent_id="invoice-ap",
        blueprint_version="invoice-ap@4.2.0", outcome="committed",
        cost_usd=0.42, billable=True,
    )
    base.update(overrides)
    return base


def test_duplicate_delivery_is_a_no_op_exactly_one_row(ledger):
    """Doc 55 §5.1 rule 2 / §5.3's duplicate-delivery test."""
    first = ledger.record_billable_event(**_event())
    second = ledger.record_billable_event(**_event())  # same run_id, at-least-once redelivery
    assert first is not None
    assert second is None  # duplicate is silently discarded, not an error
    assert len(ledger.entries_for_tenant("acme")) == 1


def test_ledger_is_never_updated_or_deleted(ledger):
    """Doc 55 §5.3's never-updated test: even a direct raw UPDATE/DELETE
    against the underlying table is rejected by the DATABASE layer itself
    (the trigger installed in ledger.py's schema), not merely discouraged
    by convention at the Python layer."""
    entry = ledger.record_billable_event(**_event())
    assert entry is not None

    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        ledger._conn.execute(
            "UPDATE agent_run_ledger SET cost_usd = 999 WHERE ledger_id = ?", (entry.ledger_id,)
        )

    with pytest.raises(sqlite3.IntegrityError, match="append-only"):
        ledger._conn.execute("DELETE FROM agent_run_ledger WHERE ledger_id = ?", (entry.ledger_id,))

    # Unharmed — the attempted mutations never took effect.
    (row,) = ledger.entries_for_tenant("acme")
    assert row.cost_usd == 0.42


def test_correction_is_a_new_row_never_an_edit(ledger):
    original = ledger.record_billable_event(**_event())
    correction_fields = _event(cost_usd=0.50)
    del correction_fields["run_id"]  # record_correction synthesizes its own run_id
    correction = ledger.record_correction(correction_of=original.ledger_id, **correction_fields)

    entries = ledger.entries_for_tenant("acme")
    assert len(entries) == 2  # original row is untouched, a new row was appended
    assert correction.correction_of == original.ledger_id
    originals = [e for e in entries if e.ledger_id == original.ledger_id]
    assert originals[0].cost_usd == 0.42  # original value survives unchanged


def test_reconciliation_discrepancy_raises_and_does_not_touch_ledger(ledger):
    """Doc 55 §5.3's reconciliation-discrepancy test: seed a Harness-local
    count that disagrees with the ledger; assert the job raises an alert
    and does NOT auto-correct the ledger."""
    ledger.record_billable_event(**_event(run_id="run-1", recorded_at="2026-03-01T00:00:00+00:00"))
    ledger.record_billable_event(**_event(run_id="run-2", recorded_at="2026-03-02T00:00:00+00:00"))

    with pytest.raises(ReconciliationDiscrepancy) as excinfo:
        ledger.reconcile("acme", "2026-03", harness_local_count=5)
    assert excinfo.value.ledger_count == 2
    assert excinfo.value.harness_count == 5

    # No row was added, removed, or changed by the failed reconciliation attempt.
    assert len(ledger.entries_for_tenant("acme")) == 2


def test_reconciliation_within_tolerance_does_not_raise(ledger):
    ledger.record_billable_event(**_event(run_id="run-1", recorded_at="2026-03-01T00:00:00+00:00"))
    ledger.reconcile("acme", "2026-03", harness_local_count=1)  # exact match, no raise
