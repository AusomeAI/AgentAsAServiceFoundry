import { describe, expect, it } from "vitest";
import {
  actionForKey, actionsAreEnabled, confidenceCopy,
  disabledActionAriaLabel, headerCopy, shouldShowUncertainBlock,
} from "../src/logic/escalationReview";

describe("shouldShowUncertainBlock", () => {
  it("shows for low_confidence and hard_rule_failed", () => {
    expect(shouldShowUncertainBlock("low_confidence")).toBe(true);
    expect(shouldShowUncertainBlock("hard_rule_failed")).toBe(true);
  });

  it("omits for out_of_policy and budget_exhausted (a hard boundary, not a confidence gap)", () => {
    expect(shouldShowUncertainBlock("out_of_policy")).toBe(false);
    expect(shouldShowUncertainBlock("budget_exhausted")).toBe(false);
  });
});

describe("actionsAreEnabled", () => {
  it("is disabled before scroll-into-view and before the dwell time", () => {
    expect(actionsAreEnabled({ evidencePanelScrolledIntoView: false, dwellSeconds: 1 })).toBe(false);
  });

  it("is enabled once scrolled into view, even before dwell elapses", () => {
    expect(actionsAreEnabled({ evidencePanelScrolledIntoView: true, dwellSeconds: 0 })).toBe(true);
  });

  it("is enabled once the 4-second dwell elapses, even without scroll", () => {
    expect(actionsAreEnabled({ evidencePanelScrolledIntoView: false, dwellSeconds: 4 })).toBe(true);
  });
});

describe("disabledActionAriaLabel", () => {
  it("announces WHY, not just that it's disabled (aria-disabled, not disabled attribute)", () => {
    expect(disabledActionAriaLabel("Approve")).toBe("Approve, unavailable until you've reviewed the evidence below");
  });
});

describe("actionForKey", () => {
  it("maps the full Doc 56 §2.4 shortcut table", () => {
    expect(actionForKey("a")).toBe("approve");
    expect(actionForKey("M")).toBe("modify");
    expect(actionForKey("r")).toBe("reject");
    expect(actionForKey("?")).toBe("show_shortcuts");
    expect(actionForKey("j")).toBe("next");
    expect(actionForKey("K")).toBe("previous");
    expect(actionForKey("z")).toBeUndefined();
  });
});

describe("headerCopy", () => {
  it("uses the specific subject line when present", () => {
    expect(headerCopy("Invoice INV-4471 — quantity and price variance", "invoice-ap"))
      .toBe("Invoice INV-4471 — quantity and price variance needs your call.");
  });

  it("falls back to the exact spec wording — never a blank header", () => {
    expect(headerCopy(null, "invoice-ap")).toBe("This invoice-ap run needs your review.");
    expect(headerCopy("   ", "invoice-ap")).toBe("This invoice-ap run needs your review.");
  });
});

describe("confidenceCopy", () => {
  it("always states the comparison against the threshold, never a bare number", () => {
    expect(confidenceCopy(71, 90)).toBe("Below the 90% threshold for this blueprint");
    expect(confidenceCopy(95, 90)).toBe("At or above the 90% threshold for this blueprint");
  });
});
