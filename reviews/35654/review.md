# PR Review: #35654 — fix(perps): align position list item design

**Tier:** standard

## Summary

Perps list rows on Wallet Home, Perps Home, and Asset Detail used a different layout than Pro. This PR pulls header formatting into `getPerpsPositionHeaderDisplay` and points both `PerpsCard` and `PerpsProPositionCard` at it.

The shared row is now: ticker title, `{n}x Long/Short` tag, `size • USD` subtitle, PnL on the right, ROE under it. Order rows stay on the old `getOrderListDisplay` path. Privacy still masks size, notional, PnL, and ROE, and leaves ticker plus the direction tag visible.

This is the right fix. Duplicating the header math was how Lite and Pro drifted. Unit tests are revert-sensitive. Author screenshots on the PR show Wallet Home, Perps Home, and Pro with the same header. This slot did not run a live recipe (static-code, no runtime capabilities).

Jira TAT-3776 is linked and has no numbered acceptance criteria. Claims below are copied from the PR body.

## Recipe Coverage

Recipe decision: `skip-runtime-offline` (step 4 runtime not live; validation depth static-code; capability catalog empty). No `recipe.json`, no `trace.json`, no `review.mp4`.

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|-----------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "Shows leverage and direction in a success/danger badge beside the ticker." | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 2 | "Displays position size and USD position value together in the subtitle." | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 3 | "Separates unrealized P&L and ROE into the right-side value and subvalue." | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 4 | "Preserves privacy-mode masking and leaves order rows unchanged." | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 5 | "Updates the Appium fallback locator and unit coverage for the new structure." | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 6 | "Then the ticker symbol should be shown as the title" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 7 | "And leverage and direction should be shown in a colored badge beside the title" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 8 | "And the subtitle should show the position size and USD position value" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 9 | "And unrealized P&L should be shown as the right-side value" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 10 | "And ROE percentage should be shown as the right-side subvalue" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 11 | "Then the long position should show a success-colored \"<leverage>x Long\" badge" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 12 | "And the short position should show a danger-colored \"<leverage>x Short\" badge" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 13 | "And positive P&L and ROE should use the success color" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 14 | "And negative P&L and ROE should use the danger color" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 15 | "Then the ticker symbol and leverage direction badge should remain visible" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 16 | "And the position size and USD position value should be masked" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |
| 17 | "And unrealized P&L and ROE should be masked" | both | none | none | UNTESTABLE | standard-tier skip — runtime-offline / static-code |

Overall recipe coverage: 0/17 ACs PROVEN (untestable: 1-17, weak: 0, missing: 0)

Untestable: 1-17 — standard-tier skip — runtime-offline / static-code. No live recipe in this slot.

Author PR screenshots (not recipe evidence) show claims 1-3, 6-10, 12, 14 on Wallet Home, Perps Home, and Pro for a short ETH row. Missing from those shots: Asset Detail, a long badge, privacy mode.

## Prior Reviews

No prior reviews.

Bot comments only: CLA, flaky-test detector, Codecov (patch 77.8%, 2 lines missed), smart E2E selection, Sonar QG passed, Android perf tests passed.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Shows leverage and direction in a success/danger badge beside the ticker. | PASS | `PerpsCard.tsx` `titleEndAccessory` Tag; helper `directionLabel`/`directionSeverity`; PerpsCard + helper tests; author shots |
| 2 | Displays position size and USD position value together in the subtitle. | PASS | helper `description`; tests `1.5 ETH • $4,350`; author shots `0.00442 ETH • $10.02` |
| 3 | Separates unrealized P&L and ROE into the right-side value and subvalue. | PASS | `pnlText` / `roeText` mapped to ListItem value/subvalue; tests split `+$150.00` and `+10.3%` |
| 4 | Preserves privacy-mode masking and leaves order rows unchanged. | PASS | position `SensitiveText` + order `getOrderListDisplay` unchanged; privacy + order tests |
| 5 | Updates the Appium fallback locator and unit coverage for the new structure. | PASS | `PerpsView.ts` `*-direction-tag`; 48 passing tests in 3 suites |
| 6 | Then the ticker symbol should be shown as the title | PASS | title is `displaySymbol`; tests `ETH`; author shots |
| 7 | And leverage and direction should be shown in a colored badge beside the title | PASS | Tag beside title; tests `3x Long`/`3x Short` + `*-direction-tag` |
| 8 | And the subtitle should show the position size and USD position value | PASS | same as #2 |
| 9 | And unrealized P&L should be shown as the right-side value | PASS | same as #3 |
| 10 | And ROE percentage should be shown as the right-side subvalue | PASS | same as #3 |
| 11 | Then the long position should show a success-colored "`<leverage>`x Long" badge | PASS | helper test `TagSeverity.Success` + `3x Long`; no author long screenshot |
| 12 | And the short position should show a danger-colored "`<leverage>`x Short" badge | PASS | helper `TagSeverity.Danger`; author shots show maroon `3x Short` |
| 13 | And positive P&L and ROE should use the success color | PASS | `pnlColor` from `pnl >= 0`; Perps Home author shot `+$0.01` / `+0.2%` green. PerpsCard tests named "color" only assert text |
| 14 | And negative P&L and ROE should use the danger color | PASS | helper `TextColor.ErrorDefault`; Wallet Home / Pro author shots red `-$0.00` / `-0.1%` |
| 15 | Then the ticker symbol and leverage direction badge should remain visible | PASS | privacy tests: `ETH` and `3x Long` still on screen |
| 16 | And the position size and USD position value should be masked | PASS | privacy tests hide `1.5 ETH • $4,350` |
| 17 | And unrealized P&L and ROE should be masked | PASS | privacy tests hide `+$150.00` and `+10.3%`; >=3 short-dot nodes |

