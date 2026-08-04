# Recipe Coverage — PR #34267

**Recipe decision:** `generate-ui`
**Recipe:** `artifacts/recipe.json` (22 nodes)
**Trace:** `artifacts/recipe-run/trace.json` — **22/22 nodes passed**, 0 failed
**Source of claims:** PR body claims (no numbered Jira / linked-issue acceptance criteria)
**Target platform:** both — copy/i18n changes render identically on iOS and Android; no platform-specific code in the diff. Slot ran **ios** (`mmdev-1`), which is sufficient.

## Coverage matrix

| # | Claim (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|------------------|-----------------|--------------------|---------------------|----------------|---------------|
| 1 | "Then the label reads \"Size (USD)\"" | both (ran ios) | `gate-pro-view`, `ac1-assert-size-label`, `ac1-screenshot-size-label` | `evidence-ac1-size-usd-label.png` | **PROVEN** | Typed assertion `ui.wait_for test_id=perps-pro-order-form-size-input text="Size (USD)"` passed on the live Pro order form. Revert-sensitive: the pre-PR string `Size USD` does not contain `Size (USD)`, so the node would fail on revert. The screenshot shows the label rendered as `Size (USD)` above the size input. |
| 2 | "Then limit orders show \"Limit\" and stop market orders show \"Stop market\"" | both (ran ios) | `setup-limit-order`, `ac2-open-orders-tab`, `ac2-assert-orders-list`, `ac2-assert-limit-order-open`, `ac2-screenshot-limit-pill`, `ac2-scroll-to-stop-order`, `ac2-screenshot-stop-market-pill`, `ac2-run-pill-label-tests`, `ac2-assert-pill-label-tests-pass` | `evidence-ac2-order-pill-limit.png` (primary), `evidence-ac2-order-pill-stop-market.png` | **PROVEN** | `evidence-ac2-order-pill-limit.png` proves **both halves in one frame**: the Orders (4) tab shows the SOL order (Reduce only: **No**) with a bare **`Limit`** pill — pre-PR this exact order rendered `Open limit` — and directly below it the ETH trigger order with a **`Stop market`** pill (pre-PR: `Stop`). `evidence-ac2-order-pill-stop-market.png` corroborates with the BTC `Stop market` and ETH `Take profit limit` pills. `metamask.perps.assert_orders market=SOL state=open` independently confirmed the limit order was live, so the pill is not a stale row. Because the `Tag` pill carries **no testID**, no typed text assertion can reach it (verified live: `ui.wait_for` on the order-row testID returns only `"BTC"`); the non-visual half of the proof is `ac2-run-pill-label-tests` → **107/107 jest tests passed, exit 0**, pinning the exact strings `Limit`, `Stop market`, `Take profit limit`. |
| 3 | "Then the first option reads \"All sides\"" | both (ran ios) | `ac3-scroll-to-positions`, `ac3-open-positions-tab`, `ac3-open-side-filter`, `ac3-assert-all-sides`, `ac3-screenshot-side-filter` | `evidence-ac3-all-sides-filter.png` | **PROVEN** | Typed assertion `ui.wait_for test_id=perps-pro-market-positions-side-filter-sheet-option-all text="All sides"` passed. Revert-sensitive: the pre-PR key `all_types` renders `All types`. The screenshot shows the sheet with **All sides** as the first option (checked), above `Long` and `Short`, and additionally shows the collapsed Positions-tab filter button also reading **All sides**, confirming the sheet and button labels are now consistent. |

## Audit notes

- **Image review performed:** all four evidence PNGs were opened and read directly; each manifest `label`/`intent` matches what the pixels demonstrate. HUD was on for every capture (`RUN 6/22`, `11/22`, `16/22`, `18/22` overlays visible), satisfying the observability contract.
- **Iteration history (honest reporting):** the first three live runs all passed 22–23/23 nodes, but the claim-2 `Limit` pill was scrolled out of frame, so claim 2 was graded **WEAK** and the recipe was fixed and re-run rather than reported as proven. Superseded runs and exploratory probe screenshots were deleted; only the final run's AC-bound evidence remains.
- **Evidence pruning:** 4 exploratory `probe-*.png` orphans and 3 superseded run directories removed. Every remaining PNG is AC-bound.
- **Forbidden-pattern scan (step 16):** no `switch`/`default` routing around an assertion, no `eval_sync`, no `wait` used as a substitute for `ui.wait_for` (no `wait` nodes at all), no fiber-only assertion for a visual-ordering claim (claim 3 pairs typed state proof with a screenshot), every node ID prefixed `setup-`/`gate-`/`ac<N>-`/`teardown-`, no ES6+ syntax in `command`. Clean.
- **Trace cross-check:** every drafted node has a trace entry (22 drafted / 22 traced / 0 missing); no node failed. Counts reported here are derived from `trace.json`, not from the draft.
- **State hygiene:** the recipe created one SOL testnet limit order as a precondition and cancelled it in `teardown-close-limit-order`; no other live state was mutated.

## Runner gap observed (not an AC failure)

The order-type `Tag` in `PerpsProOrderCard.tsx` has no `testID`, so the runner cannot assert the pill text with `ui.wait_for` — `text` validation reads only the node's own shallow text (`"BTC"` for the order row). This forced claim 2 onto screenshot + unit-test proof instead of a typed UI assertion. Reported as a review finding against the PR, since the PR modified that exact element.

Overall recipe coverage: 3/3 ACs PROVEN (untestable: none, weak: 0, missing: 0)
