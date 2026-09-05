# Screen: Escalation Review

> Console: Customer · Route: `/tenants/{tenantId}/escalations/{escalationId}` · Traces to: Doc 56 §2 (all subsections), Doc 52 §1.2 `Escalation`, Doc 53 §2.3
> This is the most important screen in the product (Doc 56's own executive take). Designed to the letter of §2.2's layout and §2.3's philosophy — no new information architecture introduced.

## Layout (wide, ≥1024px) — single screen, no scroll for the primary decision

```
┌────────────────────────────────────────────────────────────────────────────┐
│  ← Back to queue (3 remaining)                                    ? Shortcuts│
│                                                                              │
│  Invoice INV-4471 — quantity and price variance on a partial delivery      │  ← HEADER, one sentence
│  needs your call.                                                          │     (scale.700, text.primary)
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 🤖 Agent recommends: Escalate                          Confidence 71%│  │  ← RECOMMEND block
│  │ Below the 90% threshold for this blueprint — the quantity and price  │  │
│  │ both changed since the PO was issued, and that combination isn't    │  │
│  │ covered by an auto-approve rule.                                     │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [ Evidence Panel component — see components/evidence-panel.md ]           │  ← EVIDENCE
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ⚠ What the agent is uncertain about                                  │  │  ← UNCERTAIN block
│  │ Whether the price change was pre-agreed with the supplier (no        │  │
│  │ record of a change order was found) or is a billing error.           │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                                 │  ← ACTIONS
│  │ Approve A│  │ Modify  M│  │ Reject  R│                                 │
│  └──────────┘  └──────────┘  └──────────┘                                 │
│                                                                              │
│  [ Reason Chip Picker component — see components/reason-chip-picker.md ]   │  ← REASON
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

This is a direct, literal render of Doc 56 §2.2's mermaid flow (`HEADER → RECOMMEND → EVIDENCE → UNCERTAIN → ACTIONS → REASON`) — no reordering, no added sections.

## Region specifications

### Header
- **Copy formula:** `{subjectLine} needs your call.` where `subjectLine` is generated server-side from the escalation's type and the specific discrepancy (this is backend-owned content per the `EvidenceAssembler`, Doc 54 §8.1 — the design's job is the container, not authoring every possible sentence).
- **Typography:** `typography.scale.700`, `weight.semibold`, `text.primary`.
- Always exactly one sentence. If the backend cannot produce a specific subject line, the fallback is `"This {blueprintDisplayName} run needs your review."` — never a blank header.

### Recommend block
- Background: `bg.surface-sunken`, `radii.md`, `spacing.6` padding (customer density).
- Confidence is always shown as a percentage AND compared explicitly against the blueprint's threshold ("Below the 90% threshold") — never a bare number with no reference point, per Doc 56 §2.2's "WHY it isn't confident enough."
- Robot emoji (🤖) is a deliberate, minimal visual marker distinguishing agent-authored text from the reviewer's own input elsewhere on the screen — not decoration, a comprehension aid (a reviewer scanning quickly should never mistake the agent's stated reasoning for a fact the evidence panel has independently verified).

### Evidence panel
- See [components/evidence-panel.md](../components/evidence-panel.md) in full. Embedded here with `leftLabel`/`rightLabel` populated from the specific run's source documents.

### Uncertain block
- Background: `semantic.warning-bg` at 30% of the picker's full-strength warning treatment (a quieter tint than an actual warning state — this is information, not an alert) — implemented as `semantic.warning-bg` at reduced opacity or a dedicated lighter token; flagged in design-log.md decision #4.
- Always present when the escalation reason is `low_confidence` or `hard_rule_failed`; omitted (region collapses, does not show empty) when the reason is `out_of_policy` or `budget_exhausted`, where there's nothing the agent is "uncertain" about — it hit a hard boundary, not a confidence gap. This conditional omission is a UX decision beyond what Doc 56 specifies — recorded in design-log.md.

### Actions
- Three equal-width buttons, `Approve` primary-styled (`accent.default` fill), `Modify` and `Reject` secondary-styled (outlined).
- Disabled state (Doc 56 §2.5's soft nudge): buttons are visually present but non-interactive (reduced opacity, `cursor: not-allowed`, `aria-disabled="true"` rather than the `disabled` attribute — so screen readers can still announce *why*: `"Approve, unavailable until you've reviewed the evidence below"`) until the evidence panel has been scrolled into view OR a minimum dwell time (provisional 4 seconds, per Doc 56 §2.5 and this document's own open question) has elapsed.
- `Modify` opens the inline editor — see "Modify state" below.

### Reason chip picker
- See [components/reason-chip-picker.md](../components/reason-chip-picker.md) in full.
- Submitting any action with the reason field empty triggers the picker's own error state and blocks submission — the screen itself has no separate validation logic; it delegates entirely to the component per its spec.

## The three action states

### Approve (default flow)
1. Reviewer selects a reason chip or types free text.
2. Reviewer presses `Approve` (button or `A` then `Enter`).
3. Screen transitions to a brief confirmation toast ("Approved — INV-4471 will post to the ERP.") and auto-advances to the next escalation in the queue (`J` behavior applied automatically), per the "seconds, not minutes" standard — the reviewer should not need an extra click to move on.

### Modify (inline editor)
```
┌────────────────────────────────────────────────────────────────────┐
│ Modify before approving                                    [Cancel]│
│                                                                      │
│ Only the fields in question are editable:                          │
│                                                                      │
│   Unit price     $4.35  →  [ $4.20________ ]  ← reset to PO price  │
│   Quantity        600   →  [ 600__________ ]  ← accept as delivered│
│                                                                      │
│                                          [ Confirm modified amount ]│
└────────────────────────────────────────────────────────────────────┘
```
- Opens as an inline panel **within the Actions region**, not a modal — per Doc 53 §2.3 and Doc 56 §3.2's rationale for *not* replicating full editing in Teams: the fields shown are exactly and only the fields the evidence panel flagged as discrepant (`discrepancy: "material"` rows), never the full invoice record. This keeps Modify fast (§2.1's standard) while giving it genuine editing power for the actual point of disagreement.
- Each editable field shows the original agent-extracted value struck through alongside the input, and a one-click "reset to {source}" affordance for the common cases (reset to PO value, accept the delivered/invoiced value as correct).
- `Cancel` collapses the editor back to the three-button state with no changes retained.
- Confirming submits through the same reason-required flow as Approve/Reject.

### Reject
- Identical mechanics to Approve, with the confirmation toast reading "Rejected — INV-4471 will not post. [Blueprint owner] has been notified." (per Doc 52 §1.2's `Escalation` lifecycle: `escalated → failed` on reject).

## Keyboard shortcut overlay

Triggered by `?`, per Doc 56 §2.4:

```
┌─────────────────────────────────────┐
│  Keyboard shortcuts             [Esc]│
│                                       │
│  A          Approve                  │
│  M          Open Modify              │
│  R          Reject                   │
│  1–9        Select reason chip       │
│  Enter      Confirm current action   │
│  J / K      Next / previous          │
│  ?          Show this list           │
└─────────────────────────────────────┘
```
Rendered as a dismissible overlay (`role="dialog"`, `aria-modal="true"`, focus trapped inside, `Escape` or the visible close control dismisses it, focus returns to whatever was focused before it opened) — this is the one place on this screen a modal is appropriate, since it is genuinely a transient reference lookup, not part of the primary task flow.

## Responsive (compact, <1024px)

All regions stack full-width in the same top-to-bottom order; the Evidence Panel switches to its own compact layout (see its spec); the Actions row becomes three stacked full-width buttons rather than three columns, since thumb-width tap targets matter more than horizontal density at this size.

## Empty/edge states

- **Queue exhausted** (no escalations remain): the screen is never reached in this state — the Approval Queue list view (out of this screen's scope, part of the customer Console's `Overview`/`Approval Queue` per Doc 56 §1.3) shows an empty-queue state instead and this route is not navigated to.
- **Escalation already decided** (e.g. opened from a stale Teams notification after another reviewer acted): screen shows a read-only summary — "This was already {approved/rejected} by {name} at {time}." with a link back to the queue — never re-presents the action buttons for an already-decided case.
