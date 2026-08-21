# Comments triage — PR #34789

PR intent: Lite Perps treated an unresolved wallet-token balance as `$0` after switching payment methods. The order flow now reads the live paying-account balance, keeps unknown balances as `undefined`, shows at most one funding message, and blocks submit until the balance resolves.

Skipped without reply (status-only automation): 4
- github-actions CLA (5290199503)
- github-actions Smart E2E selection (5345633424)
- sonarqubecloud Quality Gate (5345731611)
- github-actions Performance Test Results (5346199399) — informational, non-blocking

Prior human triage comment (5299847404, abretonc7s) is already the flaky-test response, not a new request.

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | cursor[bot] 3781582063 | PerpsOrderView.tsx:2279 | REAL (already on branch) | `hasInsufficientPayTokenBalance` is on both Place Order `isDisabled` lists. No further change. |
| 2 | cursor[bot] 3781855756 | useInsufficientPayTokenBalanceAlert.ts | REAL (already on branch) | Fee check gates on `isPayBalanceRawKnown` (`accountBalanceRaw !== undefined`), USD check stays on `isPayBalanceKnown`. No further change. |
| 3 | matthewwalsh0 3783645243 | usePayTokenAccountBalance.ts | REAL (already on branch) | Extra flags dropped; `balanceUsd`/`balanceRaw` are `string \| undefined`. No further change. |
| 4 | matthewwalsh0 3793297994 | usePayWithPreferredToken.ts | REAL (already on branch) | Live balance only: `liveBalanceUsd ?? '0'`. Does not fall back to `selectedToken.balanceUsd`. No further change. |
| 5 | matthewwalsh0 3793303225 | useInsufficientPayTokenBalanceAlert.ts:139 | REAL (already on branch) | Place Order stays disabled via `isPayBalanceLoading` until the live balance resolves. No further change. |
| 6 | matthewwalsh0 3793304361 | pay-with-row.tsx | REAL (already on branch) | Row no longer falls back to `payToken.balanceUsd` (wrong-account snapshot). No further change. |
| 7 | cursor[bot] 3815225399 | usePerpsOrderValidation.ts:244 | REAL | Fix was claimed in 45f48d0143f but that commit is not on the PR branch (dangling after later history). Re-apply: filter the stored generic balance string out of `errors` as soon as `skipBalanceError` becomes true, without waiting for the debounce. |
| 8 | github-actions 5290235689 | PerpsOrderView.test.tsx J6 | FALSE POSITIVE | `setTimeout(0)` flushes this file's `requestAnimationFrame` → `setTimeout(cb, 0)` mock inside `act()`, not a DOM wait. Historical 0/436. |
| 9 | github-actions 5290235689 | PerpsOrderView.test.tsx J9 | FALSE POSITIVE | Nested describe that mutates pay mocks already resets them in `afterEach`. Historical 0/436. |
| 10 | github-actions 5290235689 | usePerpsOrderValidation.test.ts J8 | FALSE POSITIVE | Pre-existing suite advances the debounce with `jest.advanceTimersByTime` before `fastWaitFor`. Historical 0/436. |

CHANGES_REQUESTED reviews from matthewwalsh0 (4937146587, 4947816977) cover comments 3–6; those threads are resolved. GitHub still shows CHANGES_REQUESTED until a new review is submitted; no extra code for that.

## Local CI

- Scoped ESLint: pass
- `yarn lint:tsc`: 32 errors, all pre-existing on `origin/main` (react-navigation 3-arg `navigate` / `NavigationIndependentTree`). None in changed files (`usePerpsOrderValidation.ts` / `.test.ts`).
- `yarn format:check`: pass
- Jest: `usePerpsOrderValidation.test.ts` 35/35, `PerpsOrderView.test.tsx` 139/139, plus the other PR test files in the first-five gate.

## Inherited recipe AC coverage

Family recipe `artifacts/recipe.json` covers TAT-3742 ACs:

| AC | Proof | Nodes |
|----|-------|-------|
| 1. At most one funding message; no Perps-balance `$0` after a token switch | mixed | `ac1-assert-no-perps-balance-warning`, `ac1-assert-no-zero-available-row`, `ac1-screenshot-single-message` |
| 2. Place-order button stays in the viewport | visual | `ac2-assert-action-button-visible`, `ac2-assert-button-still-visible` |
| 3. Slider stays usable while the pay-token balance is unresolved | state | `ac3-ac4-run-funding-state-tests` |
| 4. Below-minimum pay-token state states the $10 minimum | state | `ac3-ac4-run-funding-state-tests` |

## Recipe re-validation

SKIPPED: mobile runtime unavailable. `mm-harness launch ios --verify` opened the dev client but the in-app bridge never matched (`wait-for-bridge: no bridge target matched ... 90 polls`). `mm-harness call app.status` hung. Did not rebuild Metro or the native app (slot recovery is out of scope). Unit tests cover the review fix.

## Summary

- Total comments: 11 (7 REAL, 1 FALSE POSITIVE with 3 findings, 4 OUT OF SCOPE skipped)
- Commit SHA for fixes: `8ae9149c9eeab4f548a21dd7a10d080266fc8e0f`
- Files changed: `app/components/UI/Perps/hooks/usePerpsOrderValidation.ts`, `app/components/UI/Perps/hooks/usePerpsOrderValidation.test.ts`
- Recipe re-validation: SKIPPED (mobile runtime unavailable)
- Integration status: `rebased`


