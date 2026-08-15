# Comments triage — PR #34789

Skipped status-only automation (no reply): 5
- `5290199503` github-actions[bot] CLA signature
- `5290647503` abretonc7s previous farmslot worker report
- `5290752791` github-actions[bot] Smart E2E test selection
- `5290919841` sonarqubecloud[bot] Quality Gate passed
- `5290994832` github-actions[bot] Performance test results (non-blocking)

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | matthewwalsh0 | usePayTokenAccountBalance.ts:22 | REAL | Drop `isResolved`/`isRawResolved`; use `undefined` on `balanceUsd`/`balanceRaw` for unknown |
| 2 | cursor[bot] | PerpsOrderView.tsx:2268 | REAL (already fixed) | Prior run added `hasInsufficientPayTokenBalance` to Place Order `isDisabled`; thread resolved |
| 3 | cursor[bot] | useInsufficientPayTokenBalanceAlert.ts | REAL (already fixed) | Prior run gated fees on raw-known; will keep via `balanceRaw !== undefined` after #1 |
| 4 | github-actions[bot] | PerpsOrderView.test.tsx J6 | FALSE POSITIVE | `setTimeout(0)` flushes the file's rAF mock inside `act()`; 0/360 failures; not a DOM wait |
| 5 | github-actions[bot] | PerpsOrderView.test.tsx J9 | FALSE POSITIVE | Pay-mock lets are reset in the nested describe that mutates them; 0/360 failures |
| 6 | github-actions[bot] | usePerpsOrderValidation.test.ts J8 | FALSE POSITIVE | Pre-existing fake-timer + `advanceTimersByTime` + `waitFor` workaround; 0/360 failures |
| 7 | github-actions[bot] | usePerpsToasts.test.tsx J9 | FALSE POSITIVE | `beforeEach` already resets both module-level lets; 0/360 failures |

## Context

PR TAT-3742: lite-mode Perps "pay with token" treated an unresolved balance as `0`, stacking funding errors and hiding Place Order. The hook added `isResolved`/`isRawResolved` so callers could tell a stale snapshot from a measured balance.

Matthew's CHANGES_REQUESTED review: extra booleans are less idiomatic than `undefined` on the existing properties. That matches the PR's own rule ("an unresolved balance is unknown, not zero") and removes the flags the previous pr-complete round introduced.

## Inherited AC coverage (for step 10)

See `inputs/inherited/report.md`, `inputs/inherited/recipe-coverage.md`, and `artifacts/recipe.json`.

| AC | Claim | Proof |
|----|-------|-------|
| AC1 | At most one funding message; no false $0 available | `ac1-assert-no-perps-balance-warning`, `ac1-assert-no-zero-available-row`, screenshot |
| AC2 | Place-order button stays in the viewport after payment switch | `ac2-assert-action-button-visible`, `ac2-assert-button-still-visible` |
| AC3 | Slider stays usable while pay-token balance is unresolved | funding-state unit tests via `ac3-ac4-run-funding-state-tests` |
| AC4 | Below-minimum token shows the $10 minimum-order copy | same funding-state tests |

Recipe is family-inherited, 21 nodes, no arbitrary-code primitives. Re-validation must pass against `branch + origin/main`.

## Recipe re-validation

SKIPPED — mobile runtime unavailable, skipping recipe re-validation.

`mm-harness launch --platform ios --preflight-mode fast` exited 1: portable harness wrapper missing at `$HOME/dev/metamask/metamask-skills/domains/agentic/skills/recipe-harness/scripts/recipe-harness` (`METAMASK_SKILLS_DIR` unset). Runtime capability catalog has no providers. Did not invent a replacement launch path.

## Summary

- Total comments: 9 (3 REAL, 1 FALSE POSITIVE, 5 OUT OF SCOPE)
- Commit SHA for fixes: `37f5e3fea07312b64130cacca551bf898d9aefd6`
- Files changed:
  - `app/components/Views/confirmations/hooks/pay/usePayTokenAccountBalance.ts`
  - `app/components/Views/confirmations/hooks/pay/usePayTokenAccountBalance.test.ts`
  - `app/components/Views/confirmations/hooks/alerts/useInsufficientPayTokenBalanceAlert.ts`
  - `app/components/Views/confirmations/hooks/alerts/useInsufficientPayTokenBalanceAlert.test.ts`
  - `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx`
  - `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.test.tsx`
  - `app/components/Views/confirmations/hooks/pay/usePayWithPreferredToken.ts`
  - `app/components/Views/confirmations/hooks/pay/usePayWithPreferredToken.test.ts`
  - `app/components/Views/confirmations/components/rows/pay-with-row/pay-with-row.tsx`
  - `app/components/Views/confirmations/components/rows/pay-with-row/pay-with-row.test.tsx`
- Recipe re-validation: SKIPPED (mobile runtime unavailable)
- Integration status: `rebased`
- Local CI: scoped ESLint 0 errors (11 pre-existing warnings); `format:check` pass; `lint:tsc` failures are origin/main TWAP/strategy types, not this diff; unit tests 212/212 pass (77 pay + 135 PerpsOrderView)
