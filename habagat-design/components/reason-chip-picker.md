# Component: Reason Chip Picker

> Used on: Escalation Review screen (full version), Teams adaptive card (condensed version — top 3 chips only, see [screens/teams-card.md](../screens/teams-card.md))
> Traces to: Doc 56 §2.3 (the flywheel interface), Doc 52 §1.2 `Escalation.decision_reason` (mandatory), Doc 53 §2.3 (server-side validation of `decision_reason`)
> Theme: customer only

## Purpose

Make the mandatory `decision_reason` field fast for the common case (one click) while preserving full nuance for the novel case (free text) — because Doc 36 §2's evaluation-corpus flywheel depends on every decision producing a genuinely informative label, and a rushed "n/a" defeats that purpose entirely. This is the single component doing the most work toward the product's actual moat (the evaluation corpus, Doc 36 executive take).

## Data shape

```typescript
interface ReasonChipPickerData {
  systemReasons: SystemReasonChip[];   // derived 1:1 from Escalation.reason enum, Doc 52 §1.2
  learnedChips: LearnedReasonChip[];   // mined from prior decisions on this blueprint, Doc 56 §2.3
  maxChipsShown: number;               // 9 on the full Console view (keys 1-9, Doc 56 §2.4); 3 on the Teams card
}

interface SystemReasonChip {
  code: "low_confidence" | "out_of_policy" | "hard_rule_failed" | "tool_denied" | "budget_exhausted";
  label: string;              // short chip label, e.g. "Low confidence"
  template: string;           // the auto-fill sentence template, with {placeholders} filled from Escalation.evidence
}

interface LearnedReasonChip {
  id: string;
  label: string;               // e.g. "Partial delivery, price changed mid-shipment"
  template: string;
  usageCount: number;          // drives ranking — most-used chips surface first among learned chips
  blueprintVersion: string;    // chips are versioned with the blueprint, Doc 56 §2.3
}

interface ReasonSelection {
  chipId: string | "free_text" | null;
  text: string;                 // the editable, auto-filled (or freely typed) reason — THIS is what maps to decision_reason
}
```

**Why the template auto-fills rather than submits the label directly:** Doc 56 §2.3 requires the filled sentence to reference the specific case's numbers ("the delivered quantity (600/1000) and the invoiced unit price ($4.35 vs PO $4.20)") — a bare label like "Partial delivery" is not itself an informative eval-corpus label; the *filled* sentence is. The template's `{placeholders}` are populated from the same `Escalation.evidence` shape the Evidence Panel consumes (see [evidence-panel.md](./evidence-panel.md)), so both components read from one data source without divergence.

## Anatomy

```
Reason for your decision (required)

┌──────────────────┐ ┌──────────────────────────────┐ ┌────────────┐
│ 1 Low confidence  │ │ 2 Partial delivery, price     │ │ 3 Wrong PO │  ← chips, numbered
│                   │ │   changed mid-shipment        │ │            │     for keyboard select
└──────────────────┘ └──────────────────────────────┘ └────────────┘
┌───────────────────────────────────────────────────────────────────┐
│ Rejected the auto-post because the delivered quantity (600/1000)  │  ← editable text area,
│ and the invoiced unit price ($4.35 vs PO $4.20) both changed —    │     auto-filled on chip
│ this needs a commercial decision, not just a data fix.            │     select, or blank for
└───────────────────────────────────────────────────────────────────┘     free text
```

## States

| State | Visual treatment | Token reference |
|---|---|---|
| **Chip: unselected** | Outlined pill, `border.default`, `text.primary` label, `accent.subtle-bg` numeral badge in the corner | `radii.full`, `border.default` |
| **Chip: selected** | Filled pill, `accent.default` background, `text.on-accent` label — exactly one chip may be selected at a time (selecting a second chip replaces the text-area content with the new template; selecting the same chip again does not clear a since-edited text area — see Interaction note) | `accent.default` |
| **Chip: hover/focus** | `border.focus` ring, `accent.subtle-bg` background wash | `border.focus` |
| **Text area: empty and required** | Standard border; the field does not show an error until the reviewer attempts to submit (Approve/Modify/Reject) with it empty — no premature red-bordering while the reviewer is still deciding | `border.default` |
| **Text area: submit attempted while empty** | `semantic.danger` border + inline message "A reason is required before you can {approve/reject/modify}." positioned directly below the field | `semantic.danger-text` |
| **Text area: filled (from chip or typed)** | Standard border, no special treatment — a filled field is the unremarkable, expected state | `border.default` |
| **Learned chips: loading** | The system-reason chips (always available instantly, since they're a fixed enum) render immediately; learned chips render a moment later behind a subtle inline skeleton — the picker is never fully blocked waiting on the learned-chip fetch | `bg.surface-sunken` skeleton |

## Keyboard behavior (the primary interaction mode per Doc 56 §2.4)

| Key | Action |
|---|---|
| `1`–`9` | Select the Nth chip shown (system chips first, then learned chips, in the order rendered — the numbering is positional, not semantic, so it stays predictable as learned chips change over time) |
| Selecting a chip | Auto-fills the text area with the chip's template (placeholders resolved); moves focus to the text area with the cursor placed at the end, so the reviewer can immediately start editing if needed |
| `Tab` (from a chip) | Moves to the next chip, then to the text area, then out of the component |
| Typing directly in the text area without selecting a chip | Sets `chipId: "free_text"` — this is tracked distinctly from a chip selection so the eval corpus (Doc 36 §2) can measure what fraction of decisions use a learned chip vs. free text, which is itself a signal about whether the chip vocabulary is keeping pace with real cases |

## Accessibility

- Chips are rendered as a `role="radiogroup"` of `role="radio"` buttons (single-select, matching native radio semantics) — NOT checkboxes, since exactly one may be active.
- Each chip's accessible name includes its position for screen-reader users who aren't using the visual numeral: `"Reason option 2 of 9: Partial delivery, price changed mid-shipment"`.
- The text area has a persistent, non-error-state visible label ("Reason for your decision (required)") — the requirement is stated up front, not sprung on the reviewer only at the error state (WCAG 3.3.2).
- The error message on empty-submit is linked to the field via `aria-describedby`, and focus moves to the text area when the error appears (so a screen-reader user isn't left wondering why nothing happened after pressing Approve).

## Interaction note: preventing "the mandatory field becomes noise"

Per Doc 56 §2.3's central design risk, this component is evaluated on one metric above all others in usability testing: **the proportion of decisions where the submitted `decision_reason` differs from an unedited chip template in a way that adds real information, vs. the proportion that are an unedited template or a near-empty free-text entry.** This is not a visual design property — it's flagged here so the Software Engineer Agent instruments it (a simple string-diff against the original template, logged alongside the decision) and so product/eval leadership can watch it as a live quality signal on the flywheel itself, per Doc 36 §2's own logic applied reflexively to this UI.
