import React, { useMemo, useState } from "react";
import {
  AnyReasonChip, LearnedReasonChip, ReasonSelection, SystemReasonChip,
  accessibleChipName, buildNumberedChips, classifyReasonProvenance,
  editFreeText, selectChip,
} from "../logic/reasonChipPicker";

export interface ReasonChipPickerProps {
  systemReasons: SystemReasonChip[];
  learnedChips: LearnedReasonChip[];
  maxChipsShown: number;
  value: ReasonSelection;
  onChange: (selection: ReasonSelection) => void;
  submitAttempted: boolean;
  /** Escalation.evidence-derived values used to fill {placeholders} —
   * see component-contracts.md: "both components read from one data
   * source without divergence" (shared with EvidencePanel's data). */
  evidenceValues: Record<string, string>;
  /** Required instrumentation point (component-contracts.md): logs
   * whether the submitted reason was an unedited template, edited
   * template, or free text, for the eval-corpus flywheel quality signal. */
  onProvenanceLogged?: (provenance: ReturnType<typeof classifyReasonProvenance>) => void;
}

export function ReasonChipPicker({
  systemReasons, learnedChips, maxChipsShown, value, onChange,
  submitAttempted, evidenceValues, onProvenanceLogged,
}: ReasonChipPickerProps): JSX.Element {
  const chips = useMemo(
    () => buildNumberedChips(systemReasons, learnedChips, maxChipsShown),
    [systemReasons, learnedChips, maxChipsShown]
  );

  const handleSelect = (chip: AnyReasonChip) => {
    const next = selectChip(value, chip, evidenceValues);
    onChange(next);
    onProvenanceLogged?.(classifyReasonProvenance(next, chips, evidenceValues));
  };

  const handleTextChange = (text: string) => {
    const next = editFreeText(text);
    onChange(next);
  };

  const showError = submitAttempted && value.text.trim().length === 0;

  return (
    <div className="reason-chip-picker">
      <label htmlFor="reason-text-area" id="reason-label">
        Reason for your decision (required)
      </label>
      <div role="radiogroup" aria-labelledby="reason-label">
        {chips.map((chip, i) => {
          const id = chip.kind === "system" ? chip.code : chip.id;
          const selected = value.chipId === id;
          return (
            <button
              key={id}
              type="button"
              role="radio"
              aria-checked={selected}
              aria-label={accessibleChipName(chip, i, chips.length)}
              onClick={() => handleSelect(chip)}
              className={selected ? "chip chip--selected" : "chip"}
            >
              <span aria-hidden="true">{i + 1}</span> {chip.label}
            </button>
          );
        })}
      </div>
      <textarea
        id="reason-text-area"
        value={value.text}
        onChange={(e) => handleTextChange(e.target.value)}
        aria-describedby={showError ? "reason-error" : undefined}
        aria-invalid={showError}
      />
      {showError && (
        <p id="reason-error" style={{ color: "var(--semantic-danger-text)" }}>
          A reason is required before you can approve/reject/modify.
        </p>
      )}
    </div>
  );
}
