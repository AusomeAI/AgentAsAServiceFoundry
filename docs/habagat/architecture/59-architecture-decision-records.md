# Document 59 — Architecture Decision Records

> Owner: Software Architecture · Status: Engineering standard v1.0
> These ADRs record the application-architecture decisions made across Docs 51–58. They sit below Doc 30's platform-level ADRs (ADR-01 through ADR-08) in scope — this document does not re-decide the two-plane model, single-tenancy, or the harness-owns-policy decisions Doc 30 already made; it records the decisions made *within* those constraints, at the level of services, data, interfaces, and code.

## Executive take

- **Every ADR below states explicitly whether it is a one-way or two-way door**, per the assignment's requirement, and for every one-way door, names the specific hedge — not a vague "we'll monitor it," but the concrete mechanism that limits the cost of being wrong.
- **Most application-architecture decisions here are two-way doors.** This is itself a finding worth stating plainly: at the application layer (as opposed to Doc 30's platform layer, where single-tenancy and the harness-owns-policy decisions are genuinely one-way), most choices — repo layout details, a specific datastore for a specific bounded context, the frontend framework — are reversible within a quarter or two of focused work, because they sit inside the isolation and trust-layer boundaries Doc 30 already fixed. The one-way doors that do exist here are almost all about **immutability and audit trail integrity** (ADR-06, ADR-11, ADR-15), which is a different kind of irreversibility than infrastructure lock-in.
- **Numbering continues from Doc 30's ADR-08** to keep a single, continuous decision log across the platform and application architecture layers, rather than two competing numbering schemes.

---

### ADR-09: Nine deployables, with the Harness as a single deployable per tenant

**Context.** Doc 30/31 named the harness's seven subsystems and eight-context bounded model (Blueprint, Tenant, Run, Policy, Evaluation, Fleet, Identity, Billing) but did not settle how many separate running services these map to. A team of eight engineers must be able to operate whatever we choose.

**Decision.** Nine deployables (Doc 51 §1.2): Blueprint Registry, Fleet Manager, Provisioning Engine, Evaluation Service, Metering & Billing, Habagat Console (two builds, one codebase), and the Habagat Harness (one deployable, replicated per tenant, internally structured as seven modules).

**Alternatives considered.**
- *One service per bounded context per subsystem (≈15+ services).* Rejected: exceeds what eight engineers can operate; most of the split points (Policy Engine, Verifier as separate services from the Run Manager) add network hops to a single logical transaction with no isolation or scaling benefit (Doc 51 §2.2).
- *One monolith for everything, including the Harness, shared across tenants.* Rejected outright — this would violate Doc 30 P1 (physical isolation); the Harness must be per-tenant by construction, which alone forces at least a two-deployable-class system (control plane vs. per-tenant harness).

**Consequences.** Delivery is simpler for a small team; the cost is that the Harness's seven internal modules cannot be scaled or released independently of each other — accepted because their load and release cadence are identical in practice (Doc 51 §2.2).

**Door:** Two-way. Promoting a harness module to its own service (e.g., if a specific connector genuinely needs independent scaling, Doc 57 §1.2) is an additive change, not a rearchitecture — the promotion rule already exists for exactly this eventuality.

---

### ADR-10: Synchronous inside a run, asynchronous across runs

**Context.** Every inter-component call in the system needed a consistent rule for communication style, or the codebase would accumulate ad hoc choices per integration.

**Decision.** Communication inside the boundary of a single agent run (harness internals, harness-to-tool) is synchronous with timeouts and retries. Communication across deployables that serve fleet-level, non-run-blocking concerns (telemetry, billing, provisioning, evaluation) is asynchronous, event-driven, and idempotent (Doc 51 §2.1).

**Alternatives considered.**
- *Fully synchronous control plane* (e.g., the Harness calls Billing synchronously to record a run). Rejected: couples run completion latency to an unrelated service's availability, and violates Doc 34 §7's "tenants continue running" business-continuity property if Billing is down.
- *Fully asynchronous, including inside a run* (e.g., policy checks via a message queue). Rejected per Doc 51 §2.2's detailed justification — partial failure inside a run's control loop has no good answer under this model.

**Consequences.** The system has exactly one narrow, deliberate exception (the kill switch, Doc 53 §5.1, which is synchronous end-to-end across the control-plane boundary) — flagged in Doc 53 §5.1 and Doc 51 §5 open question 1 as needing to be reflected back into Doc 51 explicitly.

**Door:** Two-way, in principle — but changing the default would ripple through every service's client code. Low practical likelihood of reversal; not treated as high-risk because the rule has proven correct in every case examined across Docs 51–58.

---

### ADR-11: BlueprintVersion and EvalResult are immutable once created; corrections are new rows, never edits

**Context.** Both the compiled agent artifact and its evaluation history need to serve as evidence in customer AI Council reviews (Doc 33 §1.4) and regulator-facing audits (CTO Doc 03 §2 "audit pack"). Evidence that can be silently edited is not evidence.

**Decision.** `BlueprintVersion` becomes immutable the moment it is signed (Doc 52 §1.2); `EvalResult` is never updated after `graded_at` (Doc 55 §4.3). A "correction" in either case is a new row referencing the old one, never an `UPDATE`.

**Alternatives considered.** *Mutable records with an audit-log side table.* Rejected: a side table can itself be tampered with or simply not consulted; making the primary record itself immutable is a stronger, simpler guarantee that doesn't depend on every reader remembering to check a separate history table.

**Consequences.** Storage grows monotonically (old versions/results are never deleted) — accepted, since this data is small relative to the tenant-side data volumes driving most storage cost (Doc 32 §7), and the audit value is high.

**Door:** **One-way** — reversing this (allowing in-place edits) would retroactively undermine every audit claim already made using this design. Hedge: the immutability is enforced at the data-access layer (a guard rejecting `UPDATE`/`DELETE` against these tables, Doc 55 §5.3's test pattern applied identically here), not merely by convention, so there is no code path to accidentally "temporarily" violate it under deadline pressure.

---

### ADR-12: Cosmos DB partition keys chosen from access pattern, not entity identity

**Context.** Doc 51 flagged Cosmos partition-key mistakes as "effectively unfixable at scale" and deferred the actual design to this layer.

**Decision.** Two containers for the Harness's Cosmos account: `runs` partitioned by `/instance_id` (serving the dominant "load/resume a run" and "list runs for this instance" patterns) and `memory` partitioned by `/scope_key` (serving the "get all memory for entity X" pattern) — a deliberate split rather than one container serving both, because the query shapes genuinely differ (Doc 52 §3.1).

**Alternatives considered.**
- *Single container, partitioned by `run_id`.* Rejected: makes "list runs for this instance" and "all memory for this entity" both cross-partition fan-outs — the two highest-frequency reads in the system would both be expensive.
- *Partition by `tenant_id`.* Rejected: a tenant with many concurrent instances and runs would create a hot partition, since Cosmos throughput is provisioned per logical partition — `instance_id` gives finer-grained distribution.

**Consequences.** Escalations get their own third container partitioned by `/tenant_id` as a deliberate exception (Doc 52 §3.1), because that specific query (all pending, oldest-first, across instances) is inherently cross-instance — a case where following the "partition by dominant access pattern" principle consistently means *not* reusing the `runs` container's partition scheme.

**Door:** Two-way, but expensive to reverse — a partition-key change requires a full data migration (re-writing every document under a new key). Hedge: the partition-key choice is documented and tested against the specific access patterns in Doc 52 §3.1 *before* any tenant's production data accumulates under it, and a migration runbook exists as a contingency rather than being designed only if the need arises.

---

### ADR-13: Hybrid REST/async for the Control Plane API; cursor-based pagination

**Context.** Needed a single, consistent style for the Control Plane API (Doc 53 §1) serving both internal operators and customers.

**Decision.** REST over HTTPS, resource-oriented, URL-path-versioned, cursor-paginated (Doc 53 §1.2, §1.5), with long-running operations (provisioning, audit export) modeled as async job resources rather than long-held HTTP connections.

**Alternatives considered.**
- *GraphQL.* Rejected: the API's access patterns are well-understood and resource-shaped (list runs, get a blueprint version), not the flexible, client-driven querying GraphQL is suited for; adding a GraphQL layer would be complexity without a corresponding benefit for this specific surface.
- *Offset-based pagination.* Rejected per Doc 53 §1.5 — degrades badly against Cosmos's own continuation-token model and against large tenants' run history.

**Consequences.** Clients (the Console, any customer-side integration) must implement cursor-following rather than page-number navigation — a minor UX constraint (no "jump to page 5") accepted because it is the right trade for the scale involved.

**Door:** Two-way. An API style is the easiest thing in this document to change later without touching the domain model underneath it, since Doc 53's resource model maps directly onto the domain entities of Doc 52 regardless of transport style.

---

### ADR-14: The Agent Spec is the single source of truth for tool risk classification, enforced at compile time

**Context.** CTO Doc 03 §3.5 already established that a spec with an R3 tool and no approval requirement fails CI. This ADR generalizes and records that principle as an application-architecture decision governing the full R0–R3 lifecycle, not just the R3 case.

**Decision.** Every tool reference in an Agent Spec (Doc 53 §4.1's `toolReference` schema) carries its risk class, and the compiler enforces, as a hard compile-time failure (not a warning, not a runtime check): R2 requires `compensatingAction`; R3 requires `requiresHumanApproval: true`. No tool may be called at runtime without having passed this compile-time gate.

**Alternatives considered.** *Runtime-only enforcement* (the Policy Engine checks at call time whether an R2/R3 tool has the required properties). Rejected: this would allow a malformed blueprint to be *signed and deployed* before the defect is caught, wasting a full release cycle and creating a false sense that the signed artifact is trustworthy when it in fact has an unenforceable safety property.

**Consequences.** Blueprint authors get fast, clear feedback (a failed PR) rather than a late-discovered runtime gap. This does add a small amount of friction to blueprint authoring (a forgotten compensator blocks the PR) — accepted as the correct trade given what's at stake.

**Door:** **One-way** in spirit — weakening this to a runtime-only check would be a regression a security review should treat as a serious finding. Hedge: the rule is a small, isolated piece of compiler logic (Doc 53 §4.1's JSON Schema `allOf`/`if`/`then` conditionals), trivial to audit and re-verify with a dedicated test suite (Doc 58 §7), so its correctness is cheap to continuously confirm even though relaxing it would be a significant regression.

---

### ADR-15: The control-plane telemetry allowlist is enforced in code, at the source (inside the tenant), not at the receiving service

**Context.** Doc 30 §2.1's boundary table needed a concrete enforcement mechanism, not just a documented list of allowed fields.

**Decision.** The allowlist (Doc 53 §6.1) is applied by the Telemetry Emitter *inside the tenant*, before any event crosses the network boundary — never by the receiving control-plane service filtering an already-received payload.

**Alternatives considered.** *Filter on receipt at the control-plane service.* Rejected per Doc 53 §6.2's reasoning: a disallowed field would still have transited the network (potentially appearing in intermediate logs) before being discarded — a narrow but real exposure that source-side filtering avoids entirely.

**Consequences.** Every control-plane-bound event type requires its allowlist to be defined and versioned alongside the Harness code that emits it (not alongside the receiving service) — a minor coordination cost, since a new telemetry field requires a change in the tenant-side codebase even though its consumer is a control-plane service.

**Door:** **One-way** — this is, alongside ADR-14, one of the two ADRs in this document that most directly implements Doc 30's core compliance claim ("the control plane never holds customer content"). Reversing the enforcement point would be a fundamental weakening of the isolation architecture, not a minor implementation detail. Hedge: the isolation canary (Doc 30 §2.1, Doc 55 §2.4) is the independent, continuously-running verification that this control is actually working — a second, structurally different check that does not rely on the allowlist code being correct, so a defect in the allowlist enforcement itself would still likely be caught.

---

### ADR-16: React/TypeScript for both Console surfaces, sharing one component library across two separately-deployed builds

**Context.** Doc 51 §5's two-language rule (Python, TypeScript) needed a concrete decision on whether the internal and customer Consoles (Doc 56) are one build with role-based feature toggling or two builds.

**Decision.** Two separately deployed builds of one shared codebase/component library (Doc 56 §5.1) — role separation happens at build time (which routes/features are compiled in), not at runtime via a permission check inside a single bundle.

**Alternatives considered.** *One build, runtime role-gating.* Rejected: this pattern ships every feature's code (including internal-operator-only capabilities like the waiver register, Doc 56 §4.3) to every customer's browser, even if hidden by a permission check — a weaker security posture (client-side code is inspectable) for no operational benefit, since the two audiences' needs are different enough that shared routing logic buys little.

**Consequences.** Two build/deploy pipelines instead of one, but they share the same component source, so the marginal cost is a build-configuration difference, not a maintenance-doubling of UI code.

**Door:** Two-way. Consolidating to one build later, or splitting further into more than two builds, are both low-cost changes relative to the underlying component library, which is unaffected either way.

---

### ADR-17: MCP-first, hand-built long tail; the promotion-to-own-container threshold is volume/risk-based, not fixed by connector type

**Context.** CTO Doc 01 §3 item 12 set the MCP-first strategic direction but left the concrete engineering threshold for "when does a connector get its own deployment" open (Doc 51 §5 open question 2).

**Decision.** A connector is promoted from "module inside the Tool Gateway" to "its own container" when it crosses any of four thresholds: sustained volume >50 calls/minute, any R2/R3 tool touching a top-tier ERP/CRM, an independent release cadence need, or a blocking/long-running operation profile (Doc 57 §1.2).

**Alternatives considered.** *Promote every connector to its own container by default.* Rejected: most connectors in the long tail (Doc 57 §2.5's generic REST connector category) are low-volume and stateless; running a dedicated container for each is unjustified operational overhead for a small team. *Never promote; keep everything as Tool Gateway modules.* Rejected: SAP-class connectors (Doc 57 §2.2) genuinely warrant independent deployment given their risk profile and release cadence.

**Consequences.** A small number of connectors (the top-tier ERP/CRM systems named across Docs 02–21's most common `Systems & tools` entries) will always be promoted; most will not. This is intended and matches the actual shape of the connector population the use-case catalogue implies.

**Door:** Two-way per connector — promotion or demotion of any individual connector is a deployment-topology change with no effect on its Tool Interface contract (Doc 53 §3), so it can be revisited per-connector without touching the framework's design.

---

### ADR-18: Append-only billing ledger reconciled nightly, rather than a strongly-consistent write path

**Context.** Billing correctness needed a design that respects the async-across-boundary rule (ADR-10) while still guaranteeing no double-charge and no silent loss.

**Decision.** `agent_run_ledger` is append-only, unique on `run_id`, with corrections modeled as new rows referencing the original — never an `UPDATE` — and reconciled nightly against the Harness's own local count (Doc 55 §5.1).

**Alternatives considered.** *A distributed transaction spanning the Harness (in-tenant) and Billing (control plane).* Rejected outright: this would require a synchronous cross-boundary call on every run's completion path, violating both ADR-10 and Doc 34 §7's tenant-independence property — a Billing outage would then be able to block run completion, which is precisely the coupling the whole architecture is designed to avoid.

**Consequences.** A brief window can exist where a run has completed but its billing event has not yet reached the ledger — acceptable because the reconciliation job (Doc 55 §5.1) catches any sustained discrepancy, and the ledger's uniqueness constraint means a delayed-but-eventually-delivered event is never lost or double-counted.

**Door:** **One-way**, for the same reason as ADR-11 — this is a financial audit trail, and switching to a mutable ledger later would undermine every reconciliation and dispute-resolution claim made under the append-only design. Hedge: the design is standard practice in financial systems generally (not a novel risk specific to Habagat), and the reconciliation job itself is the continuously-running verification that the approach is working, exactly mirroring the canary/allowlist relationship in ADR-15.

---

### ADR-19: Tenant-scoped evaluation compute executes inside the tenant via the Harness; only aggregate scores cross the boundary

**Context.** Doc 36 §2.1 established that tenant-scoped eval case *content* must never leave the tenant; this document needed to decide *where the grading computation itself runs*, since the Evaluation Service is a control-plane deployable (Doc 51 §1.1) but tenant-scoped cases are not control-plane data.

**Decision.** For tenant-scoped corpora, the actual model-calling and grading execution happens inside the tenant (invoked by the control-plane Evaluation Service as an orchestrator issuing a command, not by it pulling case content out to grade centrally); only the resulting aggregate score crosses back to the control plane, subject to the same allowlist discipline as ADR-15 (Doc 55 §4.2).

**Alternatives considered.** *Pull tenant-scoped case content to the control plane temporarily, grade it, then discard it.* Rejected: "temporarily" is exactly the kind of exception that erodes an isolation guarantee over time (today's temporary pull becomes tomorrow's cached copy); it also directly contradicts Doc 36 §2.1's explicit prohibition on tenant content leaving the tenant "for any purpose."

**Consequences.** The Harness needs an evaluation-execution capability beyond its normal run-execution path (Doc 55 §6 open question 1 recommends this be a new endpoint on the existing Harness API, reusing its model-calling infrastructure, rather than a second execution engine) — flagged there as needing to be finalized in Doc 53 §2.

**Door:** Two-way in mechanism (which specific endpoint/orchestration pattern is used can change), but **one-way in principle** — the "tenant content never leaves for grading" rule itself is as fixed as ADR-15's telemetry rule, for the identical reason (it is a direct extension of Doc 30 P2). Hedge: same as ADR-15 — the isolation canary's scope should explicitly include a check that no tenant-scoped eval case content has ever appeared in the control-plane Eval DB, extending Doc 55 §4.5's storage split into a tested property, not just a documented one.

---

## Summary table

| ADR | Decision | Door | Hedge (if one-way) |
|---|---|---|---|
| 09 | Nine deployables; Harness is one per tenant | Two-way | — |
| 10 | Sync inside a run, async across | Two-way | — |
| 11 | BlueprintVersion/EvalResult immutable | **One-way** | DB-layer guard against UPDATE/DELETE |
| 12 | Cosmos partition keys by access pattern | Two-way (costly) | Documented migration runbook |
| 13 | REST, cursor pagination, URL versioning | Two-way | — |
| 14 | Compile-time R2/R3 enforcement | **One-way** | Small, isolated, continuously tested compiler rule |
| 15 | Telemetry allowlist enforced at source | **One-way** | Isolation canary as independent verification |
| 16 | Two Console builds, shared components | Two-way | — |
| 17 | Volume/risk-based connector promotion | Two-way per connector | — |
| 18 | Append-only billing ledger | **One-way** | Standard financial-systems practice + nightly reconciliation |
| 19 | Tenant-scoped eval compute stays in-tenant | Two-way (mechanism) / **one-way (principle)** | Isolation canary scope extended to eval corpus |

---

## Open questions and decisions required

1. **ADR-19's exact endpoint design** is deferred to Doc 53 §2 per Doc 55 §6 open question 1 — this ADR records the *decision* (in-tenant execution) but not yet the final *interface*.
2. **ADR-12's migration runbook** does not yet exist as a written document — recommend it be authored before the first tenant crosses a data volume where a partition-key change would be genuinely painful, not after.
3. **No conflict found with the binding constraints in Docs 30–36.** Every ADR above operates strictly within the platform-level ADRs in Doc 30 §9 — none of ADR-09 through ADR-19 contradicts, loosens, or attempts to re-litigate Doc 30's ADR-01 (single-tenant), ADR-05 (control plane holds zero customer content), ADR-07 (compensating actions/human approval), or ADR-08 (centralized blueprints, tenant config only). Where this document's decisions implement those platform ADRs concretely (ADR-14 implements Doc 30's ADR-07; ADR-15 and ADR-19 implement Doc 30's ADR-05), that lineage is stated explicitly in each entry above.
