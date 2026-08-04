# PR Review: #34267 — fix(perps): correct Pro copy for size label, order pills, and side filter

**Tier:** standard (recipe strategy: full-qa)

## Summary

The PR batches three UAT-flagged copy corrections in Perps Pro and achieves all three of its stated goals. Verified live on the Pro market view (iOS, `mmdev-1`), all three render exactly as claimed:

1. `perps.pro_order_form.size_usd` → `Size (USD)`.
2. The Orders-tab type pill now shows the order type only, via a new `formatOrderTypeLabel` helper replacing the local `getOrderTypeLabel`.
3. `PRO_POSITION_SIDE_FILTER_OPTIONS[0].labelKey` → `all_sides`, which also makes the sheet consistent with `getProPositionSideFilterButtonLabelKey`, which already returned `all_sides`.

The change is small, well-tested at the unit level, type-clean, and low-risk in the English build. The one substantive concern is in the new helper: `formatOrderTypeLabel` returns **un-translated, un-normalized strings** — hardcoded English `'Limit'`/`'Market'` literals and the raw provider-supplied `detailedOrderType`. The code it replaced routed both through `strings(...)`. That is a localization regression in 13 locales and a provider-abstraction leak that will produce inconsistent copy once MYX orders reach this surface.

### PR hygiene

No numbered Jira or linked-issue acceptance criteria are provided. This review evaluates PR-author claims (the Gherkin block in *Manual testing steps*), not ticket-bound acceptance criteria. Linked ticket TAT-3655 states only non-enumerable prose: *"All five copy strings updated as described"* — this PR corrects **three**; the Markets and DeFi copy items named in the ticket title are not in this diff. If that is intentional (split across PRs) it is worth saying so in the PR body so the ticket is not closed prematurely.

## Recipe Coverage

**Recipe decision:** `generate-ui` · **Trace:** 22/22 nodes passed, 0 failed.

| # | Claim (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|------------------|-----------------|--------------------|---------------------|----------------|---------------|
| 1 | "Then the label reads \"Size (USD)\"" | both (ran ios) | `gate-pro-view`, `ac1-assert-size-label`, `ac1-screenshot-size-label` | `evidence-ac1-size-usd-label.png` | **PROVEN** | Typed assertion `ui.wait_for test_id=perps-pro-order-form-size-input text="Size (USD)"` passed live. Revert-sensitive: pre-PR `Size USD` does not contain `Size (USD)`. Screenshot shows the label above the size input. |
| 2 | "Then limit orders show \"Limit\" and stop market orders show \"Stop market\"" | both (ran ios) | `setup-limit-order`, `ac2-open-orders-tab`, `ac2-assert-orders-list`, `ac2-assert-limit-order-open`, `ac2-screenshot-limit-pill`, `ac2-scroll-to-stop-order`, `ac2-screenshot-stop-market-pill`, `ac2-run-pill-label-tests`, `ac2-assert-pill-label-tests-pass` | `evidence-ac2-order-pill-limit.png` (primary), `evidence-ac2-order-pill-stop-market.png` | **PROVEN** | The primary image proves both halves in one frame: SOL order (Reduce only: **No**) with a bare **`Limit`** pill — pre-PR this same order rendered `Open limit` — and directly below, the ETH trigger order with **`Stop market`** (pre-PR: `Stop`). `assert_orders market=SOL state=open` confirmed the row was live, not stale. The `Tag` pill has no testID, so no typed text assertion can reach it; the non-visual half is 107/107 jest tests passing (exit 0) pinning `Limit`, `Stop market`, `Take profit limit`. |
| 3 | "Then the first option reads \"All sides\"" | both (ran ios) | `ac3-scroll-to-positions`, `ac3-open-positions-tab`, `ac3-open-side-filter`, `ac3-assert-all-sides`, `ac3-screenshot-side-filter` | `evidence-ac3-all-sides-filter.png` | **PROVEN** | Typed assertion on `...side-filter-sheet-option-all` with text `All sides` passed. Revert-sensitive: pre-PR key `all_types` renders `All types`. Screenshot shows **All sides** first and checked, above `Long`/`Short`, and the collapsed filter button also reading **All sides**. |

