import { describe, expect, it } from "vitest";
import {
  markerGlyphFor, materialRows, minorRows, nextRowIndex,
  resolveState, sourceLinkAccessibleName, tableCaption,
  type EvidencePanelData,
} from "../src/logic/evidencePanel";

const DOC36_EDGE_CASE: EvidencePanelData = {
  comparisonType: "po_invoice_match",
  leftLabel: "Purchase Order PO-44120",
  rightLabel: "Invoice INV-4471",
  rows: [
    { field: "Quantity", left: { value: "1,000", unit: "units" }, right: { value: "600", unit: "units" }, discrepancy: "material", discrepancyNote: "600/1000 delivered" },
    { field: "Unit price", left: { value: "$4.20" }, right: { value: "$4.35" }, discrepancy: "material", discrepancyNote: "3.6% variance — outside the 2% auto-approve tolerance" },
    { field: "Delivery date", left: { value: "2026-03-01" }, right: { value: "2026-03-01" }, discrepancy: "none" },
    { field: "Currency", left: { value: "USD" }, right: { value: "USD" }, discrepancy: "none" },
  ],
  sourceRefs: [{ label: "View source", url: "https://blob/PO-44120.pdf" }],
};

describe("materialRows / minorRows", () => {
  it("reproduces Doc 36 §1.1's exact edge case as two material rows", () => {
    expect(materialRows(DOC36_EDGE_CASE)).toHaveLength(2);
    expect(minorRows(DOC36_EDGE_CASE)).toHaveLength(0);
  });
});

describe("markerGlyphFor", () => {
  it("never relies on color alone — material/minor/none each get a distinct glyph or none", () => {
    expect(markerGlyphFor("material")).toBe("▲");
    expect(markerGlyphFor("minor")).toBe("●");
    expect(markerGlyphFor("none")).toBeNull();
  });
});

describe("sourceLinkAccessibleName", () => {
  it("never renders bare 'View source' — always names the file", () => {
    expect(sourceLinkAccessibleName("PO-44120.pdf")).toBe("View source: PO-44120.pdf");
  });
});

describe("tableCaption", () => {
  it("builds the exact caption format from the spec", () => {
    expect(tableCaption(DOC36_EDGE_CASE)).toBe("Comparison: Purchase Order PO-44120 vs Invoice INV-4471");
  });
});

describe("nextRowIndex", () => {
  it("moves down/up and clamps at the table bounds (no wraparound)", () => {
    expect(nextRowIndex(0, "down", 4)).toBe(1);
    expect(nextRowIndex(3, "down", 4)).toBe(3); // clamped at last row
    expect(nextRowIndex(0, "up", 4)).toBe(0); // clamped at first row
  });
});

describe("resolveState", () => {
  it("prioritizes loading, then error, then empty, then ready", () => {
    expect(resolveState({ loading: true })).toBe("loading");
    expect(resolveState({ error: { message: "x" } })).toBe("error");
    expect(resolveState({ data: { ...DOC36_EDGE_CASE, rows: [] } })).toBe("empty");
    expect(resolveState({ data: DOC36_EDGE_CASE })).toBe("ready");
  });
});
