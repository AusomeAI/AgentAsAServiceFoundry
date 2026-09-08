import React, { useEffect, useState } from "react";
import { EvidencePanel, EvidencePanelData } from "@habagat/console-shared";
import { ReasonChipPicker } from "@habagat/console-shared";
import {
  LearnedReasonChip, ReasonSelection, SystemReasonChip,
} from "@habagat/console-shared";
import {
  actionForKey, actionsAreEnabled, confidenceCopy, disabledActionAriaLabel,
  EscalationReason, headerCopy, shouldShowUncertainBlock,
} from "@habagat/console-shared";

/**
 * Route: /tenants/{tenantId}/escalations/{escalationId}
 * habagat-design/screens/escalation-review.md — "the most important
 * screen in the product." Literal render of HEADER -> RECOMMEND ->
 * EVIDENCE -> UNCERTAIN -> ACTIONS -> REASON, no reordering, no added
 * sections, per the spec's own instruction.
 */
export interface EscalationReviewProps {
  subjectLine: string | null;
  blueprintDisplayName: string;
  recommendation: "escalate";
  confidencePct: number;
  thresholdPct: number;
  recommendationRationale: string;
  reason: EscalationReason;
  uncertaintyNote?: string;
  evidence: EvidencePanelData;
  systemReasons: SystemReasonChip[];
  learnedChips: LearnedReasonChip[];
  evidenceValues: Record<string, string>;
  alreadyDecided?: { decision: "approved" | "rejected"; by: string; at: string };
  onDecision: (action: "approve" | "modify" | "reject", reason: ReasonSelection) => void;
  onNext: () => void;
  onPrevious: () => void;
}

export function EscalationReview(props: EscalationReviewProps): JSX.Element {
  const [reasonSelection, setReasonSelection] = useState<ReasonSelection>({ chipId: null, text: "" });
  const [submitAttempted, setSubmitAttempted] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [gateState] = useState({ evidencePanelScrolledIntoView: false, dwellSeconds: 0 });
  const [dwellSeconds, setDwellSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setDwellSeconds((s) => s + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  const enabled = actionsAreEnabled({ ...gateState, dwellSeconds });

  const submit = (action: "approve" | "modify" | "reject") => {
    setSubmitAttempted(true);
    if (reasonSelection.text.trim().length === 0) return; // spec: blocks submission on empty reason
    props.onDecision(action, reasonSelection);
  };

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const action = actionForKey(e.key);
      if (action === "approve" || action === "modify" || action === "reject") {
        if (enabled) submit(action);
      } else if (action === "show_shortcuts") {
        setShowShortcuts(true);
      } else if (action === "next") {
        props.onNext();
      } else if (action === "previous") {
        props.onPrevious();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled, reasonSelection]);

  if (props.alreadyDecided) {
    return (
      <div className="escalation-review escalation-review--already-decided">
        <p>
          This was already {props.alreadyDecided.decision} by {props.alreadyDecided.by} at{" "}
          {props.alreadyDecided.at}.
        </p>
        <a href="../escalations">Back to queue</a>
      </div>
    );
  }

  return (
    <div className="escalation-review">
      {/* HEADER */}
      <h1>{headerCopy(props.subjectLine, props.blueprintDisplayName)}</h1>

      {/* RECOMMEND */}
      <div className="escalation-review__recommend" style={{ background: "var(--bg-surface-sunken)" }}>
        <span aria-hidden="true">🤖</span> Agent recommends: Escalate — Confidence {props.confidencePct}%
        <p>
          {confidenceCopy(props.confidencePct, props.thresholdPct)} — {props.recommendationRationale}
        </p>
      </div>

      {/* EVIDENCE */}
      <EvidencePanel data={props.evidence} />

      {/* UNCERTAIN — conditionally omitted, never shown empty */}
      {shouldShowUncertainBlock(props.reason) && props.uncertaintyNote && (
        <div className="escalation-review__uncertain">
          ⚠ What the agent is uncertain about
          <p>{props.uncertaintyNote}</p>
        </div>
      )}

      {/* ACTIONS */}
      <div className="escalation-review__actions">
        {(["approve", "modify", "reject"] as const).map((action) => (
          <button
            key={action}
            type="button"
            aria-disabled={!enabled}
            aria-label={!enabled ? disabledActionAriaLabel(capitalize(action)) : undefined}
            onClick={() => enabled && submit(action)}
          >
            {capitalize(action)} <span aria-hidden="true">{action[0].toUpperCase()}</span>
          </button>
        ))}
      </div>

      {/* REASON */}
      <ReasonChipPicker
        systemReasons={props.systemReasons}
        learnedChips={props.learnedChips}
        maxChipsShown={9}
        value={reasonSelection}
        onChange={setReasonSelection}
        submitAttempted={submitAttempted}
        evidenceValues={props.evidenceValues}
      />

      {showShortcuts && (
        <div role="dialog" aria-modal="true" aria-label="Keyboard shortcuts">
          <button onClick={() => setShowShortcuts(false)} aria-label="Close">
            Esc
          </button>
          <ul>
            <li>A — Approve</li>
            <li>M — Open Modify</li>
            <li>R — Reject</li>
            <li>1–9 — Select reason chip</li>
            <li>Enter — Confirm current action</li>
            <li>J / K — Next / previous</li>
            <li>? — Show this list</li>
          </ul>
        </div>
      )}
    </div>
  );
}

type Capitalized<S extends string> = S extends `${infer First}${infer Rest}`
  ? `${Uppercase<First>}${Rest}`
  : S;

function capitalize<T extends string>(s: T): Capitalized<T> {
  return (s[0].toUpperCase() + s.slice(1)) as Capitalized<T>;
}
