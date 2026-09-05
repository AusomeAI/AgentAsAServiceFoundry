# Screens: Internal Operator Console

> Traces to: Doc 56 §4 (all subsections), Doc 55 §2 (Fleet Manager), Doc 33 §1.1 (Agent Review Board), Doc 33 §6 (incidents)
> Theme: internal-operator throughout.

---

## Fleet Overview — `/fleet`

The operator's equivalent of the customer Console's `Overview` (Doc 56 §4.2).

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Fleet Overview                                    47 tenants · 3 breach │
│                                                                            │
│  [ Fleet Coordinate Matrix component — see components/                   │
│    fleet-coordinate-matrix.md ]                                          │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘
```
- This screen is, deliberately, almost entirely the matrix component — Doc 56 §4.2 gives it no other content, and this design does not add any (a summary chart above the matrix would duplicate what the matrix's own sort-breach-first ordering already communicates faster).
- The header count (`47 tenants · 3 breach`) is the one piece of chrome added beyond the matrix itself, giving the page's `<title>`-equivalent a scannable number before any table row is read — matches the "show the page at rest" principle: the single most important fact (how many tenants are broken right now) is visible without scrolling into the table.

## Drift & Compliance — `/fleet/drift`

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Drift & Compliance                                                       │
│                                                                            │
│  Open drift items                                          [ Filter ▾ ]  │
│  🔴 northwind-health   Config drift — AgentInstance vs .habagat-lock      │
│                        mismatch on support-triage@2.0.0        [ View ]  │
│  🟡 acme-industrial    Infra drift — non-breaking, remediation PR #4471   │
│                        opened automatically                    [ View ]  │
│                                                                            │
│  Policy compliance                                                        │
│  46 / 47 tenants at 100% Azure Policy compliance                          │
│  northwind-health: 1 non-compliant resource — see detail                 │
└──────────────────────────────────────────────────────────────────────────┘
```
- Drift items use the same clean/watch/breach visual vocabulary as the Fleet Overview matrix (shared tokens, `health.*`) — an operator moving between the two screens reads the same color grammar, per Doc 56 §5.2's "visual consistency... an operator moving between the fleet dashboard and a single blueprint's eval history should read the same chart grammar."
- A drift item auto-remediated by an already-opened PR (Doc 55 §2.4) shows its PR link directly in the list — the operator's next action ("go review PR #4471") is one click away, not a fact buried in a detail view.
- The "AgentInstance vs .habagat-lock mismatch" drift class named in the example row is the new drift class flagged in Doc 60 §7 item 1 — its presence here is a design placeholder anticipating that addition, not evidence it's already implemented; noted in design-log.md.