Overall recipe coverage: **3/3 ACs PROVEN**
Untestable: none

Full matrix and audit notes: `artifacts/recipe-coverage.md`.

## Prior Reviews

| Reviewer | State | Date | Addressed? | Notes |
|----------|-------|------|------------|-------|
| geositta | APPROVED | 2026-08-04 | n/a | Approval with an empty body and no line comments; nothing to duplicate or resolve. |

No `CHANGES_REQUESTED` reviews exist. Single commit `b1378a58`, no line comments on the PR.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Then the label reads "Size (USD)" | PASS | `ac1-assert-size-label` (typed assertion) + `evidence-ac1-size-usd-label.png` |
| 2 | Then limit orders show "Limit" and stop market orders show "Stop market" | PASS | `ac2-screenshot-limit-pill` / `ac2-screenshot-stop-market-pill` + `ac2-assert-limit-order-open` + `ac2-assert-pill-label-tests-pass` (107/107 jest) |
| 3 | Then the first option reads "All sides" | PASS | `ac3-assert-all-sides` (typed assertion) + `evidence-ac3-all-sides-filter.png` |

## Code Quality

- **Pattern adherence:** Mostly follows conventions — helper lives beside the existing `formatOrderLabel` in `orderUtils.ts`, is JSDoc'd, and is unit-tested. **Deviates** on i18n: every other user-facing string in `PerpsProOrderCard.tsx` goes through `strings(...)`; after this change the type pill is the only one that does not.
- **Complexity:** Appropriate. Removing the four-branch `getOrderTypeLabel` in favour of one shared helper is a genuine simplification, and lifting it to `orderUtils.ts` makes it reusable.
- **Type safety:** Clean. `npx tsc --noEmit` over the whole project reports **zero errors**. No `any`, no casts, no `eslint-disable` added.
- **Error handling:** N/A — pure string formatting with a defined fallback.
- **Accessibility/fallbacks:** Adequate. `PerpsProCompactInput` passes `accessibilityLabel={label}`, so the accessible name tracks the corrected `Size (USD)` copy automatically; the filter option's `title` drives both visible and accessible text. The `detailedOrderType`-absent fallback has the same shape as the removed helper, so no misleading value is rendered while data hydrates.
- **Anti-pattern findings** (against `temp/recipe/runtime/review-patterns.md`):
  - *Magic strings* — `app/components/UI/Perps/utils/orderUtils.ts:586-588` hardcodes English `'Limit'` / `'Market'` where `perps.order.limit` and `perps.order.market` already exist and are translated in 13 locales.
  - *Protocol abstraction ("provider differences must be normalized in the aggregation layer, not leaked to the view")* — `orderUtils.ts:587` renders raw `order.detailedOrderType` straight into the pill.
  - *Agentic testability (testIDs)* — `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderCard.tsx:207-209`: the `Tag` the PR modified has no `testID`, so the pill string cannot be asserted by a recipe (confirmed live).

## Fix Quality

- **Best approach:** For claims 1 and 3, yes — both are minimal one-line key/value corrections and I would ship them as-is. For claim 2 the *approach* (one shared type-only helper) is right, but the *implementation* is not the best fix. The old `getOrderTypeLabel` normalized provider strings into i18n keys; the new helper drops that normalization entirely.
  - **Pragmatic fix for this PR:** keep the helper, but return `strings('perps.order.limit')` / `strings('perps.order.market')` for the fallback branch instead of English literals. One-line change, removes the 13-locale regression immediately.
  - **Best long-term fix:** map `detailedOrderType` through the canonical `DETAILED_ORDER_TYPES` constants to i18n keys, so the pill is both translated and provider-independent. `Stop Limit` / `Stop Market` / `Take Profit Limit` / `Take Profit Market` are a closed set in `@metamask/perps-controller/constants/orderTypes`, so this is a small exhaustive map, not open-ended work.
