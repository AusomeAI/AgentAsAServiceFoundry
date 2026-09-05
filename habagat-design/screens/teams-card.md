# Screen: Teams Adaptive Card (Escalation Decision)

> Traces to: Doc 56 §3 (all subsections), Doc 53 §2.3 (the decision contract this card calls), Doc 52 §1.2 `Escalation`
> Designed against **Adaptive Card schema v1.5** layout primitives (Container, ColumnSet, FactSet, ActionSet, Action.Submit, Action.ShowCard) — not a freeform mockup. Every element below maps to an actual Adaptive Card element type so the Software Engineer Agent's bot implementation (Doc 56 §3.3) can render this without redesign.

## State 1: Initial card (posted when the escalation is created)

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "Container",
      "style": "warning",
      "items": [
        {
          "type": "TextBlock",
          "text": "🔶 Needs your decision",
          "weight": "Bolder",
          "size": "Medium"
        }
      ]
    },
    {
      "type": "TextBlock",
      "text": "Invoice INV-4471 — quantity/price variance on partial delivery",
      "wrap": true,
      "weight": "Bolder"
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Agent recommends:", "value": "Escalate" },
        { "title": "Confidence:", "value": "71% (below 90% threshold)" }
      ]
    },
    {
      "type": "ColumnSet",
      "columns": [
        {
          "type": "Column", "width": "stretch",
          "items": [
            { "type": "TextBlock", "text": "PO-44120", "weight": "Bolder", "size": "Small" },
            { "type": "TextBlock", "text": "1,000 @ $4.20", "wrap": true }
          ]
        },
        {
          "type": "Column", "width": "stretch",
          "items": [
            { "type": "TextBlock", "text": "INV-4471", "weight": "Bolder", "size": "Small" },
            { "type": "TextBlock", "text": "600 @ $4.35", "wrap": true, "color": "Attention" }
          ]
        }
      ]
    }
  ],
  "actions": [
    { "type": "Action.ShowCard", "title": "Approve",
      "card": { "type": "AdaptiveCard", "body": [
        { "type": "TextBlock", "text": "Reason (required)", "weight": "Bolder" },
        { "type": "Input.ChoiceSet", "id": "reasonChip", "style": "expanded",
          "choices": [
            { "title": "1. Low confidence", "value": "low_confidence" },
            { "title": "2. Partial delivery, price changed mid-shipment", "value": "chip_learned_1" },
            { "title": "3. Other (opens Console)", "value": "other" }
          ] }
      ], "actions": [
        { "type": "Action.Submit", "title": "Confirm approve",
          "data": { "decision": "approve", "escalationId": "esc_9182" } }
      ] } },
    { "type": "Action.ShowCard", "title": "Reject",
      "card": { "type": "AdaptiveCard", "body": [
        { "type": "TextBlock", "text": "Reason (required)", "weight": "Bolder" },
        { "type": "Input.ChoiceSet", "id": "reasonChip", "style": "expanded",
          "choices": [
            { "title": "1. Duplicate suspected", "value": "chip_learned_2" },
            { "title": "2. Wrong PO reference", "value": "chip_learned_3" },
            { "title": "3. Other (opens Console)", "value": "other" }
          ] }
      ], "actions": [
        { "type": "Action.Submit", "title": "Confirm reject",
          "data": { "decision": "reject", "escalationId": "esc_9182" } }
      ] } },
    { "type": "Action.OpenUrl", "title": "Modify in Console",
      "url": "https://console.habagat.dev/tenants/contoso-prod/escalations/esc_9182?source=teams" }
  ]
}
```

**Design notes, mapped to Doc 56 §3.2's constraints:**

- **`Action.ShowCard` for Approve/Reject** (not `Action.Submit` directly) — this is what implements "a condensed reason-chip picker (top 3 chips only)... inline in the card's follow-up prompt" (Doc 56 §3.2). Adaptive Cards' `ShowCard` action is the correct native primitive for "reveal a small follow-up form without leaving the card" — using `Action.Submit` directly would either skip reason capture (violating the mandatory-reason rule, Doc 53 §2.3) or require a second round-trip card update, which `ShowCard` avoids.
- **Top 3 chips only, with "Other" always the third/last option** deep-linking to the Console — this is the literal card-level implementation of Doc 56 §3.2's fast-path/full-path split. The chip choices differ per action (Approve's chips vs. Reject's chips) because the plausible reasons for each differ, matching the reason-chip-picker component's semantics even in this condensed form.
- **`Action.OpenUrl` for Modify** (never `ShowCard` or an in-card form) — Doc 56 §3.2 is explicit that Modify never attempts inline structured editing in the card; this is a hard constraint reflected directly in the action type chosen, not just a stated intention.
- **The PO/invoice comparison uses a two-column `ColumnSet` with `FactSet`-adjacent styling**, not the full Evidence Panel table — Adaptive Cards render inside a chat pane at a few hundred pixels wide; this is the compact subset explicitly scoped in Doc 56 §3.2 ("enough of the evidence panel... to make the *common* decision"), showing only the single most material discrepancy row, with the full multi-row comparison reserved for the Console.
- **`color: "Attention"` on the invoice-side price** is the Adaptive Card schema's built-in semantic color token for drawing attention to a value — the card-native equivalent of the web Evidence Panel's `diff.added-bg` treatment, using the platform's own semantic vocabulary rather than trying to inject custom hex values into a card (which degrades unpredictably across Teams clients).

## State 2: Post-decision card (in-place update after a decision is submitted)

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "Container",
      "style": "good",
      "items": [
        { "type": "TextBlock", "text": "✅ Approved by Priya at 14:32", "weight": "Bolder" }
      ]
    },
    {
      "type": "TextBlock",
      "text": "Invoice INV-4471 — \"Approved as recommended; confidence was low but the variance is within our normal supplier-timing pattern.\"",
      "wrap": true, "isSubtle": true
    }
  ],
  "actions": [
    { "type": "Action.OpenUrl", "title": "View in Console",
      "url": "https://console.habagat.dev/tenants/contoso-prod/escalations/esc_9182" }
  ]
}
```

