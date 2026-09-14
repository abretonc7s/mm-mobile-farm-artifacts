# Step 4 — live comments (PR 35832)

Fetched 2026-09-14 after rebase onto origin/main.

## Actionable

| Source | ID | Author | File:line | Unresolved | Content |
|---|---|---|---|---|---|
| review_comment | 4006111799 | michalconsensys | usePerpsMarketHeaderActions.ts:95 | yes | Header stamp check misses iOS edge-swipe / Android hardware back; intercept beforeRemove / BackHandler |
| review_comment | 4006112036 | michalconsensys | PerpsMarketListView.tsx:357 | yes | List back still parent-aware goBack; after Lite→Pro can pop PERPS.ROOT to wallet |
| review_comment | 4006112200 | michalconsensys | PerpsMarketListView.tsx:354 | yes | preserveHomeDroppedFromHistory only on replaceOnSelect; stamp the push path too |
| issue_comment | 5665437346 | michalconsensys | types/navigation.ts | n/a | homeDroppedFromHistory missing from PerpsStackParamList |
| review_comment | 3986216821 | cursor[bot] | usePerpsMarketHeaderActions.ts:95 | resolved | Unstamped Home drop skips fallback; already replied 3987812668 |
| review_comment | 4001899297 | cursor[bot] | usePerpsMarketHeaderActions.ts:94 | resolved | Stamp lost after market replace; already replied 4001979273 |
| issue_comment | 5578623640 | github-actions[bot] | tests | n/a | metamask-flaky-test-detection: J4 MarketList waitFor; J4 ModeSelection Promise.resolve; J4 ProHeader act; J3 perpsModeSwitch mocks |

## Already-replied (do not re-reply)

- 3987812668 abretonc7s on 3986216821
- 4001979273 abretonc7s on 4001899297
- 5578694608 abretonc7s J9 flaky-test triage
- 5658340698 abretonc7s J4/J6/J3 flaky-test triage (does not cover MarketList waitFor or ProHeader act)

## Skipped status-only (6, no reply)

- 5578599388 github-actions CLA
- 5658540794 github-actions smart-e2e-selection
- 5658609281 sonarqubecloud quality gate
- 5658658201 github-actions performance results
- 5175282853 cursor[bot] stale review summary
- 5193534100 cursor[bot] review summary ("found 1 potential issue"; inline already listed)

No CHANGES_REQUESTED reviews. Empty review wrapper bodies ignored.