## Code Quality

- Pattern adherence: matches Perps lite/pro split (shared helper, not a copied card). `titleEndAccessory` is the ListItem API other rows already use.
- Complexity: appropriate. Helper is 64 lines.
- Type safety: tsc --noEmit exit 0. No `any`.
- Error handling: invalid ROE becomes `0` then `+0.0%` via `parseFloat(...) || 0`. Domain pattern prefers `PERPS_CONSTANTS.FallbackPercentageDisplay` (`--%`) when data is missing. Positions that actually exist usually have ROE, so this is not a merge blocker.
- Accessibility/fallbacks: ListItem is a button. Tag has no extra a11y props; "3x Long" is nested text and should fold into the row name. Invalid ROE fallback is `+0.0%`, not `--%`. Privacy path is correct.
- Anti-pattern findings:
  - `positionDisplay.ts:46` defaults missing ROE to 0% (see Fix Quality).
  - `PerpsCard.tsx:223` builds `*-direction-tag` inline instead of a `Perps.testIds.ts` helper.
  - `perps.market.long_lowercase` / `short_lowercase` are unused in app code after this PR (locale keys still in `locales/languages/*.json`).

## Fix Quality

- **Best approach:** shared formatter is the long-term fix and the pragmatic one. Reusing the whole Pro card on Wallet Home would drag in actions and key figures the list does not want.
- **Would not ship:** none.
- **Test quality:** layout assertions would fail if this PR were reverted (`ETH 3x long` vs `ETH` + `3x Long`). Zero-size short and NaN ROE are covered. PerpsCard tests titled "displays correct PnL color" only check the formatted strings, not `TagSeverity` or `TextColor`. The helper tests do check severity and color.
- **Brittleness:** helper contract is ROE as a decimal ratio (`0.103` → `+10.3%`). This PR corrects `defaultPerpsPositionMock`. Other Perps fixtures still use `'10'` as if it were already a percent. Those files do not call this helper. Zero-size positions render as Short (`size > 0`). Old Pro used `size >= 0` (zero was Long). The new rule is tested.

## Live Validation

- Recipe: skipped (tier: standard, `skip-runtime-offline`)
- Result: SKIPPED. No recipe nodes executed.
- Video: skipped (static-code)
- Native changes: none
- Metro errors: stale `metro.log` from 2026-08-19 (Android bundle + pre-existing package export warnings). Not from this PR.
- Log monitoring: skipped (static-code). Inspected existing log only.

## Correctness

- Diff vs stated goal: aligned. Wallet Home (`PerpsSectionMain`), Perps Home (`PerpsHomeView`), and Asset Detail (`AssetOverviewContent`) all render `PerpsCard`.
- Edge cases: zero-size → Short (tested). NaN ROE → `+0.0%` (tested). PnL and ROE share `pnlColor`, so a sign split between the two would paint ROE with the PnL color. Unlikely for a live position.
- Race conditions: none. Pure display.
- Backward compatibility: Appium `expectPositionRowAfterLimitOrderFilled` now looks for `*-direction-tag` and the word `Long`/`Short`. Order locators unchanged.

## Static Analysis

- lint:tsc: PASS
- Tests: 48/48 pass (`positionDisplay.test.ts`, `PerpsCard.test.tsx`, `PerpsProPositionCard.test.tsx`)

## Architecture & Domain

Right layer: UI display helper, not controller. Lite and Pro cannot drift on header math unless someone bypasses the helper. No WS, no order params, no provider branching.

## Risk Assessment

- LOW — UI formatting, shared display helper, tests and Appium locators updated. No auth, payments, or persistence.

The `risk:high` label on the PR does not match this diff.

## Recommended Action

APPROVE

Optional follow-ups (non-blocking):

1. `positionDisplay.ts:46` — use `FallbackPercentageDisplay` when ROE is non-numeric.
2. Centralize the `-direction-tag` suffix in `Perps.testIds.ts`.
3. Assert Tag severity / PnL `TextColor` in `PerpsCard` tests, or rename the tests that claim they check color.
4. Human glance at Asset Detail, a long row, and privacy mode. Author shots cover short rows on Wallet Home, Perps Home, and Pro only.