## Ring Rollout Control — `/fleet/rollout`

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Ring Rollout Control                                                     │
│                                                                            │
│  invoice-ap@4.3.0                                    Currently at: R1     │
│  Soaking 3 of 5 days · Design partners: 3 tenants                        │
│                                                                            │
│  Advance criteria                                                         │
│  ✓ No SLO regression        ✓ No eval regression                        │
│  ✓ No new error classes     ⧗ Partner sign-off (2 of 3 received)         │
│                                                                            │
│                                    [ Advance to R2 ]  (disabled — 1 more  │
│                                     sign-off needed)                     │
└──────────────────────────────────────────────────────────────────────────┘
```
- **The Advance button is disabled with the specific blocking reason stated inline**, not just greyed out — Doc 55 §2.2's "Fleet Manager proposes advance... a human confirms" is only a meaningful control if the human confirming can see exactly what's outstanding, not just that something is.
- Advance criteria checklist items use `semantic.success-text` (✓) / `semantic.info-text` (⧗ pending, not yet failing) / `semantic.danger-text` (✗, would appear if a criterion actually failed and halted the soak) — the ⧗ state is distinct from failure, matching Doc 55 §2.2's automated halt criteria being continuously evaluated rather than only checked at soak's end (a criterion can be "still waiting," not yet "failed").
- Confirming Advance is a two-step action (button → inline confirmation "Advance invoice-ap@4.3.0 to R2 for ~9 tenants?" → confirm) since this is a genuinely consequential, hard-to-instantly-reverse fleet action, matching the weight Doc 33 §2.2 gives it.

## Agent Review Board Workspace — `/review-board`

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Agent Review Board                                                       │
│                                                                            │
│  Pending review                                                           │
│  claims-triage@1.4.0     Risk: Medium (B3)          [ Review ]           │
│  contract-review@1.0.0   Risk: High (B4, L3)        [ Review ]           │
│                                                                            │
│  ⚠ Active waivers                                          3 active      │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ invoice-ap@4.1.0 · false_post_rate gate         Expires in 4d   │    │
│  │   Risk: A specific vendor-currency edge case fails the gate     │    │
│  │   Compensating control: 100% human review on affected currency  │    │
│  │───────────────────────────────────────────────────────────────│    │
│  │ support-triage@2.9.0 · groundedness gate        Expires in 21d  │    │
│  └────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```
- **The waiver register (Doc 56 §4.3) is the always-visible widget, exactly as specified** — never collapsed behind a tab or a secondary click, since Doc 56 explicitly requires it be a standing fixture, not a report someone has to remember to pull.
- Escalating visual urgency as expiry nears, per Doc 56 §4.3: >14 days remaining renders in `text.secondary`; 7–14 days in `semantic.warning-text`; <7 days in `semantic.danger-text` with a small pulsing dot (respecting `prefers-reduced-motion` — a static bold treatment substitutes when motion is reduced).
- Risk classification badges (`Medium (B3)`, `High (B4, L3)`) use the same blast-radius/autonomy notation as the rest of the corpus (Doc 00 §3–4) rather than an invented internal-only vocabulary — an operator reading this screen should never need a translation layer back to the documents they already know.

## Incident Dashboard — `/incidents`

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Incidents                                                                │
│                                                                            │
│  🔴 SEV-2  Open 34m   Compensation failure — northwind-health            │
│            invoice-ap reversal of erp.post_invoice failed                │
│            SLA: highest priority (Doc 54 §3.4)          [ Open runbook ]│
│                                                                            │
│  🟡 SEV-3  Open 2h    Elevated escalation rate — acme-industrial         │
│            support-triage escalating 34% vs 8% baseline                  │
│                                                                            │
│  Resolved (last 7 days)                                        12        │
└──────────────────────────────────────────────────────────────────────────┘
```
- Severity badges follow Doc 33 §6's SEV-1–4 definitions exactly, including the compensation-failure class from Doc 54 §3.4 rendered with its own explicit label ("Compensation failure") rather than a generic "run failure" — this is the highest-priority incident class in the whole system and the screen should never make it look like an ordinary failure.
- Each open incident's SLA clock is visible inline (elapsed time since open), not hidden in a detail view — matches the dashboard's job of surfacing what needs attention now.

## Cross-tenant Cost & Margin — `/fleet/economics`

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Cross-tenant Cost & Margin                          Period: Mar 2026    │
│                                                                            │
│  By archetype                                                            │
│    A — high-volume/low-complexity    12 agents   61% GM                 │
│    B — mid                           30 agents   58% GM                 │
│    C — low-volume/high-complexity     8 agents   64% GM                 │
│                                                                            │
│  Portfolio gross margin: 62.3%                    [ View full breakdown ]│
└──────────────────────────────────────────────────────────────────────────┘
```
- Structured identically to CTO Doc 04 §4.4's blended portfolio table — this screen is a live rendering of that exact table, not a reinvented cost dashboard, so a reader moving between the design corpus and the running product recognizes the same shape immediately.
- Gross margin figures use the same tabular-numeric monospace treatment as the customer Console's Cost & Usage screen — the two audiences see the same number-formatting grammar even though the surrounding density differs.

---

## Cross-screen navigation

Matches Doc 56 §4.2's mermaid diagram: all seven screens (Fleet Overview, Drift & Compliance, Ring Rollout Control, Blueprint Registry Browser — not separately specified here as it is a straightforward version-list-and-detail pattern with no novel interaction beyond the existing patterns in this document, Agent Review Board Workspace, Incident Dashboard, Cross-tenant Cost & Margin) are top-level, equal-weight nav items — Doc 56 does not establish a hierarchy among them, and this design does not invent one.