- **Would not ship:** `orderUtils.ts:585-591` as written. Concretely: (a) 13 locales (`de, el, es, fr, hi, id, ja, ko, pt, ru, tr, vi, zh`) translate `perps.order.market`/`limit` — the pill now shows English in all of them, where the removed code showed the translation; (b) the MYX adapter (`@metamask/perps-controller/utils/myxAdapter.mjs:308-317`) emits `'Take Profit'`, `'Stop Loss'`, `'Liquidation'`, none of which are in `DETAILED_ORDER_TYPES`, so once MYX orders reach this tab the same UI will read `Stop loss` next to HyperLiquid's `Stop market`. The removed `getOrderTypeLabel` normalized both to `Stop`. Impact is bounded (a display pill, English build unaffected, MYX is feature-flagged), so this is a fix-before-merge item rather than a correctness bug.
- **Test quality:** Good and genuinely revert-sensitive — I checked each suite against a mental revert. `PerpsProOrderCard.test.tsx:115` expects `Limit` where the old code produced `Open limit`; `PerpsProPositionsSideFilterSheet.test.tsx:13` remaps the mock to `all_sides`, so the old `all_types` key would render the raw key and fail; the `formatOrderTypeLabel` describe block would fail to import on revert. Both the detailed-type path and the absent-detailed-type fallback are covered. Gaps: no test asserts the pill is *localized* (which is why the regression slipped through), and no test covers a MYX-shaped `detailedOrderType`.
- **Brittleness:** The helper renders a provider-controlled string verbatim with no test guarding the mapping, so pill copy silently changes if a provider changes its wording — the data model stays "easy to break again". No import-time-constant or mock-coupling problems. The removal of open/close from the pill loses no information: the card still shows `Reduce only: Yes/No` (`PerpsProOrderCard.tsx:224-233`), verified in the evidence screenshots.

## Live Validation

- **Recipe:** generated — `artifacts/recipe.json` (22 nodes, `generate-ui`)
- **Result:** **PASS** — 22/22 nodes passed per `artifacts/recipe-run/trace.json`; 0 failed. Per-claim breakdown in the coverage table above. Three earlier runs also passed their nodes but framed the claim-2 `Limit` pill off-screen; the recipe was fixed and re-run rather than reported as proven.
- **Video:** `artifacts/evidence/review.mp4` (moov atom verified) — records the passing recipe execution end to end
- **Native changes:** none — no rebuild required
- **Metro errors:** none attributable to this PR. Log scan shows only pre-existing environment noise: HyperLiquid WebSocket reconnects, `circuit breaker is open`, and a `registerMYXProvider` `TypeError: Cannot read property 'prototype' of undefined`. No entry references `orderUtils`, `PerpsProOrderCard`, `proPositionSideFilter`, or `formatOrderTypeLabel`.
- **Log monitoring:** monitored across all four live runs (~10 min of app runtime) plus a targeted scan of `temp/recipe/runtime/metro.log` and the runner's `diagnostics.json` (10 distinct warning/error events, all matching the pre-existing categories above).

## Correctness

- **Diff vs stated goal:** Aligned — all three stated corrections are implemented and verified on device.
- **Edge cases:**
  - Covered: `detailedOrderType` present; absent with `orderType: 'limit'`; absent with `orderType: 'market'`.
  - Uncovered: non-English locales (regression, see Fix Quality); MYX-shaped `detailedOrderType` values (`'Stop Loss'`, `'Liquidation'`); `capitalize` lower-cases everything after the first character, so any acronym a provider returns would be mangled — pre-existing behaviour inherited from `formatOrderLabel`, not introduced here.
  - Checked and clear: the `Size (USD)` label is static while the size-unit toggle exists, but `onSizeUnitPress` is never wired by any parent (`PerpsProOrderForm.tsx:493`), so the toggle is disabled and the label is unconditionally accurate today. Not a defect in this PR.
