/**
 * Pure logic for <EvidencePanel /> — the row-classification and
 * navigation rules from habagat-design/components/evidence-panel.md,
 * kept separate from rendering so the "material vs minor vs none" and
 * keyboard-row-navigation behaviors are unit-testable without a DOM.
 */

export type Discrepancy = "none" | "minor" | "material";

export interface EvidenceRowValue {
  value: string;
  unit?: string;
}

export interface EvidenceRow {
  field: string;
  left: EvidenceRowValue;
  right: EvidenceRowValue;
  discrepancy: Discrepancy;
  discrepancyNote?: string;
}

export interface EvidencePanelData {
  comparisonType: string;
  leftLabel: string;
  rightLabel: string;
  rows: EvidenceRow[];
  sourceRefs: { label: string; url: string }[];
}

/** Only `material` rows get the strong visual treatment and a rendered
 * discrepancyNote callout — spec: "Only material rows get the strong
 * visual treatment; minor gets a quieter marker; none gets no marker." */
export function materialRows(data: EvidencePanelData): EvidenceRow[] {
  return data.rows.filter((r) => r.discrepancy === "material");
}

export function minorRows(data: EvidencePanelData): EvidenceRow[] {
  return data.rows.filter((r) => r.discrepancy === "minor");
}

/** The marker glyph — never color alone (WCAG 1.4.1, per spec's
 * accessibility section: "color reinforces but is never the only signal"). */
export function markerGlyphFor(discrepancy: Discrepancy): string | null {
  switch (discrepancy) {
    case "material":
      return "▲";
    case "minor":
      return "●";
    case "none":
      return null;
  }
}

export function sourceLinkAccessibleName(filename: string): string {
  // Spec: accessible names of the form "View source: {filename}", never
  // bare "View source" repeated.
  return `View source: ${filename}`;
}

export function tableCaption(data: EvidencePanelData): string {
  return `Comparison: ${data.leftLabel} vs ${data.rightLabel}`;
}

/** ↓/↑ row navigation while focus is inside the table — clamps at the
 * table's bounds rather than wrapping (spec doesn't call for wraparound). */
export function nextRowIndex(currentIndex: number, direction: "down" | "up", rowCount: number): number {
  if (rowCount === 0) return -1;
  const next = direction === "down" ? currentIndex + 1 : currentIndex - 1;
  return Math.max(0, Math.min(rowCount - 1, next));
}

export type EvidencePanelState = "loading" | "empty" | "error" | "ready";

export function resolveState(opts: {
  loading?: boolean;
  error?: { message: string };
  data?: EvidencePanelData;
}): EvidencePanelState {
  if (opts.loading) return "loading";
  if (opts.error) return "error";
  if (!opts.data || opts.data.rows.length === 0) return "empty";
  return "ready";
}
