import { describe, expect, it } from "vitest";
import {
  buildNumberedChips, chipForNumeralKey, classifyReasonProvenance,
  editFreeText, fillTemplate, selectChip,
  type LearnedReasonChip, type SystemReasonChip,
} from "../src/logic/reasonChipPicker";

const SYSTEM: SystemReasonChip[] = [
  { code: "low_confidence", label: "Low confidence", template: "The agent was not confident enough." },
];

const LEARNED: LearnedReasonChip[] = [
  { id: "l1", label: "Rare case", template: "Rare: {qty}", usageCount: 1, blueprintVersion: "4.2.0" },
  { id: "l2", label: "Common case", template: "Common: {qty}/{ordered} at ${price}", usageCount: 50, blueprintVersion: "4.2.0" },
];

describe("buildNumberedChips", () => {
  it("puts system chips first, then learned chips ranked by usageCount descending", () => {
    const chips = buildNumberedChips(SYSTEM, LEARNED, 9);
    expect(chips.map((c) => c.label)).toEqual(["Low confidence", "Common case", "Rare case"]);
  });

  it("truncates to maxChipsShown", () => {
    const chips = buildNumberedChips(SYSTEM, LEARNED, 2);
    expect(chips).toHaveLength(2);
  });
});

describe("chipForNumeralKey", () => {
  it("maps numeral 1-9 positionally, out-of-range returns undefined", () => {
    const chips = buildNumberedChips(SYSTEM, LEARNED, 9);
    expect(chipForNumeralKey(chips, "1")?.label).toBe("Low confidence");
    expect(chipForNumeralKey(chips, "2")?.label).toBe("Common case");
    expect(chipForNumeralKey(chips, "9")).toBeUndefined();
    expect(chipForNumeralKey(chips, "0")).toBeUndefined();
  });
});

describe("fillTemplate", () => {
  it("fills placeholders from the evidence values map", () => {
    expect(fillTemplate("Common: {qty}/{ordered} at ${price}", { qty: "600", ordered: "1000", price: "4.35" }))
      .toBe("Common: 600/1000 at $4.35");
  });

  it("leaves an unresolved placeholder untouched rather than crashing", () => {
    expect(fillTemplate("{missing}", {})).toBe("{missing}");
  });
});

describe("selectChip / editFreeText", () => {
  const chips = buildNumberedChips(SYSTEM, LEARNED, 9);
  const values = { qty: "600", ordered: "1000", price: "4.35" };

  it("auto-fills the text area from the chip's template", () => {
    const selection = selectChip({ chipId: null, text: "" }, chips[1], values);
    expect(selection.chipId).toBe("l2");
    expect(selection.text).toBe("Common: 600/1000 at $4.35");
  });

  it("re-selecting the SAME chip does not clobber a since-edited text area", () => {
    const filled = selectChip({ chipId: null, text: "" }, chips[1], values);
    const edited = { ...filled, text: "Common: 600/1000 at $4.35 — approved with vendor confirmation." };
    const reselected = selectChip(edited, chips[1], values);
    expect(reselected).toEqual(edited); // unchanged
  });

  it("typing directly sets chipId to free_text", () => {
    const selection = editFreeText("A totally novel situation.");
    expect(selection.chipId).toBe("free_text");
  });
});

describe("classifyReasonProvenance", () => {
  const chips = buildNumberedChips(SYSTEM, LEARNED, 9);
  const values = { qty: "600", ordered: "1000", price: "4.35" };

  it("classifies an untouched chip fill as unedited_template", () => {
    const selection = selectChip({ chipId: null, text: "" }, chips[1], values);
    expect(classifyReasonProvenance(selection, chips, values)).toBe("unedited_template");
  });

  it("classifies an edited chip fill as edited_template", () => {
    const selection = { chipId: "l2", text: "Common: 600/1000 at $4.35, escalating to vendor manager." };
    expect(classifyReasonProvenance(selection, chips, values)).toBe("edited_template");
  });

  it("classifies free text as free_text", () => {
    const selection = editFreeText("Something the chips don't cover.");
    expect(classifyReasonProvenance(selection, chips, values)).toBe("free_text");
  });
});
