# Screens: Customer Console

> Traces to: Doc 56 §1.3 (information architecture), Doc 33 §4 (customer-facing governance surfaces), Doc 55 §6.1–6.3
> Covers every screen in Doc 56 §1.3's mermaid diagram except Escalation Review (its own document, [escalation-review.md](./escalation-review.md), since it's the Approval Queue's destination).

---

## Overview — `/tenants/{tenantId}`

The landing page. Per Doc 56 §1.3: **exactly three things, nothing else on first view.**

```
┌────────────────────────────────────────────────────────────────────┐
│  Contoso Manufacturing                              [Priya ▾]      │
│                                                                      │
│  Needs your attention                                               │
│  ┌────────────────────────┐ ┌────────────────────────┐            │
│  │ 4 escalations waiting   │ │ 1 agent below target    │            │
│  │ Oldest: 6 hours ago     │ │ enterprise-knowledge    │            │
│  │        [ Review now → ] │ │ eval currency: 34d      │            │
│  └────────────────────────┘ └────────────────────────┘            │
│                                                                      │
│  This month                                                         │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Cost to date        $2,340 of $4,000 plan       ▓▓▓▓▓░░░░░ │   │
│  │  Runs completed      6,240          Auto-resolved  91%      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  No open incidents affecting your agents.                          │
│                                                                      │
└────────────────────────────────────────────────────────────────────┘
```

**Design decisions:**
- The "needs your attention" cards are the only clickable primary content — everything else on this screen is read-only summary. This enforces Doc 56 §1.3's "everything else is one click away, not crammed onto the first screen."
- Zero attention items → the cards are replaced with a single quiet line: "Everything's running normally." — never an empty grid of zero-state cards, which reads as broken rather than good news.
- An open incident (rare) replaces the "no open incidents" line with a `semantic.warning-bg` callout naming the incident and linking to its status — this is the one case Overview surfaces something beyond the three named categories, because an active incident affecting the tenant overrides the "exactly three things" rule by necessity.

## Run Explorer — `/tenants/{tenantId}/runs`

```
┌────────────────────────────────────────────────────────────────────┐
│  Runs                                    [ Filter: All agents ▾ ]  │
│                                           [ Filter: Last 7 days ▾ ] │
│  Run ID          Agent            Status      Cost     Started     │
│  run_8f2a...     invoice-ap       Committed    $0.24    2m ago      │
│  run_8f29...     invoice-ap       Escalated    $0.31    5m ago  →   │
│  run_8f28...     support-triage   Committed    $0.09    6m ago      │
│  run_8f27...     invoice-ap       Failed       $0.18    8m ago      │
└────────────────────────────────────────────────────────────────────┘
```
- A row's Status cell uses the same semantic color mapping across the whole Console: `committed` → `semantic.success-text`, `escalated` → `semantic.warning-text` (with a `→` affordance linking straight to Escalation Review, per Doc 56 §1.3's `RUNS --> QUEUE` edge), `failed`/`compensation_failed` → `semantic.danger-text`.
- Clicking any row opens a run-detail panel (a slide-over, not a navigation) showing the full trace summary: steps, tool calls (with denied ones visibly marked, not hidden), verification result, and cost breakdown — the customer-facing rendering of Doc 31 §5's "what a good trace looks like" checklist, filtered to what a business user (not an engineer) needs: no raw span IDs, no internal model-deployment names, plain-language step descriptions.
- Table columns match `run.completed` event fields (Doc 53 §5.2) exactly — no field is invented that isn't already in that contract.
- `Run ID` is monospace (`typography.fontFamily.mono`) and truncated with a copy-to-clipboard affordance on hover/focus — customers reference these in support conversations.

## Approval Queue — `/tenants/{tenantId}/escalations`

