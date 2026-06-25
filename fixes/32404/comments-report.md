# PR #32404 — Review Comment Triage

PR: feat(perps): enable RoE sign toggle on Auto Close TP/SL
Branch: TAT-3398-feat-add-roe-sign-toggle

## Context
The PR adds a tappable +/- RoE sign badge to the Auto Close (TP/SL) sheet so a
user can set a negative take profit or a gain-side stop loss. All sign logic
lives in `usePerpsTPSLForm`, which validates against an *effective* direction
derived from the chosen sign. The sheet persists only the resulting trigger
**price** — not the sign.

## Comments

| # | Author | Source | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | cursor[bot] | inline (id 3474511814) | usePerpsTPSLForm.ts:1051-1085 | REAL | Order view re-validated stored TP/SL with classic long/short side rules, rejecting signed triggers → `hasInvalidTPSL` stayed true, Place Order disabled. Made the order view sign-aware. |
| 2 | gambinish | review CHANGES_REQUESTED (id 4574797409) | PerpsOrderView (~:1983/:2007) | REAL | Same root cause as #1 (P1). Negative TP / gain-side SL set in the sheet left Place Order disabled. Fixed with sign-aware effective direction. |
| 3 | abretonc7s | conversation (id 4799410026) | — | OUT OF SCOPE | Orchestrator worker-report comment, not actionable review feedback. No reply needed. |

## Fix summary
Both REAL comments share one root cause: `PerpsOrderView` validated
`orderForm.takeProfitPrice` / `stopLossPrice` against `orderForm.direction`
only, with no knowledge of the sign chosen in the sheet. A signed trigger
(price on the classic "wrong" side) was therefore rejected.

Fix (contained in `PerpsOrderView.tsx`):
- Capture the RoE sign from the sheet's `trackingData` (already carries the
  signed RoE percentage) into local `takeProfitSign` / `stopLossSign` state on
  `onConfirm`. Defaults match the sheet (`+` TP / `-` SL).
- Derive an effective direction from the sign (mirroring `usePerpsTPSLForm`)
  and validate against it, so a signed trigger is accepted while the
  un-toggled default keeps the existing wrong-side guard intact.

This preserves the entire pre-existing wrong-side validation suite (default
sign → effective direction == `orderForm.direction`) and only changes behavior
when the user has toggled the sign.

Added a regression test: a long order with a TP below current price is rejected
by default but accepted after the sheet confirms a negative RoE.

## Inherited recipe coverage
The inherited recipe (`artifacts/recipe.json`, 39 steps) proves the Auto Close
sheet's RoE sign behavior AC1-AC7 (defaults + TP / - SL, toggle keeps value &
recomputes trigger, preset flips sign, negative TP → below-entry trigger, reset
on reopen). It covers the *sheet*; the review fix is in the *order view*, which
is covered by the new unit test above.

## Validation results
- ESLint (changed files): 0 errors (6 pre-existing deprecation/react-compiler
  warnings on untouched lines).
- `PerpsOrderView.test.tsx`: 101/101 passed (full pre-existing wrong-side suite
  green → default behavior unchanged; new signed-acceptance test green).
- Prettier: both changed files conform.
- Recipe re-validation (post branch+origin/main merge, mobile adapter): **PASS
  39/39** (`artifacts/recipe-run/summary.json`).
- Note: full `yarn lint:tsc` skipped per worker-slot policy (forbidden in
  slots; left to CI). TS-aware ESLint substituted, 0 errors.
- Merge-main status: clean (no conflicts).

## Final summary
- Total comments: 3 (2 REAL, 0 FALSE POSITIVE, 1 OUT OF SCOPE)
- Fix commit: `f94192ac81` — "fix: address review comments on PR #32404"
- Files changed:
  - `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx`
  - `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.test.tsx`
- Recipe re-validation: PASS 39/39
- Merge-main status: clean
- Replies: cursor[bot] inline thread replied + resolved; gambinish
  CHANGES_REQUESTED replied via conversation (re-approval is the reviewer's);
  abretonc7s worker report — OOS, no reply.
