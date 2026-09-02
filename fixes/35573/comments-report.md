# PR #35573 comment triage

Ticket: TAT-3772 — deposit tap should navigate immediately; Pay with should not stall.
PR: fire-and-forget `depositWithConfirmation()` after confirmation navigation, with a focus-aware dismiss guard.

Skipped without reply (status-only automation): 2
- `github-actions[bot]` #5506154352 CLA signature
- `github-actions[bot]` #5506183754 Smart E2E test selection

No `CHANGES_REQUESTED` reviews.

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | cursor[bot] | `usePerpsHomeActions.ts:190` (+ MarketDetails `L729-L747`) | REAL | Stale `setTimeout` / `depositWithConfirmation()` settlement can null the latest guard. Add a prep session that cancels the pending timeout, ignores stale settlement, and reuses one in-flight prep against the latest guard. |
| 2 | github-actions[bot] | `usePerpsHomeActions.test.ts:167` (J6) | REAL | Remove `afterEach` `setTimeout(0)` sleep; it can hang when a sibling test uses fake timers. |
| 3 | github-actions[bot] | `usePerpsHomeActions.test.ts:196` (J8) | REAL | Isolate the fake-timer test in a nested describe with `beforeEach`/`afterEach` timer setup. |
| 4 | github-actions[bot] | `PerpsMarketDetailsView.test.tsx:1825` (J8) | FALSE POSITIVE | Fake timers start after render on purpose so mount effects use real timers. `try/finally` always restores (including on throw). Historical rate 0/431. Suggested nested describe would freeze mount timers. |

## Inherited recipe AC coverage

Source: `inputs/inherited/recipe-coverage.md` + `artifacts/recipe.json` (family-inherited, trusted).

| AC | Proof | Nodes | Inherited verdict |
|----|-------|-------|-------------------|
| 1. Deposit tap navigates immediately to confirmation | mixed | ac1-press-deposit → ac1-wait-confirmation (`custom-amount-input`, 4s) → ac1-wait-pay-with → screenshot | PROVEN |
| 2. Pay with token list loads without multi-second stall | mixed | ac2-press-pay-with → ac2-wait-token-sheet (`pay-with-crypto-section-preferred-token-row`, 4s) → screenshot | PROVEN |

Recipe is the after/with-state validation flow. Re-run uses the same node IDs against `branch + origin/main`.

## Recipe re-validation

- Result: PASS (13/13 nodes, 37074ms)
- summary: `artifacts/recipe-run/summary.json`
- trace: `artifacts/recipe-run/trace.json`
- manifest: `artifacts/recipe-run/artifact-manifest.json`
- AC1 screenshot: Add funds amount screen, Pay with ETH ($3.17), keypad visible (`screenshots/evidence-ac1-deposit-confirmation.png`, simctl)
- AC2 screenshot: Pay with sheet lists ETH $3.17 and Other assets (`screenshots/evidence-ac2-pay-with-list.png`, simctl)
- Integration: rebased onto origin/main (`artifacts/integration-status.txt`)

## Summary

- Total comments: 4 (2 REAL, 0 FALSE POSITIVE, 2 OUT OF SCOPE)
  - Finding-level: 2 REAL (stale prep race; J6+J8 home-actions tests), 1 FALSE POSITIVE (MarketDetails J8), 2 skipped status-only
- Commit SHA for fixes: `c4e7408f1da65cc8aee2c5b2a83078ae1c9697dc`
- Files changed:
  - `app/components/UI/Perps/utils/depositConfirmationGuard.ts`
  - `app/components/UI/Perps/utils/depositConfirmationGuard.test.ts`
  - `app/components/UI/Perps/hooks/usePerpsHomeActions.ts`
  - `app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts`
  - `app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.tsx`
- Recipe re-validation: PASS
- Integration status: rebased
- Replies: inline on review `3911860795`; consolidated issue comment `5506607069`; skipped CLA `5506154352` and Smart E2E `5506183754`
- Review thread `PRRT_kwDOCG4DHc6eaSzx` resolved