- **Race conditions:** None — synchronous pure formatting.
- **Backward compatibility:** Preserved for the English build. `getOrderTypeLabel` was file-local, so its removal cannot break external callers; `isClosingOrder` is correctly dropped from the imports with no stale reference left behind.

## Static Analysis

- **lint:tsc:** PASS — `npx tsc --noEmit --project ./tsconfig.json` produced zero errors.
- **Tests:** 107/107 pass across the 3 affected suites (`orderUtils.test.ts`, `PerpsProOrderCard.test.tsx`, `PerpsProPositionsSideFilterSheet.test.tsx`), run both standalone and inside the recipe.
- **Stale-string sweep:** no remaining `Size USD` / `All types` / `Open limit` / `Close limit` references in `app/` (only an unrelated comment in `SocialLeaderboard/components/Filters/TypeFilter.tsx:53`).
- **Orphaned locale keys:** `perps.pro_positions_panel.order_card.{take_profit,stop,open_limit,close_limit}` and `perps.pro_positions_panel.side_filter.all_types` now have zero references in `app/`. This PR orphaned them and should remove them.

## Architecture & Domain

The move of type-label formatting from a view-local helper into `orderUtils.ts` is the right layering — it is the same place `formatOrderLabel` lives, and the two now share identical type-resolution logic (`orderUtils.ts:566-567` and `585-588`), which is worth extracting into one internal `resolveOrderTypeString(order)`.

The domain concern is provider portability. Perps routes all provider access through `AggregatedPerpsProvider`, and the anti-pattern doc is explicit that provider differences must be normalized in the aggregation layer rather than leaked to the view. `formatOrderTypeLabel` is a view-layer helper that renders a provider-native string verbatim, so the Pro Orders tab's copy is now a function of whichever provider served the order. With HyperLiquid alone this is invisible (its `detailedOrderType` values are exactly `DETAILED_ORDER_TYPES`); with MYX enabled it is not.

File-size guardrail: every source file touched is well within limits (largest is `orderUtils.test.ts` at 1,395 lines, +49 from this PR). `locales/languages/en.json` is 10,707 lines, over the 2,500 hard limit, but it is the repo-wide i18n bundle consumed by the translation pipeline — splitting it is out of scope for a copy PR and is not a defect this PR introduced, so it is reported as informational and **not** as a merge blocker.

## Risk Assessment

**LOW** — string and display-label changes only; no trading, auth, ordering, or data logic touched. All three claims verified on a live device with a passing 22-node recipe, type checking is clean, and 107 unit tests pass. The residual risk is cosmetic and bounded: untranslated pill copy in 13 non-English locales, and future provider-dependent pill wording once MYX orders surface here.

## Recommended Action

**COMMENT** — approve-with-follow-up. All three claimed fixes work and are proven on device; nothing here blocks the copy corrections themselves. Before merge, please address the one substantive item:

1. **`app/components/UI/Perps/utils/orderUtils.ts:585-591`** (`must_fix`) — route the fallback through `strings('perps.order.limit')` / `strings('perps.order.market')` and normalize `detailedOrderType` via `DETAILED_ORDER_TYPES` instead of rendering provider text verbatim. Restores translation in 13 locales and keeps pill copy provider-independent.

Non-blocking follow-ups:

2. **`locales/languages/en.json:1524`** (`suggestion`) — remove the five locale keys this PR orphaned.
3. **`app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderCard.tsx:207`** (`suggestion`) — add a `testID` from `Perps.testIds.ts` to the order-type `Tag`; without it the pill string cannot be asserted agentically.
4. **`app/components/UI/Perps/utils/orderUtils.ts:586`** (`nitpick`) — extract the type-resolution expression shared with `formatOrderLabel:566-567`.
