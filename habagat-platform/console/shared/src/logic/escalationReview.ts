/**
 * Pure logic for the Escalation Review screen
 * (habagat-design/screens/escalation-review.md) — the parts of the screen
 * that are decision rules rather than markup, so they're unit-testable.
 */

export type EscalationReason = "low_confidence" | "hard_rule_failed" | "out_of_policy" | "budget_exhausted";

/** Doc 56 §2.2 / spec: the "uncertain" block is shown only for
 * low_confidence and hard_rule_failed; omitted (not shown empty) for
 * out_of_policy and budget_exhausted, "where there's nothing the agent
 * is uncertain about — it hit a hard boundary, not a confidence gap." */
export function shouldShowUncertainBlock(reason: EscalationReason): boolean {
  return reason === "low_confidence" || reason === "hard_rule_failed";
}

export interface ActionsGateState {
  evidencePanelScrolledIntoView: boolean;
  dwellSeconds: number;
}

const MIN_DWELL_SECONDS = 4; // spec's "provisional 4 seconds"

/** Doc 56 §2.5's soft nudge: Approve/Modify/Reject are aria-disabled
 * (not `disabled`, so screen readers can announce why) until EITHER the
 * evidence panel has been scrolled into view OR the dwell time elapses. */
export function actionsAreEnabled(state: ActionsGateState): boolean {
  return state.evidencePanelScrolledIntoView || state.dwellSeconds >= MIN_DWELL_SECONDS;
}

export function disabledActionAriaLabel(action: "Approve" | "Modify" | "Reject"): string {
  return `${action}, unavailable until you've reviewed the evidence below`;
}

export type ActionKind = "approve" | "modify" | "reject";

/** Doc 56 §2.4's keyboard shortcut table, as a pure key->action mapping
 * (the overlay's own display content is markup, not logic). */
export function actionForKey(key: string): ActionKind | "show_shortcuts" | "next" | "previous" | undefined {
  switch (key) {
    case "a":
    case "A":
      return "approve";
    case "m":
    case "M":
      return "modify";
    case "r":
    case "R":
      return "reject";
    case "?":
      return "show_shortcuts";
    case "j":
    case "J":
      return "next";
    case "k":
    case "K":
      return "previous";
    default:
      return undefined;
  }
}

export function headerCopy(subjectLine: string | null, blueprintDisplayName: string): string {
  // Spec: always exactly one sentence; never a blank header. Fallback per
  // spec's exact wording when no specific subject line is available.
  if (subjectLine && subjectLine.trim().length > 0) {
    return `${subjectLine} needs your call.`;
  }
  return `This ${blueprintDisplayName} run needs your review.`;
}

export function confidenceCopy(confidencePct: number, thresholdPct: number): string {
  // Spec: confidence always compared explicitly against the threshold,
  // never a bare number with no reference point.
  const comparator = confidencePct < thresholdPct ? "Below" : "At or above";
  return `${comparator} the ${thresholdPct}% threshold for this blueprint`;
}
