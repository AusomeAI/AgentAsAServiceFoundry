"""Metering & Billing — the append-only ledger.

Traces to: Doc 55 §5 (why append-only, not transactionally exact at write
time), Doc 52 §1.2 (Billing entities), Doc 59 ADR-18 (append-only billing
ledger is a one-way-door decision).

Doc 55 §5.1's four rules, restated as code:
  1. Every agent_run.billable event is inserted keyed uniquely on run_id.
  2. A duplicate delivery is a no-op insert (unique constraint violation,
     caught and discarded, not an error).
  3. Nothing in this table is ever UPDATE'd or DELETE'd. A correction is a
     new row with correction_of set, never an edit.
  4. Nightly reconciliation compares ledger vs. Harness-local counts; a
     discrepancy raises an alert and is NEVER auto-corrected by rewriting
     the ledger.

Doc 55 §5.3 names three required tests, all present in
controlplane/billing/tests/test_ledger_append_only.py:
  - duplicate-delivery test
  - never-updated test (a runtime assertion in the data-access layer,
    proven here by a SQLite trigger that makes UPDATE/DELETE fail at the
    database layer itself, not merely at the Python layer — belt and
    braces, matching the Verifier's own belt-and-braces pattern in
    harness/verifier.py)
  - reconciliation discrepancy test
"""
from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal

Outcome = Literal["committed", "escalated", "failed", "cancelled"]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS agent_run_ledger (
    ledger_id TEXT PRIMARY KEY,
    run_id TEXT UNIQUE NOT NULL,
    tenant_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    blueprint_version TEXT NOT NULL,
    outcome TEXT NOT NULL,
    cost_usd REAL NOT NULL,
    billable INTEGER NOT NULL,
    recorded_at TEXT NOT NULL,
    correction_of TEXT REFERENCES agent_run_ledger(ledger_id)
);

-- Doc 55 §5.3's "never-updated test" as a DATABASE-LAYER guard, not just a
-- Python-layer convention: even a future code path that forgets this rule
-- and issues a raw UPDATE/DELETE is rejected by SQLite itself.
CREATE TRIGGER IF NOT EXISTS forbid_ledger_update
BEFORE UPDATE ON agent_run_ledger
BEGIN
    SELECT RAISE(ABORT, 'agent_run_ledger is append-only: UPDATE is forbidden (Doc 55 §5.1 rule 3)');
END;

CREATE TRIGGER IF NOT EXISTS forbid_ledger_delete
BEFORE DELETE ON agent_run_ledger
BEGIN
    SELECT RAISE(ABORT, 'agent_run_ledger is append-only: DELETE is forbidden (Doc 55 §5.1 rule 3)');
END;
"""


@dataclass(frozen=True)
class LedgerEntry:
    ledger_id: str
    run_id: str
    tenant_id: str
    agent_id: str
    blueprint_version: str
    outcome: Outcome
    cost_usd: float
    billable: bool
    recorded_at: str
    correction_of: str | None = None


class LedgerAppendOnlyViolation(Exception):
    """Raised when a caller attempts an UPDATE/DELETE against the ledger
    from the Python layer, before it would even reach the DB trigger."""


class ReconciliationDiscrepancy(Exception):
    """Raised by reconcile() on a mismatch. Never auto-corrects the ledger
    (Doc 55 §5.1 rule 4) — the caller is expected to surface this as a
    finance-facing alert, per §5's mermaid diagram."""

    def __init__(self, tenant_id: str, period: str, ledger_count: int, harness_count: int):
        self.tenant_id = tenant_id
        self.period = period
        self.ledger_count = ledger_count
        self.harness_count = harness_count
        super().__init__(
            f"Ledger/Harness discrepancy for {tenant_id}/{period}: "
            f"ledger has {ledger_count} runs, Harness reports {harness_count}."
        )


