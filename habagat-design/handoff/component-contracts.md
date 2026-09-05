# Handoff: Component & Screen Contracts

> Consumed by: the Software Engineer Agent (Doc 60 §5, §6). This is the single file to read before writing any Console component — it is a flat index of every exact data shape, keyboard behavior, and ARIA requirement, cross-referenced to its full spec, so nothing here needs to be inferred from a screenshot.

## Component prop contracts

### `<EvidencePanel />`
Full spec: [components/evidence-panel.md](../components/evidence-panel.md)

```typescript
type EvidencePanelProps = {
  data: EvidencePanelData;          // see full spec — maps directly to Escalation.evidence (Doc 52 §1.2)
  loading?: boolean;
  error?: { message: string };      // renders the specific fallback copy given in the spec's Error state — do not substitute a generic error component
};
```
- Renders as `<table>` with `<caption>`, `scope="col"`/`scope="row"` headers.
- Focus order: source-doc links → table (row-by-row via `↓`/`↑`) → next screen region.
- Never invent a loading spinner in place of the specified skeleton-row treatment.

### `<FleetCoordinateMatrix />`
Full spec: [components/fleet-coordinate-matrix.md](../components/fleet-coordinate-matrix.md)

```typescript
type FleetCoordinateMatrixProps = {
  rows: FleetMatrixRow[];           // see full spec — maps to Doc 55 §2.1 FleetCoordinate
  onRowActivate: (tenantId: string) => void;   // Enter or click navigates to tenant detail (see open item below)
  filter?: { ring?: string; healthTier?: "clean" | "watch" | "breach" };
};
```
- **Contract requirement on the backend, not just the frontend:** any `health !== "clean"` row MUST include a non-empty `healthReason`. Reject this in the API response schema (Doc 53 §1), not only in the component — a silent fallback ("no reason given") in the UI would mask a backend contract violation.
- Sort order is fixed: breach → watch → clean, then alphabetical `displayName` within each tier. Do not make this configurable — the spec is explicit that this ordering is the point.
- **Open item:** `onRowActivate`'s destination (tenant detail view) has no corresponding screen spec in this handoff — per Doc 60 §6's protocol, this is a gap. Route back to the UI/UX Designer Agent for a follow-up screen spec before building tenant detail; do not invent its layout.

### `<ReasonChipPicker />`
Full spec: [components/reason-chip-picker.md](../components/reason-chip-picker.md)

```typescript
type ReasonChipPickerProps = {
  systemReasons: SystemReasonChip[];
  learnedChips: LearnedReasonChip[];
  maxChipsShown: number;             // 9 on Console, 3 on the Teams card's condensed rendering
  value: ReasonSelection;
  onChange: (selection: ReasonSelection) => void;
  submitAttempted: boolean;          // controls whether the empty-field error state shows (see spec)
};
```
- `role="radiogroup"` / `role="radio"` on chips — not checkboxes, not a native `<select>`.
- Numeral keys `1`–`9` map positionally to rendered chip order (system chips first, then learned) — this must be recalculated live if `learnedChips` changes; do not hardcode the numeral-to-chip mapping.
- Track and log whether the final submitted text is an unedited template, an edited template, or pure free text (see the component spec's "Interaction note") — this is a required instrumentation point, not optional telemetry.

## Screen contracts

| Screen | Route | Full spec |
|---|---|---|
| Escalation Review | `/tenants/{tenantId}/escalations/{escalationId}` | [screens/escalation-review.md](../screens/escalation-review.md) |
| Overview | `/tenants/{tenantId}` | [screens/customer-console.md](../screens/customer-console.md) §Overview |
| Run Explorer | `/tenants/{tenantId}/runs` | [screens/customer-console.md](../screens/customer-console.md) §Run Explorer |
| Approval Queue | `/tenants/{tenantId}/escalations` | [screens/customer-console.md](../screens/customer-console.md) §Approval Queue |
| Policy Control | `/tenants/{tenantId}/instances/{instanceId}/policy` | [screens/customer-console.md](../screens/customer-console.md) §Policy Control |
| Audit Export | `/tenants/{tenantId}/audit-export` | [screens/customer-console.md](../screens/customer-console.md) §Audit Export |
| Model Cards | `/tenants/{tenantId}/instances/{instanceId}/model-card` | [screens/customer-console.md](../screens/customer-console.md) §Model Cards |
| Cost & Usage | `/tenants/{tenantId}/billing` | [screens/customer-console.md](../screens/customer-console.md) §Cost & Usage |
| Fleet Overview | `/fleet` | [screens/internal-operator-console.md](../screens/internal-operator-console.md) §Fleet Overview |
| Drift & Compliance | `/fleet/drift` | [screens/internal-operator-console.md](../screens/internal-operator-console.md) §Drift & Compliance |
| Ring Rollout Control | `/fleet/rollout` | [screens/internal-operator-console.md](../screens/internal-operator-console.md) §Ring Rollout Control |
| Agent Review Board | `/review-board` | [screens/internal-operator-console.md](../screens/internal-operator-console.md) §Agent Review Board Workspace |
| Incident Dashboard | `/incidents` | [screens/internal-operator-console.md](../screens/internal-operator-console.md) §Incident Dashboard |
| Cross-tenant Cost & Margin | `/fleet/economics` | [screens/internal-operator-console.md](../screens/internal-operator-console.md) §Cross-tenant Cost & Margin |
| Teams adaptive card (both states) | N/A — Bot Framework activity | [screens/teams-card.md](../screens/teams-card.md) |

## Token consumption

- Import `tokens/base.tokens.json` as the shared primitive layer; never reference a raw hex value in component code — every color, spacing, radius, shadow, and duration value used anywhere in the Console must resolve through a token reference.
- The build produces two themed bundles from `tokens/customer.tokens.json` and `tokens/internal-operator.tokens.json` respectively (Doc 59 ADR-16's "two builds, shared components") — components consume theme values via CSS custom properties (or the equivalent in whatever styling approach is chosen), never via a hardcoded theme name check in component logic (`if (theme === 'internal')`) — that pattern is exactly what a shared-component, build-time-themed system exists to avoid.

## Accessibility acceptance criteria (apply to every component/screen above)

1. Automated axe-core (or equivalent) pass with zero violations at the `WCAG2AA` ruleset, in CI, per Doc 56 §1.2.
2. Every interactive element reachable and operable by keyboard alone, with a visible focus indicator (`border.focus` token) — verified manually for the Escalation Review screen specifically, since it is the highest-stakes keyboard-first surface.
3. Every color pair used for text-on-background has been verified against the `$ratio` annotations already present in the token files — do not introduce a new color combination without adding its own verified ratio to the token file first.
