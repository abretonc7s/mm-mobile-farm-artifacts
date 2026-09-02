# PR #35573 comments triage

PR: fix(perps): performance issue: Deposit button delay and token list lag in Perps flow
Ticket: [TAT-3772](https://consensyssoftware.atlassian.net/browse/TAT-3772) — deposit tap felt stuck; Pay With token list lagged. Expected: immediate haptic + confirmation skeleton, then prep.

Fetched 2026-09-02. REQUEST_CHANGES reviews: none.

Skipped status-only (no reply): 3
- 5506154352 CLA
- 5506640744 Smart E2E Test Selection
- 5506830945 Performance Test Results

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | cursor[bot] 3911860795 | usePerpsHomeActions.ts:190 | REAL (already fixed) | Prep session cancels timeout, ignores stale settlement, reuses in-flight prep. Replied + resolved in 7669847a6d (was c4e7408f1d). No further change. |
| 2 | cursor[bot] 3912193415 | depositConfirmationGuard.ts:213 | REAL | Keep the guard after failed prep so dispose/next tap can cancel a waiting dismissWhenShown listener. Callers must not null the session without dispose. |
| 3 | cursor[bot] 3912193426 | depositConfirmationGuard.ts:90 | REAL | Treat Pay With routes as still in the deposit confirmation flow. Dismiss Pay With then confirmation on prep failure. |
| 4 | github-actions[bot] 5506202407 J9 | PerpsMarketDetailsView.test.tsx:52 | FALSE POSITIVE | Outer beforeEach already sets `mockConnectionInitialized = true` (HEAD and origin/main). Historical rate 0/430. |
| 5 | github-actions[bot] 5506202407 J8 | usePerpsHomeActions.test.ts:196 | REAL | Eligible-user test still used `waitFor` against deferred `setTimeout(0)` on real timers. Converted that test and the deposit string-error test to fake timers + `runAllTimersAsync`. |

Issue comment 5506607069 is our prior flaky-test triage, not a new finding.

## Totals

- Total comments: 8 (3 REAL this run, 1 REAL already-fixed, 1 FALSE POSITIVE, 3 OUT OF SCOPE status-only)
- Actionable this run: 4 (3 REAL code fixes + 1 FALSE POSITIVE reply)
- Commit SHA: `700b2145c1d05cda9abbb761b3368f537d82e281`
- Files changed:
  - `app/components/UI/Perps/utils/depositConfirmationGuard.ts`
  - `app/components/UI/Perps/utils/depositConfirmationGuard.test.ts`
  - `app/components/UI/Perps/hooks/usePerpsHomeActions.ts`
  - `app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts`
  - `app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.tsx`
- Recipe re-validation: PASS 13/13 (`temp/tasks/fix/35573-0902-163558/artifacts/recipe-run/summary.json`)
- Integration status: rebased

## Inherited recipe AC coverage

See `inputs/inherited/report.md` and `artifacts/recipe.json`.
- AC1 mixed: Add funds opens deposit confirmation without waiting for tx prep (`custom-amount-input`, `pay-with`).
- AC2 mixed: Pay With sheet lists a crypto asset (`pay-with-crypto-section-preferred-token-row`).
- Parent run reported 2/2 PROVEN.

## Recipe re-validation (step 10)

- Recipe: `temp/tasks/fix/35573-0902-163558/artifacts/recipe.json` (family-inherited)
- Harness: `/Users/deeeed/.npm-global/bin/mm-harness` 0.45.1, slot `mini-mm-2`, watcher 8072
- Doctor: pass / ready
- Run: PASS 13/13 in 46117ms
- summary: `temp/tasks/fix/35573-0902-163558/artifacts/recipe-run/summary.json`
- Screenshots confirm Add funds amount screen (Pay with ETH $3.14) and Pay with sheet (ETH + Other assets)
- Integration: rebased onto origin/main before this run