**Design notes:**
- The card is **updated in place** (Bot Framework's `updateActivity`), not replaced with a new message — this matches Doc 56 §3.3's bot architecture, where the bot "translates the API response back into a card update," and avoids cluttering the channel with a duplicate message per decision.
- The `Container style="good"` (approved) / `style="attention"` (rejected) uses, again, Adaptive Cards' own semantic style vocabulary rather than custom color injection.
- **The `isSubtle` text block must be populated with the actual submitted `decision_reason` value for that specific escalation** — sourced from the same API response the bot receives when it posts the decision (Doc 56 §3.3's sequence diagram), never static or templated text. The example above shows realistic free-text content precisely so the Software Engineer Agent implements a live field binding here, not a hardcoded string. This closes the loop for the reviewer and for anyone else in a shared Teams channel who sees the card, so the decision's rationale is visible without requiring a Console visit for the common case.

## Accessibility (Adaptive Cards' own accessibility model)

- Every `TextBlock` carrying meaning (not purely decorative) has no `isSubtle: true` unless it is genuinely secondary information — subtle text has reduced contrast in Teams' rendering and should not carry the primary decision-relevant facts (the recommendation, the confidence, the comparison values are all full-contrast; only the post-decision timestamp detail is subtle).
- `Action.ShowCard` and `Action.Submit` buttons get accessible titles that state the action outcome, not just a verb — "Confirm approve" rather than a bare "Submit," since Teams' screen-reader integration announces the action title directly.
- The card never relies on color alone to convey the recommendation or the discrepancy — the `Attention` color on the invoice-side value is paired with the numeric values themselves being different, which is inherently perceivable without color.

## What this design does NOT attempt (explicit scope boundary, per Doc 56 §3.2)

- No inline field editing for Modify — confirmed above.
- No multi-row evidence table — only the single most material comparison surfaces; the full Evidence Panel is Console-only.
- No keyboard-shortcut system inside Teams — Teams' own card interaction model (click/tap the action buttons) is used as-is; the Console's keyboard-first design (Doc 56 §2.4) is not replicated here because Adaptive Cards do not support custom key-binding, and attempting to fake it would create an inconsistent, half-working experience worse than not having it.
