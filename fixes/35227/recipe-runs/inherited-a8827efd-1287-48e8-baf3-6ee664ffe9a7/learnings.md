- Empty full-bleed `accessible` hosts for recipes are a11y bugs, not proof. Assert chart props (`tpslLines.limitOrders`) and keep the still as visual proof.
- Two autoscale tricks on one price scale fight: keep `autoscaleInfoProvider`, drop the phantom LineSeries.
- `detailedOrderType.includes('limit')` is HyperLiquid-only. `getTriggerExecution === 'limit'` also picks up scale/chase and does not depend on MYX copy.
- Hidden price-line snapshots (`originalPriceLineData`) must not keep stretching the scale after hide.
- Limit lines off the visible 15m range look like a missing overlay. Place with a small `offset_pct` (about -1) so the still can prove the line.
- `perps-chart-limit-overlay` is an empty host. Fiber `present` is not enough; the screenshot has to show the WebView Limit line.
- Expanding the Pro chart with a nested toggle call can hit SANDBOX_BUSY. Waiting for `perps-pro-market-chart-panel` is safer when persist already left the chart open.
- Lightweight autoscale must include Limit prices or far offsets clip the line even when the overlay host mounts.
- `chartLogicString.ts` is eslint-ignored. Passing it in a changed-file eslint list trips `--max-warnings=0` without a real source error.

## Static review pass (rev-claude)

- Two autoscale mechanisms were added for the same requirement: `autoscaleInfoProvider` on the candlestick series and a hidden transparent `limitScaleSeries`. Each alone solves the clipping; keeping both compounds padding and injects synthetic datapoints into crosshair/visible-range logic. When a fix lands in two iterations, check whether the first attempt was actually removed.
- Adding an empty `accessible` Box purely so a recipe can assert `present` trades a real a11y regression for a weak proof — a screen reader announces a contentless label over the whole chart. The `recipe-quality.json` WARN already conceded the assertion proves only that a React host mounted. Assert on the existing props spy instead of inventing a DOM node.
- `detailedOrderType` is provider-native: `DETAILED_ORDER_TYPES` is HyperLiquid-only and `myxAdapter` emits only `Take Profit` / `Stop Loss` / `Liquidation`. A `.includes('limit')` match silently no-ops on MYX. The controller already exports `isLimitExecutionOrderType` and `getTriggerExecution`, and the latter also covers `scale` and `chase` resting limits that an `=== 'limit'` check misses.
- Guard accretion is a smell worth tracing: `mapTpslToPositionLines` ended up with three overlapping early returns, the last of which is provably unreachable, plus a removed invariant that previously kept TP/SL/liq from drawing without an entry line.
- `mm-harness run` without `--library perps=...` fails as `workflow.unresolved_call_ref` for `perps.ensure-session` even when a prior recipe-run already resolved that library. Pass the same source as `recipe-run/summary.json`.

## Full self-review pass (rev-claude, post-fix)

- Every blocker from the earlier static-only pass was fixed at the root rather than papered over: the duplicate `limitScaleSeries` deleted outright, `mapTpslToPositionLines` collapsed to one guard with TP/SL/liq nested inside the finite-entry branch, and the recipe's fake overlay assertion replaced with a real chart-content wait plus screenshot. Nesting the TP/SL block was a better fix than the flat guard the review suggested.
- Deleting scaffolding leaves debris one level up. Removing the overlay `Box` orphaned `LIMIT_OVERLAY` in `Perps.testIds.ts` — a dead testID constant that greps clean everywhere except its own declaration. When a review says "delete the element", also check the constant, the recipe node, and the test that referenced it.
- Artifact sidecars go stale independently. `recipe-coverage.md` was regenerated after the recipe rewrite but `recipe-quality.json` was not, so a two-hour-old WARN still described a deleted node and a node count that no longer matched. `TASK_ARTIFACT_CONTRACT_PASS` does not catch this — the gate checks presence and schema, not whether the sidecar describes the current recipe.
- The eslint gate exits non-zero on a file that is correctly `.eslintignore`d: the generated `chartLogicString.ts` emits a "File ignored" *warning* which `--max-warnings=0` promotes to failure. Excluding it from the changed-file list is the right read, but the raw gate command as written in the checklist will always fail on any diff touching the generated webview bundle.
- A WebView canvas cannot be asserted through the fiber tree. The honest split is state-proof via `assert_orders` plus visual-proof via screenshot; an `expected: present` wait on an empty React host looks like proof but only confirms a Box mounted.

