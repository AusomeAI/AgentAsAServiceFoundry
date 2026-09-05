# Component: Evidence Panel

> Used on: Escalation Review screen (customer), the Teams adaptive card's compact rendering (a reduced subset of this spec — see [screens/teams-card.md](../screens/teams-card.md))
> Traces to: Doc 56 §2.2 ("Evidence panel: the specific PO lines, the specific invoice lines, side by side, with the discrepancy highlighted — not a wall of extracted JSON"), Doc 54 §8.1 EvidenceAssembler
> Theme: customer only (this component does not appear in the internal operator console)

## Purpose

Present exactly what the reviewer needs to confirm or refute the agent's recommendation, in the shape a domain expert reasons in — a side-by-side comparison of two versions of the same fact — never a dump of the underlying JSON. The component is generic over "two comparable record sets with discrepancies," not hardcoded to invoices; the invoice case is the worked example throughout because it's the one Doc 53/54 use, but the same panel renders a claims-adjustment comparison, a KYC-document-vs-declared-detail comparison, etc.

## Data shape (traces to Doc 52 §1.2 `Escalation.evidence`)

The `Escalation.evidence` field is typed `JSON` in Doc 52 — this spec gives it the concrete shape the panel expects, so the Software Engineer Agent implements the `EvidenceAssembler` (Doc 54 §8.1) to emit exactly this, not an ad hoc structure reconciled later.

```typescript
interface EvidencePanelData {
  comparisonType: string;          // e.g. "po_invoice_match" — selects the column labels below
  leftLabel: string;               // e.g. "Purchase Order PO-44120"
  rightLabel: string;              // e.g. "Invoice INV-4471"
  rows: EvidenceRow[];
  sourceRefs: {                    // every value must be traceable — Doc 30 Rule 2 "citation or silence"
    label: string;                 // e.g. "View source document"
    url: string;                   // deep link to the underlying Blob/document (Doc 52 §3.3)
  }[];
}

interface EvidenceRow {
  field: string;                   // e.g. "Quantity", "Unit price", "Delivery date"
  left: { value: string; unit?: string };
  right: { value: string; unit?: string };
  discrepancy: "none" | "minor" | "material";  // drives the visual highlight, see States
  discrepancyNote?: string;        // e.g. "3.6% variance — outside the 2% auto-approve tolerance"
}
```

**Why `discrepancy` is a tri-state enum, not a boolean:** a row can differ trivially (rounding) or materially (the reason this escalated at all); collapsing both to "different" would highlight every row and defeat the "highlighted, not a wall of JSON" purpose. Only `material` rows get the strong visual treatment (States, below); `minor` gets a quieter marker; `none` gets no marker at all.

## Anatomy

```
┌───────────────────────────────────────────────────────────────────┐
│  Purchase Order PO-44120              Invoice INV-4471             │  ← column headers (leftLabel / rightLabel)
├───────────────────────────────────────────────────────────────────┤
│  Quantity              1,000 units      600 units          ⚠ ▲    │  ← material row, both values shown, delta marker
│  Unit price             $4.20            $4.35              ⚠ ▲   │  ← material row
│  Delivery date       2026-03-01       2026-03-01                  │  ← matching row, no marker, no highlight
│  Currency                 USD             USD                     │  ← matching row
├───────────────────────────────────────────────────────────────────┤
│  ⓘ 3.6% price variance — outside the 2% auto-approve tolerance    │  ← discrepancyNote, shown once per material row
│  📄 View source: PO-44120.pdf   📄 View source: INV-4471.pdf      │  ← sourceRefs
└───────────────────────────────────────────────────────────────────┘
```

## States

| State | Visual treatment | Token reference |
|---|---|---|
| **Default (matching row)** | No background tint, standard text color, no marker glyph | `text.primary` on `bg.surface-sunken` |
| **Minor discrepancy** | A small dot marker (●) after the right-hand value, no background tint | `text.secondary` dot, `semantic.info-text` |
| **Material discrepancy** | Left value on `diff.removed-bg`, right value on `diff.added-bg`, an amber ▲ marker, and the row's `discrepancyNote` rendered below the table in a callout | `diff.removed-bg` / `diff.added-bg`, `semantic.warning-text` for the note |
| **Loading** | Skeleton rows (3, matching typical row count) with a shimmer at `motion.moderate` duration, respecting `prefers-reduced-motion` (static grey blocks, no shimmer, if set) | `bg.surface-sunken` skeleton fill |
| **Empty (no evidence rows returned)** | A single centered message: "No comparable records were found for this case." plus the sourceRefs if any exist — never a blank panel, which would look broken rather than intentional | `text.secondary` |
| **Error (evidence assembly failed)** | A callout: "We couldn't load the full comparison. The recommendation and confidence above are still accurate — view source documents directly if you need the detail." plus sourceRefs — the reviewer's ability to decide is never fully blocked by this one component failing | `semantic.danger-bg` callout |
| **Focus (keyboard)** | Focus ring (`border.focus`, 2px, 2px offset) moves row-by-row via arrow keys once the panel has focus; `Tab` enters/exits the panel as one stop, not one stop per row (a table pattern, not a form pattern) | `border.focus` |

## Breakpoints

- **Wide (≥1024px):** side-by-side columns as drawn above.
- **Compact (<1024px):** stacks each row into a labeled pair (`field` as a small caption, then left value, then right value beneath it) rather than horizontal columns — tested to remain scannable on a tablet, per the breakpoint rationale in `base.tokens.json`.

## Accessibility

- Rendered as a semantic `<table>` with `<caption>` = `"Comparison: {leftLabel} vs {rightLabel}"` (visually hidden if the column headers above already convey this, but always present for screen readers).
- Each `<th scope="col">` for the two value columns; `<th scope="row">` for the field name column.
- The discrepancy marker is never color-alone: the ▲/● glyphs and the `discrepancyNote` text carry the meaning; color reinforces but is never the only signal (WCAG 1.4.1).
- `discrepancyNote` callouts use `role="status"` so their appearance is announced to screen-reader users without requiring them to have already found the visual callout.
- Source-document links have accessible names of the form `"View source: {filename}"`, not bare "View source" repeated (screen-reader users navigating by link list need to distinguish them).

## Keyboard behavior

| Key | Action |
|---|---|
| `Tab` (into panel) | Focus moves to the panel as a whole (first focusable element: the first source-document link, or the table if no links) |
| `↓` / `↑` (while focus is inside the table) | Move focus one row down/up |
| `Tab` (out of panel) | Focus moves to the next actionable element on the screen (the "what the agent is uncertain about" section, per Doc 56 §2.2's layout order) |

## Interaction note feeding the "seconds, not minutes" standard

The panel never requires a click to reveal a discrepancy — every material discrepancy is visible in the panel's resting state (per the artifact-design principle "show the page at rest," applied here to the product itself: a reviewer must never expand/click to discover the thing they're being asked to decide about).
