/**
 * Pure logic for <ReasonChipPicker /> — no DOM/React here, so the
 * behaviors the handoff spec cares about most (positional numbering,
 * template auto-fill, free-text-vs-template tracking) are testable without
 * a rendering environment.
 *
 * Traces to: habagat-design/handoff/component-contracts.md
 * (ReasonChipPickerProps), habagat-design/components/reason-chip-picker.md
 * (full spec — data shape, keyboard behavior, interaction note).
 */

export type SystemReasonCode =
  | "low_confidence"
  | "out_of_policy"
  | "hard_rule_failed"
  | "tool_denied"
  | "budget_exhausted";

export interface SystemReasonChip {
  code: SystemReasonCode;
  label: string;
  template: string; // may contain {placeholders}
}

export interface LearnedReasonChip {
  id: string;
  label: string;
  template: string;
  usageCount: number;
  blueprintVersion: string;
}

export type AnyReasonChip =
  | ({ kind: "system" } & SystemReasonChip)
  | ({ kind: "learned" } & LearnedReasonChip);

export interface ReasonSelection {
  chipId: string | "free_text" | null;
  text: string;
}

/**
 * Builds the POSITIONAL numbered chip list: system chips first, then
 * learned chips ranked by usageCount descending (spec: "most-used chips
 * surface first among learned chips"), truncated to maxChipsShown.
 *
 * The numbering here is recomputed from this function's output every
 * time it's called — component-contracts.md is explicit that "this must
 * be recalculated live if learnedChips changes; do not hardcode the
 * numeral-to-chip mapping."
 */
export function buildNumberedChips(
  systemReasons: SystemReasonChip[],
  learnedChips: LearnedReasonChip[],
  maxChipsShown: number
): AnyReasonChip[] {
  const rankedLearned = [...learnedChips].sort((a, b) => b.usageCount - a.usageCount);
  const all: AnyReasonChip[] = [
    ...systemReasons.map((c) => ({ kind: "system" as const, ...c })),
    ...rankedLearned.map((c) => ({ kind: "learned" as const, ...c })),
  ];
  return all.slice(0, maxChipsShown);
}

function chipIdOf(chip: AnyReasonChip): string {
  return chip.kind === "system" ? chip.code : chip.id;
}

/** Maps a pressed numeral key (1-9) to the chip at that position, or
 * undefined if out of range — the "1-9 select the Nth chip shown" rule. */
export function chipForNumeralKey(chips: AnyReasonChip[], key: string): AnyReasonChip | undefined {
  const n = Number(key);
  if (!Number.isInteger(n) || n < 1 || n > chips.length) return undefined;
  return chips[n - 1];
}

/** Fills a template's {placeholder} tokens from an evidence-derived
 * values map (same Escalation.evidence shape the EvidencePanel consumes —
 * spec: "both components read from one data source without divergence"). */
export function fillTemplate(template: string, values: Record<string, string>): string {
  return template.replace(/\{(\w+)\}/g, (match, key) => (key in values ? values[key] : match));
}

/**
 * Selecting a chip auto-fills the text area (spec: "Auto-fills the text
 * area with the chip's template"). Re-selecting the SAME chip does NOT
 * clobber a since-edited text area (spec: "selecting the same chip again
 * does not clear a since-edited text area").
 */
export function selectChip(
  current: ReasonSelection,
  chip: AnyReasonChip,
  values: Record<string, string>
): ReasonSelection {
  const id = chipIdOf(chip);
  const filled = fillTemplate(chip.template, values);
  if (current.chipId === id && current.text !== filled) {
    // Same chip re-selected, and the text has since diverged from the
    // original fill — leave the reviewer's edit alone.
    return current;
  }
  return { chipId: id, text: filled };
}

/** Typing directly (without a chip selected) sets chipId to "free_text" —
 * tracked distinctly per the spec's flywheel-quality-signal rationale. */
export function editFreeText(text: string): ReasonSelection {
  return { chipId: "free_text", text };
}

export type ReasonProvenance = "unedited_template" | "edited_template" | "free_text";

/**
 * The required instrumentation point (component-contracts.md: "Track and
 * log whether the final submitted text is an unedited template, an
 * edited template, or pure free text").
 */
export function classifyReasonProvenance(
  selection: ReasonSelection,
  chips: AnyReasonChip[],
  values: Record<string, string>
): ReasonProvenance {
  if (selection.chipId === "free_text" || selection.chipId === null) return "free_text";
  const chip = chips.find((c) => chipIdOf(c) === selection.chipId);
  if (!chip) return "free_text";
  const filled = fillTemplate(chip.template, values);
  return selection.text === filled ? "unedited_template" : "edited_template";
}

export function accessibleChipName(chip: AnyReasonChip, index: number, total: number): string {
  return `Reason option ${index + 1} of ${total}: ${chip.label}`;
}