## Self-review fix (orphaned testID + stale quality sidecar)

- After deleting a host element, grep the testID string across app, tests, and recipe. The orphaned `LIMIT_OVERLAY` constant would have sent a later recipe at a node that no longer exists.
- `recipe-quality.json` is not rebuilt when `recipe.json` changes. The coverage markdown can be current while the quality sidecar still describes a deleted wait node. Rebuild it with `mm-harness recipe-quality build` from a fresh `recipe-quality-input.json`.
- `mm-harness run` from this worker slot still needs `--library perps=/Users/deeeed/dev/metamask/experimental-metamask-recipe-perps` or `perps.ensure-session` fails as `workflow.unresolved_call_ref`.

## Fix re-review pass (rev-claude, loop 3)

- A one-line deletion is the cheapest possible fix and also the easiest to verify: `git diff origin/main...HEAD` on `Perps.testIds.ts` went fully empty, proving the constant was added and removed within the branch with no collateral edits. An empty diff against the base is stronger evidence than a passing grep.
- Regenerated artifact sidecars need verifying against the thing they describe, not just their own verdict field. `recipe-quality.json` flipped WARN→PASS, but the check that mattered was `jq '.workflow.nodes|length'` returning the 14 it claimed. A grep for the old node name still hit — on the sentence stating that node was removed, which is a correct negative reference rather than staleness.
- When a fix delta has zero added lines, whole checklist sections (test quality, anti-patterns, brittleness) have no surface to evaluate. Saying so explicitly beats re-running the prior pass's analysis and re-reporting it as if it were new work.
- Byte-identical evidence does not need re-reading. Confirming the PNG mtime predated both fix commits was enough to carry forward the earlier visual verification rather than spending a second image read on an unchanged file.

## Static self-review (rev-codex)

- Removing a price-line object and removing its autoscale input are one lifecycle operation. Clearing only the visible object leaves a chart that looks clean but still scales around canceled data.
- If a cache is written before `clearLimitOrderLines`, putting the cache reset inside clear will wipe the just-written prices. Set `lastLimitOrderPrices` after the clear, or the next overlay never enters autoscale.
- A screenshot can prove that a Limit line appears. It cannot prove that cancellation removes the line and its scale influence, so the WebView message lifecycle needs a focused add-then-clear test.
- The shared Advanced Chart and legacy TradingView template implement the same overlay through different APIs. Adapter tests alone do not cover either renderer's state cleanup.
- Silent WebView catches are especially costly for canvas features because React tests and fiber inspection cannot see the missing drawing. New line and scale failures need a diagnostic path.

## Fix-only re-review (rev-codex)

- Moving the cache reset into `clearLimitOrderLines` fixes every clear caller, but `updateLimitOrderLines` must clear before it writes the replacement prices.
- A review finding that asks for a code fix and a regression test stays open when only the production code changes. The missing test is part of the finding, not optional follow-up work.
- Embedded WebView code is awkward to test, not exempt from testing. This repository already imports the template factory in `TradingViewChart.incremental.test.tsx`; stronger coverage can execute the emitted lifecycle or extract its state transition into a helper.
- A recipe still cannot prove cancellation cleanup or error reporting. Those paths need focused static tests even when the visible-line screenshot passes.

## Self-review fix (Limit autoscale test coverage)

- A production-only fix does not close a finding that also asked for a revert-sensitive test. `TradingViewChart.incremental.test.tsx` already imports `createTradingViewChartTemplate`; string-slice assertions on the emitted HTML are enough to fail if `lastLimitOrderPrices = []` leaves `clearLimitOrderLines`.
- `mm-harness run` without `--library perps=...` still fails as `workflow.unresolved_call_ref` for `perps.ensure-session`. Pass the library from the last passing `recipe-run/summary.json`.

## Test fix re-review (rev-codex)

- Two `toContain` checks on the same function body do not encode order. `indexOf` + `toBeGreaterThan` is the smallest revert-sensitive assertion for assignment-before-clear.
- `mm-harness run` without `--library perps=...` still fails `workflow.unresolved_call_ref` for `perps.ensure-session`. Use the path from the last passing `recipe-run/summary.json`.

## Order assertion closeout (rev-codex)

- Scoping both indexes to the extracted `updateLimitOrderLines` body keeps the assertion tied to the relevant call and assignment.
- Requiring the assignment index to be greater than the clear index catches the exact assignment-before-clear regression without adding production code.
- Once the continuation delta closes the sole prior finding, a fix-only review should pass without reopening accepted code outside the declared range.