class BillingLedger:
    """`conn` is injected — production wires a Cosmos-backed or Azure SQL
    connection (Doc 55 §5.1 names the ledger table; Doc 52 §3.2/§3.3 does
    not pin the exact engine here). SQLite is used directly (not faked) so
    the append-only trigger is real enforcement, not a mock of enforcement.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def record_billable_event(
        self,
        *,
        run_id: str,
        tenant_id: str,
        agent_id: str,
        blueprint_version: str,
        outcome: Outcome,
        cost_usd: float,
        billable: bool,
        recorded_at: str | None = None,
    ) -> LedgerEntry | None:
        """Insert one agent_run.billable event. Doc 55 §5.1 rule 2: a
        duplicate delivery (same run_id) is a no-op, not an error — returns
        None on a duplicate, the newly inserted LedgerEntry otherwise."""
        ledger_id = str(uuid.uuid4())
        recorded_at = recorded_at or datetime.now(timezone.utc).isoformat()
        try:
            self._conn.execute(
                """INSERT INTO agent_run_ledger
                   (ledger_id, run_id, tenant_id, agent_id, blueprint_version,
                    outcome, cost_usd, billable, recorded_at, correction_of)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
                (ledger_id, run_id, tenant_id, agent_id, blueprint_version,
                 outcome, cost_usd, int(billable), recorded_at),
            )
            self._conn.commit()
        except sqlite3.IntegrityError:
            # run_id UNIQUE constraint: exactly the at-least-once-delivery
            # duplicate case Doc 55 §5.1 rule 2 describes. Discarded, not
            # raised — a duplicate is expected traffic, not a bug.
            self._conn.rollback()
            return None
        return LedgerEntry(ledger_id, run_id, tenant_id, agent_id, blueprint_version,
                            outcome, cost_usd, billable, recorded_at, None)

    def record_correction(self, *, correction_of: str, **kwargs) -> LedgerEntry:
        """Doc 55 §5.1 rule 3: a correction is always a NEW row referencing
        the original via correction_of, never an edit to it."""
        run_id = kwargs.pop("run_id", f"correction-{uuid.uuid4()}")
        ledger_id = str(uuid.uuid4())
        recorded_at = kwargs.pop("recorded_at", None) or datetime.now(timezone.utc).isoformat()
        self._conn.execute(
            """INSERT INTO agent_run_ledger
               (ledger_id, run_id, tenant_id, agent_id, blueprint_version,
                outcome, cost_usd, billable, recorded_at, correction_of)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (ledger_id, run_id, kwargs["tenant_id"], kwargs["agent_id"], kwargs["blueprint_version"],
             kwargs["outcome"], kwargs["cost_usd"], int(kwargs["billable"]), recorded_at, correction_of),
        )
        self._conn.commit()
        return LedgerEntry(ledger_id, run_id, kwargs["tenant_id"], kwargs["agent_id"],
                            kwargs["blueprint_version"], kwargs["outcome"], kwargs["cost_usd"],
                            kwargs["billable"], recorded_at, correction_of)

    def entries_for_tenant(self, tenant_id: str) -> list[LedgerEntry]:
        rows = self._conn.execute(
            "SELECT ledger_id, run_id, tenant_id, agent_id, blueprint_version, outcome, "
            "cost_usd, billable, recorded_at, correction_of FROM agent_run_ledger "
            "WHERE tenant_id = ? ORDER BY recorded_at",
            (tenant_id,),
        ).fetchall()
        return [LedgerEntry(r[0], r[1], r[2], r[3], r[4], r[5], r[6], bool(r[7]), r[8], r[9]) for r in rows]

    def count_for_period(self, tenant_id: str, period_prefix: str) -> int:
        """`period_prefix` e.g. '2026-03' matched against recorded_at's
        ISO-8601 prefix."""
        (count,) = self._conn.execute(
            "SELECT COUNT(*) FROM agent_run_ledger WHERE tenant_id = ? AND recorded_at LIKE ?",
            (tenant_id, f"{period_prefix}%"),
        ).fetchone()
        return count

    def reconcile(self, tenant_id: str, period: str, harness_local_count: int, tolerance: int = 0) -> None:
        """Doc 55 §5.1 rule 4 / §5.3's reconciliation-discrepancy test.
        Raises ReconciliationDiscrepancy on a mismatch beyond `tolerance`;
        never touches the ledger itself either way."""
        ledger_count = self.count_for_period(tenant_id, period)
        if abs(ledger_count - harness_local_count) > tolerance:
            raise ReconciliationDiscrepancy(tenant_id, period, ledger_count, harness_local_count)