```
┌────────────────────────────────────────────────────────────────────┐
│  Approval Queue                                    4 waiting        │
│                                                                      │
│  ⏱ 6h    Invoice INV-4471 — quantity/price variance    invoice-ap  │
│  ⏱ 2h    Invoice INV-4502 — new supplier, first invoice invoice-ap │
│  ⏱ 40m   Ticket #8821 — refund above auto-approve       support-tri│
│  ⏱ 12m   Invoice INV-4519 — duplicate suspected          invoice-ap│
└────────────────────────────────────────────────────────────────────┘
```
- Sorted oldest-first by default (matching the SLA-tracking priority in Doc 54 §8.1 SLATracker) — the queue's ordering is not cosmetic, it reflects the actual escalation urgency model.
- The ⏱ age indicator changes color as it approaches the SLA: `text.secondary` under half the SLA window, `semantic.warning-text` past half, `semantic.danger-text` past the full SLA (an aged item that's been re-escalated per Doc 54 §8.1).
- Each row is the full clickable target, navigating to [escalation-review.md](./escalation-review.md) — no separate "review" button needed since the whole row is one decision waiting to happen.
- Empty state: a plain, positive message — "Nothing waiting for your review." — not a generic "no data" pattern, since an empty queue is a good outcome here, distinct from an empty Run Explorer filter result which is neutral.

## Policy Control — `/tenants/{tenantId}/instances/{instanceId}/policy`

```
┌────────────────────────────────────────────────────────────────────┐
│  invoice-ap · v4.2.0                                                │
│                                                                      │
│  Autonomy level                                                     │
│  ○ L1 Draft   ● L2 Recommend + approve   ○ L3 Act with escalation  │
│                                            (requires promotion gate)│
│                                                                      │
│  Value limits                                                       │
│    Max invoice amount for auto-post    $ [ 10,000____ ]            │
│    (blueprint default: $25,000 — you may only set this lower)      │
│                                                                      │
│  Operating hours                                                     │
│    Automated actions permitted    [ 06:00 ] to [ 22:00 ]  Local    │
│                                                                      │
│                                              [ Save changes ]        │
└────────────────────────────────────────────────────────────────────┘
```
- **The autonomy selector directly encodes Doc 54 §4.1's "tighten only" rule at the UI level, not just the API level:** L3/L4 radio options are only selectable if the current instance has actually met the promotion gate (Doc 33 §1.4) — otherwise shown disabled with the tooltip/inline text "requires promotion gate" and a link to what that means, never silently hidden (a customer should be able to see the ceiling they haven't yet reached, per Doc 33 §4's "agent inventory... what it is permitted to do" transparency commitment). Downgrading (moving the selector left) is always immediately available with no gate, matching Doc 33 §4's "adjust autonomy (downward without approval, upward with the gate)."
- **The value-limit field explicitly states the blueprint's own default and enforces the tighten-only direction in the input itself** — attempting to type a value above $25,000 shows inline validation ("You can only set this at or below the blueprint's default of $25,000.") rather than silently clamping it, so the customer understands *why*, matching Doc 54 §4.1's narrowing-only design made visible.
- Saving triggers the same `PATCH /v1/tenants/{tenantId}/instances/{instanceId}/autonomy` contract as Doc 53 §1.2 — no separate save mechanism invented for the value-limits/hours fields; they are all part of one `policy_overrides` update.

## Audit Export — `/tenants/{tenantId}/audit-export`

```
┌────────────────────────────────────────────────────────────────────┐
│  Export audit history                                                │
│                                                                      │
│  From  [ 2026-02-01 ]   To  [ 2026-03-01 ]                          │
│  Format  ● JSON   ○ CSV                                              │
│                                                          [ Export ]  │
│                                                                      │
│  Recent exports                                                     │
│    2026-03-05 · Feb 2026 · JSON      Ready — [ Download ]           │
│    2026-02-04 · Jan 2026 · CSV       Ready — [ Download ]           │
└────────────────────────────────────────────────────────────────────┘
```
- This is an async job (Doc 55 §6.3) — the screen never blocks on export generation. Submitting shows the new job appearing in "Recent exports" immediately with status "Preparing…", polling (via the same SSE channel as Doc 56 §1.1) until "Ready."
- Download links are time-limited SAS URLs per Doc 55 §6.3 — the UI shows an expiry note under a link once it's more than 24 hours old: "This link expires in 6 days."

## Model Cards — `/tenants/{tenantId}/instances/{instanceId}/model-card`

```
┌────────────────────────────────────────────────────────────────────┐
│  invoice-ap · v4.2.0                                    L2 · Live   │
│                                                                      │
│  What this agent does                                                │
│  Extracts, validates and posts supplier invoices against purchase   │
│  orders, escalating exceptions to a human reviewer...                │
│                                                                      │
│  Evaluation results                        Human oversight design    │
│  Happy path         98.2%                  Every automated write is  │
│  Common variation    96.1%                  reversible. Payment      │
│  Edge cases          94.0%                  release always requires  │
│  Adversarial        100.0%                  human approval.          │
│  Should-escalate    100.0%  ← required                               │
│                                                                      │
│  Known limitations                                                   │
│  Does not handle invoices in currencies outside USD/EUR/GBP...       │
│                                                                      │
└────────────────────────────────────────────────────────────────────┘
```
- **This screen is generated, not authored** (per Doc 55 §6.2) — the design's job is the presentation shape, sourced from `spec.objective` (What this agent does), Evaluation Service results by band (Evaluation results — the should-escalate band is visually marked as the one that must read 100% or near it, per Doc 36 §1's own emphasis on that band's importance), and the policy bundle's human-gate declarations (Human oversight design).
- Band scores below their gate threshold render in `semantic.warning-text`/`semantic.danger-text` rather than the default `text.primary` — a model card should make a failing band visible to the customer reading it, not just to Habagat internally.

## Cost & Usage — `/tenants/{tenantId}/billing`

```
┌────────────────────────────────────────────────────────────────────┐
│  This month                                        Plan: Standard  │
│  ▓▓▓▓▓▓▓░░░░░░░░░░░  $2,340 of $4,000 committed usage               │
│                                                                      │
│  By agent                                                            │
│    invoice-ap          4,120 runs   $1,810                          │
│    support-triage      2,120 runs   $   530                         │
│                                                                      │
│  [ View invoice history ]                                            │
└────────────────────────────────────────────────────────────────────┘
```
- Cost figures use `typography.fontFamily.mono` with `font-variant-numeric: tabular-nums` for column alignment (per the artifact-design rule for digit columns) — applied consistently to every monetary/count table across this document.
- No agent's individual cost line ever appears without its run count alongside it — a bare dollar figure with no volume context invites a customer to misread cost-per-run trends.

---

## Cross-screen navigation

Matches Doc 56 §1.3's mermaid diagram exactly: `Overview → Run Explorer`, `Overview → Approval Queue`, `Run Explorer → Approval Queue` (via an escalated run's row), `Policy Control → Kill Switch` (the kill switch is a confirmation-gated destructive action reachable from Policy Control, not a separate top-level nav item — see design-log.md decision #5 for why it isn't given its own prominent nav slot).
