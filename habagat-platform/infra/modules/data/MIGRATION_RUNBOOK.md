# Cosmos DB partition-key migration runbook

> Authored per Doc 59 ADR-12's own hedge ("the migration runbook does not
> yet exist as a written document — recommend it be authored before the
> first tenant crosses a data volume where a partition-key change would be
> genuinely painful, not after") and Doc 60 §7 item 3, which directs this
> to be written as part of `infra/modules/data/`, before any tenant's
> production data accumulates.

## Why this exists

ADR-12 chose `runs` partitioned by `/instance_id` and `memory` partitioned
by `/scope_key` based on the dominant access pattern known at design time.
A partition key is chosen once and is expensive to change after data
volume grows — Cosmos does not support an in-place repartition. This
runbook is the pre-committed plan for the day that choice needs to change,
so a migration is a rehearsed procedure, not an incident.

## When to invoke this runbook

- A tenant's `runs` container develops a hot logical partition (a single
  `instance_id` receiving disproportionate throughput — visible in the
  Log Analytics workspace's Cosmos metrics, Doc 32 §2.1) that request-unit
  provisioning cannot reasonably absorb.
- A new dominant query pattern emerges that ADR-12's original two access
  patterns do not serve well (this would itself first require a new ADR,
  since it revisits ADR-12's decision — see Doc 59's own ADR process).

## Procedure (dual-write / backfill / cutover — the standard Cosmos
## repartition pattern, applied to Habagat's isolation constraints)

1. **Freeze assumption check.** Confirm the affected tenant is not
   mid-provisioning (Doc 55 §3.2's saga) and not in an active fleet-freeze
   (Doc 33 §6) — a migration must never race either.
2. **Create the new container** (new partition key) alongside the existing
   one, inside the *same* per-tenant Cosmos account — this stays entirely
   within the tenant's own isolation boundary (Doc 30 P1); it is never a
   cross-tenant or control-plane operation.
3. **Dual-write phase.** The Harness's Run Manager (`harness/run_manager.py`)
   writes every new/updated `Run`/`MemoryRecord` to both the old and new
   containers for a bake period (recommended: 7 days, matching the shortest
   realistic run-retention window referenced in Doc 31 §2.7).
4. **Backfill.** A one-time job copies historical documents from the old
   container into the new one, keyed identically — idempotent, safe to
   re-run (mirrors the idempotency discipline in `harness/saga.py` and
   `controlplane/billing/ledger.py`).
5. **Read cutover.** Flip Run Manager reads to the new container behind a
   single config flag (a tenant binding value, per Doc 30 §4.2 — never a
   code change). Verify with the tenant's own isolation canary (Doc 32 §3
   step J) before removing the dual-write.
6. **Decommission.** After a second bake period with reads fully on the
   new container and zero dual-write errors, delete the old container.
   Deletion of a Cosmos container is irreversible — this step requires the
   same two-person-review discipline as any other irreversible action in
   this platform (Doc 54 §1.2's R3 human-approval principle, applied here
   as an operational analogue even though this is not an agent tool call).

## What this runbook does not cover

- A repartition that also changes the *consistency level* (§`consistency_policy`
  in `infra/modules/data/main.tf`) — that is a separate, larger change
  requiring its own runbook revision.
- Cross-tenant data movement — this is explicitly out of scope and would
  violate Doc 30 P1; no procedure for it exists or should exist.
