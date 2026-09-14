# Comments report — PR 35832

PR intent (TAT-3786): after Lite → Pro drops Perps Home, `<` on the market page must return to Perps home, not wallet. `canGoBack()` is parent-aware, so the header only pops when the Perps stack itself has history or Home was not dropped.

Skipped status-only automation (6, no reply): CLA, smart-e2e-selection, SonarQube gate, performance results, two Bugbot review summaries.

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | michalconsensys | usePerpsMarketHeaderActions.ts:95 | REAL | Intercept GO_BACK/POP in `beforeRemove` with the same dropped-Home fallback as the header button |
| 2 | michalconsensys | PerpsMarketListView.tsx:357 | REAL | List back uses the same should-pop / fallback check; Lite → home, Pro → wallet |
| 3 | michalconsensys | PerpsMarketListView.tsx:354 | REAL | Stamp `StackActions.push` params with `preserveHomeDroppedFromHistory` |
| 4 | michalconsensys | types/navigation.ts | REAL | Add `homeDroppedFromHistory?: true` to stamped Perps routes |
| 5 | cursor[bot] | usePerpsMarketHeaderActions.ts:95 | FALSE POSITIVE | Home→Pro stamp already landed; thread resolved, already replied |
| 6 | cursor[bot] | usePerpsMarketHeaderActions.ts:94 | FALSE POSITIVE | Header picker replace already copies the stamp; thread resolved, already replied |
| 7 | github-actions[bot] | PerpsMarketListView.test.tsx J4 | FALSE POSITIVE | Cited line 123 is a mock; no empty `waitFor(() => {})`; real `waitFor` calls assert |
| 8 | github-actions[bot] | PerpsModeSelectionView.test.tsx J4 | FALSE POSITIVE | No `waitFor`; `Promise.resolve()` is a microtask flush after mocked async `handleSelect` (already triaged) |
| 9 | github-actions[bot] | usePerpsProMarketHeaderActions.test.ts J4 | FALSE POSITIVE | `act()` wrapping async `handlePerpsModeChange` is required, not waitFor-without-assertion |
| 10 | github-actions[bot] | perpsModeSwitch.test.ts J3 | FALSE POSITIVE | `jest.clearAllMocks()` is the reset; `resetAllMocks()` would wipe selector defaults (already triaged) |

## Inherited AC coverage

`inputs/inherited/report.md` is missing. Coverage from `inputs/inherited/recipe-coverage.md` and `artifacts/recipe.json`:

| AC | Proof | Nodes | Claim |
|---|---|---|---|
| AC1 | mixed | `ac1-press-back` → `ac1-wait-perps-home` → `ac1-assert-not-wallet` → `ac1-screenshot-landing` | After Lite→Pro→Lite, header back lands on Perps home (`perps-watchlist-header`, `perps-market-add-funds-button`), not wallet |
| AC2 | mixed | `ac2-wait-lite-start` → `ac2-switch-to-pro` → `ac2-wait-pro` → `ac2-screenshot-pro` → `ac2-switch-back-lite` → `ac2-wait-lite-return` → `ac2-screenshot-lite-return` | Lite market → Pro workstation (`perps-pro-order-form-place-order`) → Lite market (`perps-market-details-long-button`) |

Re-validation target: same recipe against `branch + origin/main` after the step 3 rebase.

## Recipe re-validation

SKIPPED: mobile runtime unavailable. `launch ios --verify` failed after a successful bundle: React Native answered without `__AGENTIC__` (`agenticPresent: false`, `route: null`). Metro: `Exception in HostFunction` then `"MetaMask" has not been registered`. One `--clear-metro` retry hit the same bridge failure. Not a missing JS package. Native/runtime mismatch after the main rebase is the likely cause; doctor `--expect-live` was not reachable.

## Totals

- Comments triaged: 7 GitHub comments (4 REAL, 3 FALSE POSITIVE, 0 OUT OF SCOPE). Flaky-test issue 5578623640 contains 4 FALSE POSITIVE findings.
- Skipped status-only: 6 (CLA, smart-e2e, SonarQube, performance results, 2 Bugbot review summaries)
- Already replied (no second reply): 3986216821 / 4001899297 Bugbot threads
- Replied this run: 4006111799, 4006112036, 4006112200 (inline), 5665437346 and 5578623640 (issue)
- Threads resolved: 4006111799, 4006112036, 4006112200
- Commit SHA: `18ec8a7c560f2729e27a999539fdb7e72686df72`
- Files changed: `usePerpsMarketHeaderActions.ts`, `PerpsMarketListView.tsx`, `navigation.ts`, `perpsModeSwitch.ts`, plus tests
- Recipe re-validation: SKIPPED (mobile runtime unavailable)
- Integration status: `rebased`
