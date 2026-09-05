import React, { useState } from "react";
import {
  EvidencePanelData, markerGlyphFor, materialRows, nextRowIndex,
  resolveState, sourceLinkAccessibleName, tableCaption,
} from "../logic/evidencePanel";

export interface EvidencePanelProps {
  data: EvidencePanelData;
  loading?: boolean;
  error?: { message: string };
}

/**
 * <EvidencePanel /> — habagat-design/components/evidence-panel.md.
 * Customer-theme only component; consumes theme values via CSS custom
 * properties (Doc 59 ADR-16 / component-contracts.md's token-consumption
 * rule) — every color/spacing/radius token below is a `var(--token-name)`
 * reference, never a hardcoded hex value.
 */
export function EvidencePanel({ data, loading, error }: EvidencePanelProps): JSX.Element {
  const [focusedRow, setFocusedRow] = useState(0);
  const state = resolveState({ loading, error, data });

  if (state === "loading") {
    return (
      <div aria-busy="true" className="evidence-panel evidence-panel--loading">
        {[0, 1, 2].map((i) => (
          <div key={i} className="evidence-panel__skeleton-row" style={{ background: "var(--bg-surface-sunken)" }} />
        ))}
      </div>
    );
  }

  if (state === "error") {
    return (
      <div role="status" className="evidence-panel evidence-panel--error" style={{ background: "var(--semantic-danger-bg)" }}>
        <p>
          We couldn&apos;t load the full comparison. The recommendation and confidence above are
          still accurate — view source documents directly if you need the detail.
        </p>
        <SourceRefs refs={data.sourceRefs} />
      </div>
    );
  }

  if (state === "empty") {
    return (
      <div className="evidence-panel evidence-panel--empty">
        <p style={{ color: "var(--text-secondary)" }}>No comparable records were found for this case.</p>
        <SourceRefs refs={data.sourceRefs} />
      </div>
    );
  }

  const notes = materialRows(data).filter((r) => r.discrepancyNote);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      setFocusedRow((i) => nextRowIndex(i, "down", data.rows.length));
      e.preventDefault();
    } else if (e.key === "ArrowUp") {
      setFocusedRow((i) => nextRowIndex(i, "up", data.rows.length));
      e.preventDefault();
    }
  };

  return (
    <div className="evidence-panel">
      <table onKeyDown={handleKeyDown} tabIndex={0}>
        <caption className="visually-hidden">{tableCaption(data)}</caption>
        <thead>
          <tr>
            <th scope="col"></th>
            <th scope="col">{data.leftLabel}</th>
            <th scope="col">{data.rightLabel}</th>
          </tr>
        </thead>
        <tbody>
          {data.rows.map((row, i) => {
            const glyph = markerGlyphFor(row.discrepancy);
            const isMaterial = row.discrepancy === "material";
            return (
              <tr key={row.field} aria-current={i === focusedRow ? "true" : undefined}>
                <th scope="row">{row.field}</th>
                <td style={isMaterial ? { background: "var(--diff-removed-bg)" } : undefined}>
                  {row.left.value} {row.left.unit ?? ""}
                </td>
                <td style={isMaterial ? { background: "var(--diff-added-bg)" } : undefined}>
                  {row.right.value} {row.right.unit ?? ""} {glyph && <span aria-hidden="true">{glyph}</span>}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      {notes.map((row) => (
        <p key={row.field} role="status" style={{ color: "var(--semantic-warning-text)" }}>
          ⓘ {row.discrepancyNote}
        </p>
      ))}
      <SourceRefs refs={data.sourceRefs} />
    </div>
  );
}

function SourceRefs({ refs }: { refs: EvidencePanelData["sourceRefs"] }): JSX.Element {
  return (
    <div className="evidence-panel__sources">
      {refs.map((ref) => {
        const filename = ref.url.split("/").pop() ?? ref.url;
        return (
          <a key={ref.url} href={ref.url}>
            📄 {sourceLinkAccessibleName(filename)}
          </a>
        );
      })}
    </div>
  );
}
