# Component: Fleet Coordinate Matrix

> Used on: Internal Operator Console — Fleet Overview screen
> Traces to: Doc 56 §4.2 ("tenants as rows, columns for platform version, blueprint versions, ring, drift status... any red cell immediately visible without opening a detail view"), Doc 55 §2.1 `FleetCoordinate`
> Theme: internal-operator only

## Purpose

Make fleet entropy (CTO Doc 01 risk R2) visible daily, at a glance, across every tenant — the screen's entire job is that a problem tenant is spottable in the first second of looking at the page, with detail available on demand but never required to see that something is wrong.

## Data shape (traces to Doc 55 §2.1 `FleetCoordinate`)

```typescript
interface FleetMatrixRow {
  tenantId: string;
  displayName: string;
  platformVersion: string;
  ring: "R0" | "R1" | "R2" | "R3";
  blueprints: {
    blueprintId: string;
    version: string;
    autonomy: "L0" | "L1" | "L2" | "L3" | "L4";
    health: "clean" | "watch" | "breach";
    healthReason?: string;         // e.g. "Eval currency: 34 days (SLO: 30)" — REQUIRED whenever health != "clean"
  }[];
  driftStatus: "clean" | "drifting" | "remediating";
  driftReason?: string;
  lastReconciledAt: string;        // ISO 8601 — Doc 55 §2.1 last_reconciled_at
}
```

**Why `healthReason` is required (not optional) whenever health is not clean:** Doc 56 §4.2 says a red cell must be "immediately visible" — visibility of the *problem* is only half the job; an operator seeing a red cell with no reason attached has to open a detail view anyway, which defeats the screen's purpose. The engineer implementing the Fleet Manager's API (Doc 55 §2) must never emit a non-clean health value without a reason string — flag this as a contract requirement in the Doc 53 §1 endpoint, not just a UI nicety.

## Anatomy

```
                    Platform    Ring    invoice-ap        support-triage     Drift        Last
Tenant              version             v4.2.0 · L2       v3.0.1 · L2        status       reconciled
──────────────────────────────────────────────────────────────────────────────────────────────────
contoso-prod        2.14.0      R2      🟢 clean           🟢 clean           🟢 clean     2 min ago
acme-industrial      2.14.0      R2      🟡 watch           🟢 clean           🟢 clean     2 min ago
                                          eval currency
                                          34d (SLO 30d)
northwind-health     2.13.2      R1      🔴 breach          —                 🔴 drifting  2 min ago
                                          false-action rate
                                          breach — demoted
                                          to L1 automatically
```

Rows are sorted with `breach` tenants first, then `watch`, then `clean` — the operator should never have to scan past healthy tenants to find the unhealthy ones. Within a health tier, sort alphabetically by `displayName`.

## States

| State | Visual treatment | Token reference |
|---|---|---|
| **Health: clean** | Green dot + "clean" label, no background tint on the cell | `health.clean` dot on `bg.surface` |
| **Health: watch** | Amber dot + label + the `healthReason`, rendered as a second line within the cell (not a tooltip — Doc 56 §4.2's "immediately visible" rules out anything requiring a hover) | `health.watch-bg` cell background, `health.watch` dot |
| **Health: breach** | Red dot + label + `healthReason`, same second-line pattern, PLUS the row itself gets a subtle full-row tint (not just the affected cell) so a breach is visible even in peripheral vision while scanning | `health.breach-bg` on both the cell and the row |
| **Drift: drifting** | The Drift status column shows amber/red per the same clean/drifting/remediating mapping; a `driftReason` appears identically to `healthReason` | `health.watch-bg` / `health.breach-bg` |
| **Drift: remediating** | A distinct blue "in progress" treatment (not amber, not red — this is a known, being-fixed state, and conflating it with an unaddressed breach would train operators to ignore real breaches) | `semantic.info-bg` |
| **Loading** | Skeleton rows | `bg.surface-sunken` |
| **Empty (no tenants match the current filter)** | "No tenants match this filter." with a one-click "clear filters" action | `text.secondary` |
| **Row hover** | Full-row background shift to `bg.surface-sunken`, cursor indicates the row is clickable (drills into tenant detail) | — |
| **Row focus (keyboard)** | Focus ring around the full row | `border.focus` |

## Breakpoints

This component is **wide-only** by design — it is a data-density tool for an operator at a desk, and Doc 56 §5.1 explicitly exempts the internal theme from the customer theme's mobile/tablet consideration. Below `breakpoint.wide`, the matrix switches to a horizontally-scrollable table (`overflow-x: auto` on its own container, per the artifact-design "wide content" rule) rather than reflowing into cards — reflowing would defeat the "scan many tenants at once" purpose entirely.

## Accessibility

- Semantic `<table>`; blueprint columns are dynamically generated `<th scope="col">` per the tenant's actual enabled agent set — the table's column count varies per deployment (a tenant with 3 agents has 3 blueprint columns; the table does not force a fixed column count across tenants with different agent counts — cells for a blueprint a given tenant doesn't run are omitted, not rendered empty, to avoid a wall of dashes).
- Health dots are always paired with a text label ("clean"/"watch"/"breach") — never color-only.
- The full-row breach tint (an addition beyond a plain WCAG requirement) specifically serves low-vision and colorblind operators scanning at speed — this is a case where a design choice exceeds the accessibility floor because the product's core value (spot the problem instantly) depends on it.
- Row is a single tab stop; `Enter` on a focused row opens tenant detail (matches the "row is clickable" hover affordance with a keyboard equivalent).

## Interaction note

Clicking/activating a row does not open a modal — it navigates to a tenant detail view (out of scope for this spec; Doc 56 §4.2 does not name a tenant-detail screen explicitly, and this is flagged in `handoff/design-log.md` as a gap the Software Engineer Agent should route back per Doc 60 §6's protocol rather than build ad hoc).
