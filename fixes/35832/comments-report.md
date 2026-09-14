# Comments report — PR #35832

Fetched live 2026-09-14. HEAD after rebase: `7690b91b7f`.

## PR context

Fixes TAT-3786: after Lite → Pro drops Perps Home from the stack, the market header back arrow could pop `PERPS.ROOT` out to wallet because `canGoBack()` is parent-aware. Back now pops only when the Perps stack itself has history **or** Home was not stamped as dropped; otherwise it uses `backFallback` (`home` for Lite, `wallet` for Pro).

## Comment inventory

| # | Author | Source | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | cursor[bot] | review_comment 3986216821 | `usePerpsMarketHeaderActions.ts:95` | REAL (already fixed) | Stamp already applied in `3d9351e` / `7690b91`. Thread resolved. Already replied. |
| 2 | github-actions[bot] | issue_comment 5578623640 | `PerpsModeSelectionView.test.tsx` J4 | FALSE POSITIVE | No `waitFor` in the file. Snippet is a microtask flush. |
| 3 | github-actions[bot] | issue_comment 5578623640 | `PerpsModeSelectionView.test.tsx` J6 | FALSE POSITIVE | `await Promise.resolve()` flushes `handleSelect`'s mocked `await`, not a timer. |
| 4 | github-actions[bot] | issue_comment 5578623640 | `perpsModeSwitch.test.ts` J3 | FALSE POSITIVE | `clearAllMocks` is correct; `resetAllMocks` would wipe selector implementations. |
| 5 | abretonc7s | issue_comment 5578694608 | — | n/a | Author's prior J9 triage. Not a new finding. |
| 6 | github-actions[bot] | issue_comment 5578599388 | — | skipped | CLA status-only |
| 7 | github-actions[bot] | issue_comment 5632447134 | — | skipped | Smart E2E selection status-only |
| 8 | sonarqubecloud[bot] | issue_comment 5632551424 | — | skipped | Quality gate passed |
| 9 | github-actions[bot] | issue_comment 5632887891 | — | skipped | Non-blocking perf results; timeout is unrelated open-position E2E |

Skipped status-only comments: 4 (CLA, Smart E2E, Sonar, Performance results).
REQUEST_CHANGES reviews: none.

## Triage notes

### 1. Unstamped Home drop — REAL, already fixed

Bugbot on `2a5b18f6c5` was right: `wasPerpsHomeDroppedFromHistory` only sees the stamp, and Home → Pro `navigation.reset` originally omitted it, so Back still called `goBack()` onto wallet.

Follow-up `3d9351e` / rebased `7690b91` wraps both HomeView and ModeSelectionView Home → Pro resets with `withHomeDroppedFromHistory`. Rebase conflict with main's `buildDefaultProMarket(lastViewedMarketSymbol)` kept both the stamp and the last-viewed symbol.

`routes/index.tsx` `initialParams` for an already-Pro stack is not a Home drop. Back there should pop `PERPS.ROOT` to the parent (wallet / Explore). Not stamped on purpose.

Thread `PRRT_kwDOCG4DHc6hWeJx` is resolved. Reply already posted (`3987812668`). No second reply.

### 2–4. Flaky-test detection — FALSE POSITIVE

Comment was edited in place after the original J9 findings (already answered in `5578694608`). Current body is J4 / J6 / J3 against `3d9351e`. Historical rates 0/145, 0/269, 0/489.

- **J4:** pattern requires `waitFor` with no assertion. File has zero `waitFor` calls. Line 66 in the report is a jest mock, not the cited snippet.
- **J6:** `handleSelect` awaits `markPerpsModeSelectionCompleted()`, mocked as `Promise.resolve()`. `await Promise.resolve()` is one microtask tick, then the real `expect`s. `requestAnimationFrame` is mocked to run inline in `beforeEach`. Not `setTimeout` / `sleep`.
- **J3:** `jest.resetAllMocks()` would clear `selectPerpsLastViewedMarketSymbol`'s default `jest.fn(() => 'BTC')` and per-test `useSelector` implementations. `clearAllMocks` is the right reset.

No code change for these.

## Review-fix commit

None. No remaining REAL unfixed comments. Step 3 rebased onto `origin/main` (`c131648fc6`); that history still needs a force-with-lease push in step 11.

## Inherited AC coverage (step 10b)

Inherited `report.md` is missing. Recipe and coverage come from parent run `4b157fa5-fd34-44bb-a0e3-3e4da5677343`.

Ticket TAT-3786 has no `## Acceptance Criteria` block. Two ACs are derived from the description:

| AC | Proof | Recipe nodes | Inherited verdict |
|----|-------|--------------|-------------------|
| AC1. After Lite → Pro → Lite, header back lands on Perps home, not wallet | mixed (`ui.wait_for` + screenshot) | `ac1-press-back` → `ac1-wait-perps-home` → `ac1-assert-not-wallet` → `ac1-screenshot-landing` | PROVEN on parent run |
| AC2. Lite market → Pro workstation → Lite market again | mixed (`ui.wait_for` on claimed targets + screenshots) | `ac2-wait-lite-start` → `ac2-switch-to-pro` → `ac2-wait-pro` → `ac2-screenshot-pro` → `ac2-switch-back-lite` → `ac2-wait-lite-return` → `ac2-screenshot-lite-return` | PROVEN on parent run |

This run re-validates the same recipe against `branch + origin/main` after the rebase. No new recipe. No `runtime.capability.*` lease; proof goes through the prepared mobile runtime.

## Recipe re-validation

PASS. `artifacts/recipe-run/summary.json` 18/18. Inspected PNGs:

- AC2 Pro: Pro pill, Isolated 3x, order book, Place order
- AC2 Lite return: Lite pill, BTC-USD market, Long/Short
- AC1 back: Perps Testnet home, $629.30, Withdraw / Add funds, Watchlist (not wallet)

First run failed at `setup-unlock` (stability window). Unrelated to this branch. Restarted the app and the second run passed. First failure kept in `artifacts/recipe-run-unlock-fail/`.

## Replies

- review_comment 3986216821: already replied (`3987812668`), thread resolved. No second reply.
- issue_comment 5578623640: posted consolidated triage as `5658340698`.
- Status-only comments (CLA, Smart E2E, Sonar, Performance): no reply.

## Totals

- Total comments: 9 (1 REAL, 3 FALSE POSITIVE, 5 OUT OF SCOPE)
- Commit SHA for fixes: none (REAL bugbot finding already fixed in `7690b91b7f`)
- Files changed: rebase-only. Conflict resolution in HomeView and ModeSelectionView kept `withHomeDroppedFromHistory(...)` wrapping `buildDefaultProMarket(lastViewedMarketSymbol)`.
- Recipe re-validation: PASS
- Integration status: rebased
