# Build log: decisions and gaps

## 0. Follow-up pass (closing gaps found after the initial build)

The initial build's report flagged several deliberate scope decisions.
Two of those turned out, on closer inspection, to be real gaps rather than
legitimate scope cuts — closed in this follow-up pass:

- **Doc 58 §7's E2E terminal-state requirement** ("every terminal state in
  Doc 54 §2.2's diagram has at least one E2E test reaching it") was not
  covered by the initial build's unit tests, which exercised the Run
  Manager's methods and the Saga Coordinator's `unwind()` separately but
  never drove a Run through the full realistic sequence end to end.
  **Closed:** `harness/tests/test_e2e_terminal_states.py`, seven tests
  covering `committed`, `escalated→committed`, `escalated→failed`,
  `failed` (direct, on budget exhaustion), `compensating→failed` (full
  unwind), and `compensation_failed` (partial unwind) — all six required
  terminal states.
- **Doc 54 §5.4's schema round-trip tests** ("valid input passes, each
  required field's absence fails, an extra field is rejected") were
  explicitly deferred in `harness/tool_gateway.py`'s original comment
  ("omitted here in favor of a dedicated jsonschema check in
  tools/contract.py") — but `tools/contract.py` never actually performed
  that check; the deferral pointed at code that didn't exist. This was a
  real, uncovered gap in a Doc 58 §7 zero-tolerance test suite (Tool
  Gateway), not a legitimate scope decision. **Closed:** `ToolGateway.call()`
  now validates arguments against `input_schema` (step 1) and the raw
  connector result against `output_schema` (step 8) via `jsonschema`,
  matching Doc 54 §5.2's exact call sequence; three round-trip tests run
  against the real `blueprints/invoice-ap/tools/declarations.json` (not a
  synthetic fixture), plus the injection-in-result companion test Doc 54
  §5.4 also names ("a companion integration test asserts the Policy
  Engine's envelope... is unchanged by it").
- **Console customer screen was never typechecked** against
  `@habagat/console-shared` (no `tsconfig.json` existed for
  `console/customer/`). Adding one surfaced one real type error (passing
  a lowercase action string where `disabledActionAriaLabel` expects the
  capitalized literal union) — fixed with a template-literal-typed
  `capitalize()` helper rather than a type-cast, so the fix stays real
  under future edits. CI's `console` job now typechecks this screen too.
- **Coverage measured, not just estimated**, on the three subsystems Doc
  58 §7 names as needing ≥90% line coverage: Policy Engine 99%, Verifier
  100%, Saga Coordinator 94% — all comfortably above the bar; the small
  gaps remaining are defensive/unreachable-by-design branches (a Saga
  Coordinator branch handling a `compensating_action_id`-less R2 write,
  which the compiler already refuses to produce per Doc 59 ADR-14).


> Written per the Software Engineer Agent prompt's explicit instruction:
> "When you hit a gap or conflict... record it here rather than silently
> resolving it, using the most conservative reading until a human decides."
> Every entry below is traced to the document/section it concerns.

## 1. Repository-shape decisions

### 1.1 A top-level `harness/` directory not named in CTO Doc 03 §1.2's canonical layout
CTO Doc 03 §1.2 lists the platform monorepo's top-level directories but the
copy quoted into Doc 60 §5's prompt does not explicitly enumerate `harness/`
alongside `spec/`, `compiler/`, `blueprints/`, `tools/`, `policy/`, `eval/`,
`controlplane/`, `console/`, `cli/`, `infra/`. Doc 51 §1.2 and Doc 54 are
unambiguous that the Harness (Run Manager, Policy Engine, Verifier, Saga
Coordinator, Tool Gateway, Memory Manager, Escalation Manager, Telemetry
Emitter) is one deployable and the single most safety-critical piece of
the whole system — it needs its own top-level directory rather than being
squeezed into `controlplane/` (wrong isolation boundary — the Harness runs
*inside* a tenant, never in the control plane) or `tools/` (wrong bounded
context). **Decision:** added `harness/` as a top-level directory. This is
additive, not a deviation from any binding constraint — Doc 30 §2.1's
control-plane/data-plane boundary table is what makes `controlplane/` the
wrong home, so `harness/` is the conservative, spec-consistent choice, not
an invented one.

### 1.2 Nine-deployables headcount reconciliation
Doc 51 §1.2 names "nine deployables total" but then lists eight: Blueprint
Registry, Fleet Manager, Provisioning Engine, Evaluation Service, Metering
& Billing, Habagat Console (two builds of one codebase), and the Habagat
Harness. Taking "two builds" as two separate deployed surfaces (which Doc
51 §1.1's own criteria — different release cadence per surface — supports)
gives eight distinct deployment artifacts by this build's accounting:
registry, fleet_manager, provisioning_engine, evaluation_service, billing,
console-customer, console-internal, harness. This build produced a
Dockerfile + health-check endpoint for exactly these eight. **Flagging,
not resolving:** the doc's own arithmetic doesn't reconcile to nine under
any reading I could construct without inventing a ninth deployable Doc 51
does not name — recommend Doc 51 §1.2 be corrected or clarified by a human
rather than this build guessing at a ninth service.

## 2. Design conflicts found and resolved (conservative reading applied)

### 2.1 `ToolDeclaration`'s R2-compensator rule vs. Doc 53 §3.2's compensator exemption
**Conflict:** Doc 59 ADR-14 requires every R2 tool to declare a
`compensating_action`. Doc 53 §3.2 documents an exemption: a tool that
exists *only* as another tool's compensating action (e.g.
`erp.reverse_invoice_posting`, which compensates `erp.post_invoice`) needs
no compensator of its own, since it is never a forward action a model
chooses to call. A single `ToolDeclaration` object, constructed in
isolation, cannot tell which case it is — that requires registry-wide
visibility into whether some *other* declaration names it as a
compensator.

**Resolution:** `tools/contract.py`'s `ToolDeclaration.__post_init__` now
enforces only the R3 rule (which has no exemption) at construction time.
The full R2 check (real violation vs. documented exemption) is enforced
with registry-wide visibility in `compiler/enforcement.py`
(`check_r2_tools_have_compensators`), which sees the whole blueprint's
tool list and can correctly distinguish the two cases. This is the more
conservative reading: it does not silently accept every R2 declaration,
it moves the check to the layer that can apply it correctly, and that
layer already had test coverage before this fix
(`compiler/tests/test_enforcement_module.py`,
`compiler/tests/test_r2_r3_enforcement.py`).

### 2.2 `three_way_match`'s quantity check: received vs. ordered quantity
**Conflict found while running `tools/erp`'s own test suite:** the
connector's original implementation compared invoiced quantity against
the PO's *received* quantity; the test suite (traceable to Doc 36 §1.1's
inv-edge-0447 worked example) asserts the comparison must be against the
*ordered* quantity — PO-44120 ordered 1000, received 600, invoiced 600;
Doc 36 flags this as a quantity mismatch even though invoiced equals
received. **Resolution:** fixed `tools/erp/connector.py` to compare
against `po.qty` (ordered), matching Doc 36 §1.1's own numbers exactly —
the three-way match's job is to catch "vendor invoiced for less than the
PO commits to," which a received-quantity-only check would miss entirely.

## 3. Gaps named in Doc 60 §7 and Doc 55/59's own open-questions sections, resolved here

### 3.1 AgentInstance-vs-config drift class (Doc 60 §7 item 1)
Doc 55 §2.4's drift table did not name "an enabled_agents declaration and
the actual deployed AgentInstance set have diverged" as a drift class —
only Terraform-state drift and the isolation canary were named.
**Resolution:** added `DriftStatus.AGENT_INSTANCE_DRIFT` and
`FleetManager.check_agent_instance_drift()` in
`controlplane/fleet_manager/service.py`, catching both directions of
divergence (declared-but-not-deployed, and deployed-but-removed — the
latter satisfying Doc 60 §5.3.4 row 4's "never silently orphaned" rule).
Tested in `controlplane/fleet_manager/tests/test_fleet_manager.py`.

### 3.2 Tenant-scoped evaluation compute's exact endpoint (Doc 55 §6 open question 1 / Doc 59 ADR-19, Doc 60 §7 item 2)
**Resolution:** adopted Doc 55 §6's own recommendation — a standing
Harness-internal endpoint reusing the Harness's existing execution
infrastructure, rather than a second execution engine. Implemented as
`harness/tenant_eval_endpoint.py:handle_evaluate_request()`, which wraps
the already-built `eval/runner.py:run_suite()` and returns only the
aggregate shape (`overall_pass_rate`, `band_pass_rates`, `case_count`) —
proven by `harness/tests/test_tenant_eval_endpoint.py` to carry no raw
case content across the control-plane boundary, the same allowlist
discipline `harness/telemetry_emitter.py` already enforces for run
telemetry.

### 3.3 Cosmos migration runbook (Doc 59 ADR-12)
ADR-12 explicitly flagged its own migration runbook as not yet written,
recommending it be authored "before the first tenant crosses a data
volume where a partition-key change would be genuinely painful."
**Resolution:** authored as `infra/modules/data/MIGRATION_RUNBOOK.md` —
the dual-write/backfill/cutover procedure, its trigger conditions, and
what it deliberately does not cover.

### 3.4 The kill-switch's synchronous exception to the async-by-default rule (Doc 53 §5.1, Doc 59 ADR-10, Doc 60 §7 item 4)
This build implements the kill-switch's effect inside
`harness/policy_engine.py`'s Step 7 (`IncidentState.fleet_freeze_active`),
which is evaluated synchronously as part of every envelope computation —
consistent with ADR-10. This build did **not** additionally amend Doc 51
§2.1's prose to state the exception explicitly, since that is a
documentation-only change to a different document, not a build task; it
is called out here per Doc 60 §7 item 4's own framing so it isn't lost.

## 4. Scope deliberately not built, and why

### 4.1 Live HTTP/ASGI transport for the five control-plane services
`controlplane/{registry,fleet_manager,provisioning_engine,evaluation_service,billing}/service.py`
implement the full domain/service logic from Doc 55, each with a real,
passing test suite. None of them stand up a real HTTP framework (FastAPI,
Azure Functions bindings, etc.) — only a `/healthz` WSGI endpoint per
service (Doc 58 §7's explicit requirement) is wired to a real socket.
**Why:** the task instructions say not to invent scope beyond what's
specified, and Doc 35's Azure Functions/Container Apps binding choice is
an infrastructure detail the architecture docs describe but do not
specify down to route-handler code; standing up a full API layer here
would mean guessing at request/response wire formats Doc 53 states only
as OpenAPI-style shapes, not implementing anything the documents actually
pin down. The service classes' public methods *are* the contract Doc 53
describes; a thin HTTP adapter over them is genuinely a separate,
mechanical task.

### 4.2 CLI golden paths beyond the four required minimum
`habagat agent new`, `eval run`, `tenant provision`, `release promote` are
implemented with real logic against the modules built in this repo.
`tenant ephemeral`, `release rollback`, `blueprint new`, `tool new` (CTO
Doc 03 §1.3's remaining rows) exit with a clear, non-zero, documented
"not implemented" error rather than either faking success or being
silently absent — proven by
`cli/tests/test_main.py::test_unimplemented_golden_paths_fail_clearly_not_silently`.
**Why:** each of these needs scaffolding logic (file templates for a new
blueprint/connector, an ephemeral-tenant TTL sweep) that no existing
document specifies precisely enough to build without guessing at file
layouts and defaults the docs never state.

### 4.3 Console app-level bundler/build tooling
`console/shared/` — the actual component library `component-contracts.md`
requires (`<EvidencePanel />`, `<ReasonChipPicker />`) — is built with
real, typed logic and a full passing test suite (27 tests across
`reasonChipPicker.ts`, `evidencePanel.ts`, `escalationReview.ts`), plus
the React components that consume that logic. The Escalation Review
screen (`console/customer/src/screens/EscalationReview.tsx`) composes
them into the exact `HEADER → RECOMMEND → EVIDENCE → UNCERTAIN → ACTIONS
→ REASON` layout the screen spec requires, including the keyboard
shortcut table, the dwell/scroll actions-gate, and the already-decided
read-only state. **Not built:** a real bundler config (Vite/webpack) to
produce the two themed, deployed bundles Doc 59 ADR-16 calls for, and a
DOM-rendering test pass (jsdom/RTL) for the composed screen — the pure
logic every one of the screen's decision rules reduces to is tested and
passing; the markup/rendering layer is written but not exercised by an
automated renderer in this build. This is recorded as a gap, not silently
treated as done: a reviewer should not read "console/ exists" as "console/
is deployable" without this caveat.

### 4.4 `infra/`'s `null_resource` destroy-time provisioner for agent removal
Doc 60 §5.3.4 row 4 requires removing an agent from `enabled_agents` to
call a disable/DELETE, never leave it orphaned. The `hashicorp/http`
provider's `http` resource has no first-class "run this request on
destroy" hook the way its create-time behavior is used in
`infra/modules/agent-instance/main.tf`'s registration calls. **Resolution
taken:** a `null_resource` with a `local-exec` provisioner (`when =
destroy`) calling `curl -X DELETE` against the same internal endpoint —
the conservative, explicit path, rather than inventing a resource shape
the `http` provider doesn't support. Flagged here so a reviewer evaluates
whether a purpose-built Habagat Terraform provider action should replace
this before production use.

### 4.5 Terraform validated only by manual brace/paren balance checks
No `terraform` binary was available in this build environment (no network
path to the Terraform provider registry). Every `.tf` file was written by
hand against Doc 60 §5.3.2's exact given code (reproduced verbatim where
the doc gave it) and manually reviewed; a scripted brace/paren balance
check ran across every file as a minimal sanity check (see the `security`
job in `.github/workflows/ci.yml`, which documents this same limitation
for CI). **This is not equivalent to `terraform validate`** — a reviewer
with `terraform` available should run `terraform validate` and
`terraform fmt -check` before treating `infra/` as CI-clean.

## 5. Five most consequential engineering decisions made within the design's constraints

1. **Pushing the R2-compensator-exemption check from `ToolDeclaration`'s
   constructor to `compiler/enforcement.py`'s registry-wide check**
   (§2.1 above) — the single most important correctness fix, because
   getting it wrong in either direction either breaks a documented,
   legitimate connector pattern or silently accepts a real Doc 59 ADR-14
   violation.
2. **Building `harness/` as its own top-level directory** (§1.1) — keeps
   the single most safety-critical code in the system out of both
   `controlplane/` (wrong isolation boundary) and any grab-bag location,
   making the two-plane architecture's control-plane/data-plane split
   visible in the repository layout itself, not just in code comments.
3. **Resolving the tenant-scoped eval endpoint as a Harness-internal
   capability** (§3.2) rather than a second execution engine — avoids
   duplicating the model/tool-calling infrastructure the Harness already
   has, and keeps the control-plane-never-holds-customer-content property
   intact by construction (only the aggregate crosses the boundary).
4. **Making the Metering & Billing ledger's append-only guarantee a
   database-layer trigger, not just a Python-layer convention**
   (`controlplane/billing/ledger.py`) — belt-and-braces, matching the
   Verifier's own pattern (`harness/verifier.py`'s final write-permission
   re-check): even a future code path that forgets the append-only rule
   is rejected by SQLite itself, proven by a test that issues a raw
   UPDATE/DELETE and asserts it fails.
5. **Deriving every piece of shared tenant infrastructure sizing
   (`model_tiers`, `connector_types`, `deploy_search`,
   `deploy_document_intel`, `deploy_approval_ui`) from the Blueprint
   Registry's requirements API in `infra/tenant/registry_lookup.tf`**,
   with zero hardcoded per-blueprint logic anywhere in the Terraform —
   this is the literal mechanism that makes "blueprint #26 next year
   requires a config-line change, not a module change" true, and it was
   built exactly as Doc 60 §5.3.2 specified rather than approximated.

## 6. What remains stubbed/TODO, summarized

| Area | Status |
|---|---|
| `spec/`, `compiler/`, `policy/`, `eval/`, `harness/` (all 8 modules), `blueprints/invoice-ap/`, `tools/` (3 connectors) | Complete, fully tested (139 Python tests passing, 1 documented skip for crash-resume — needs a real Cosmos-backed integration environment); Doc 54 §2.4/§3.5/§4.4/§5.4's four named test suites and Doc 58 §7's E2E-terminal-state and ≥90%-coverage requirements all verified explicitly, see §0 |
| `controlplane/` (5 services) | Domain/service logic complete and tested; no live HTTP transport (§4.1) |
| `console/shared` | Complete, typed, 27 passing tests; two consuming app builds (`customer/`, `internal/`) have one composed screen each but no bundler pipeline (§4.3) |
| `cli/` | 4 of 8 CTO Doc 03 §1.3 golden paths implemented with real logic; remaining 4 fail loudly, not silently (§4.2) |
| `infra/` | All 5 modules + tenant root module written per Doc 60 §5.3.2's exact specification; not validated by a real `terraform validate` (§4.5); one documented provider-capability gap (§4.4) |
| `.github/workflows/ci.yml` | Full 9-stage pipeline wired to real test suites; IaC-scan stage is a structural stand-in, not `terraform validate` (§4.5) |
| Dockerfiles + health checks | All 8 deployables have a Dockerfile and a passing `/healthz` implementation |
