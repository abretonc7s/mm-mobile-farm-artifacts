# PR #32404 — Comment Triage

PR: feat(perps): enable RoE sign toggle on Auto Close TP/SL  
Branch: TAT-3398-feat-add-roe-sign-toggle

## Inherited context

- **Family ID:** 199ace83-b51c-4119-ba60-2b0b4cc18b6b (TAT-3398)
- **Scope:** Enable tappable RoE sign toggles for Auto Close TP/SL on mobile perps
- **Prior work:** Original feature + self-review rounds (a11y, analytics sign recompose, unit tests) + fix commit `f94192ac81` for order-view sign-aware validation
- **Trusted recipe:** `artifacts/recipe.json` — 7/7 ACs (AC1–AC7), 39 workflow nodes

## Comments

| # | Author | Source | File / ID | Triage | Action |
|---|--------|--------|-----------|--------|--------|
| 1 | cursor[bot] | inline 3474511814 | usePerpsTPSLForm.ts:1051–1085 | REAL (fixed) | Order view rejected signed TP/SL; `hasInvalidTPSL` stayed true. Fixed in `f94192ac81` via sign-aware effective direction in `PerpsOrderView`. |
| 2 | gambinish | review CHANGES_REQUESTED 4574797409 | PerpsOrderView ~:1983/:2007 | REAL (fixed) | Same root cause as #1 — Place Order disabled after signed TP/SL confirm. Addressed in `f94192ac81`. |
| 3 | gambinish | review CHANGES_REQUESTED 4593430638 | Auto Close sheet | REAL | Sign toggle cleared validation errors when user had typed a trigger **price** directly: toggle recomputed from a clamped `0%` magnitude and moved the price, hiding the error. Fix: only recompute trigger on sign toggle when RoE % is the active input (`tpUsingPercentage` / `slUsingPercentage`); show field errors without gating on combined `isValid`. |
| 4 | abretonc7s | conversation 4799410026 | — | OUT_OF_SCOPE | Orchestrator worker-report comment; not actionable review feedback. |
| 5 | abretonc7s | conversation 4804208576 | — | OUT_OF_SCOPE | Fix notification for #1/#2; informational. |
| 6 | abretonc7s | conversation 4804220380 | — | OUT_OF_SCOPE | Prior triage worker report; superseded by this run. |

## Fix summary (this session)

### Sign-toggle validation error persistence (gambinish #4593430638)

- `usePerpsTPSLForm.ts` — `handleTakeProfitSignToggle` / `handleStopLossSignToggle` now recompute trigger price only when the RoE percentage is the active input (`tpUsingPercentage` / `slUsingPercentage`). Manual price entry keeps the typed price; sign-aware validation re-runs so errors are not cleared until the constraint actually passes.
- `PerpsTPSLView.tsx` — field error text and input styling keyed off per-field error strings (`takeProfitError`, `stopLossError`, `stopLossLiquidationError`) instead of combined `isValid`.
- `usePerpsTPSLForm.test.ts` — two regression tests for manual-price sign-toggle validation.

## Validation (this session)

- ESLint changed files: 0 errors; 7 pre-existing warnings (deprecation/react-compiler on untouched lines).
- Prettier: PASS on changed files.
- Jest: 230/230 PASS (`usePerpsTPSLForm`, `PerpsTPSLView`, `PerpsOrderView` tests).
- Recipe re-validation: **PASS 39/39** (re-run after Metro/CDP available on port 8064).

## Operator follow-up

- Reply to gambinish on review 4593430638 with fix summary and request re-review.
- Resolve cursor[bot] inline thread if not already resolved.
- Changes are **not committed/pushed** — operator to review, commit, and push.
