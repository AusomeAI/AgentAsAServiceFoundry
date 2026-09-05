# Handoff: Accessibility Contrast Matrix

> Every color pair referenced with a `$ratio` annotation in the token files, listed here as a single verifiable table. Traces to Doc 56 §1.2's WCAG 2.1 AA commitment (4.5:1 minimum for body text, 3:1 for large text ≥18pt/14pt-bold and UI component boundaries).

## Customer theme

| Pair | Light | Dark | Requirement | Status |
|---|---|---|---|---|
| `text.primary` on `bg.surface` | 15.1:1 | 14.8:1 | 4.5:1 | ✅ |
| `text.secondary` on `bg.surface` | 6.4:1 | 7.9:1 | 4.5:1 | ✅ |
| `text.on-accent` on `accent.default` | 5.2:1 | 8.0:1 | 4.5:1 | ✅ |
| `accent.subtle-text` on `accent.subtle-bg` | 6.9:1 | 9.4:1 | 4.5:1 | ✅ |
| `semantic.warning-text` on `semantic.warning-bg` | 5.8:1 | 8.9:1 | 4.5:1 | ✅ |
| `semantic.danger-text` on `semantic.danger-bg` | 7.1:1 | 8.6:1 | 4.5:1 | ✅ |
| `semantic.success-text` on `semantic.success-bg` | 6.3:1 | 8.4:1 | 4.5:1 | ✅ |
| `semantic.info-text` on `semantic.info-bg` | 6.6:1 | 8.7:1 | 4.5:1 | ✅ |

## Internal-operator theme

| Pair | Light | Dark | Requirement | Status |
|---|---|---|---|---|
| `text.primary` on `bg.surface` | 15.1:1 | 14.8:1 | 4.5:1 | ✅ |
| `text.secondary` on `bg.surface` | 6.4:1 | 7.9:1 | 4.5:1 | ✅ |
| `text.on-accent` on `accent.default` | 5.2:1 | 8.0:1 | 4.5:1 | ✅ |
| `accent.subtle-text` on `accent.subtle-bg` | 6.9:1 | 9.4:1 | 4.5:1 | ✅ |
| `semantic.warning-text` on `semantic.warning-bg` | 5.8:1 | 8.9:1 | 4.5:1 | ✅ |
| `semantic.danger-text` on `semantic.danger-bg` | 7.1:1 | 8.6:1 | 4.5:1 | ✅ |
| `semantic.success-text` on `semantic.success-bg` | 6.3:1 | 8.4:1 | 4.5:1 | ✅ |
| `semantic.info-text` on `semantic.info-bg` | 6.6:1 | 8.7:1 | 4.5:1 | ✅ |

## Health status colors (internal-operator only, fleet coordinate matrix)

| Pair | Light | Dark | Requirement | Status |
|---|---|---|---|---|
| `health.clean` dot on `bg.surface` | ≥3:1 (non-text UI component, WCAG 1.4.11) | ≥3:1 | 3:1 | ✅ — verify exact ratio when the dot glyph is finalized in implementation; paired with a text label regardless per component spec |
| `health.watch` dot on `bg.surface` | ≥3:1 | ≥3:1 | 3:1 | ✅ (same caveat) |
| `health.breach` dot on `bg.surface` | ≥3:1 | ≥3:1 | 3:1 | ✅ (same caveat) |

**Verification note for the engineer:** the `$ratio` values above were computed against the specific hex values in `tokens/base.tokens.json` at design time. If any base ramp value is changed during implementation (e.g., a color adjusted for brand reasons), **every ratio in this table must be recomputed before merge** — this table is a build gate, not a one-time design artifact. Wire an automated contrast-check into the token build pipeline (most style-dictionary-style toolchains support a contrast-validation plugin) rather than relying on this document being manually re-checked.

## What is NOT yet verified (flagged for the engineer's own pass)

- The exact `health.*` dot glyph size and its precise on-`bg.surface` ratio — sized once the actual icon/dot asset exists in the codebase, since "3:1 non-text contrast" (WCAG 1.4.11) depends on the rendered glyph's actual colors, not just the token pair.
- Focus-ring contrast (`border.focus` against every possible background it can appear on) — verified conceptually (teal-600/teal-400 against the full range of surface tokens all clear 3:1 by a wide margin given the ramp's spacing) but not independently re-tabulated pair-by-pair here; recommend a dedicated automated check in CI per `component-contracts.md`'s acceptance criterion 1.
