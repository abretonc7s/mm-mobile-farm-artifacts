# Recipe coverage — TAT-3932 / PR #36415 (pr-complete re-validation)

Recipe: `artifacts/recipe.json` — "Aggregated control switches the Perps trade list between one row per order and every fill"
Run: `artifacts/recipe-run/report.md` — status **pass**, 18/18 nodes, 51s, on the branch rebased onto `origin/main` (`3bf04be0e1`) **with this round's review fixes applied** (`a8bbe15e6f`).

| AC | Claim | Proof mode | Nodes | Result |
|----|-------|-----------|-------|--------|
| AC1 | One order's fills are summed into a single row when aggregation is on, and listed separately when it is off | state | `ac1-run-transform-tests` → `ac1-assert-transform-tests` → `ac1-index-test-log` | pass |
| AC2 | The Aggregated control is offered on Activity > Perps > Trades and switches the live list between one row per order and one row per execution | visual | `setup-nav-perps-root` → `setup-open-type-filter` → `setup-wait-type-sheet` → `setup-choose-perps` → `gate-perps-trades` → `ac1-wait-control` → `ac2-wait-rows` → `ac2-screenshot-aggregated` → `ac2-press-control` → `ac2-wait-after-toggle` → `ac2-screenshot-individual` | pass |

Tests executed by the run (`temp/tat-3932/artifacts/transform-tests.log`, 9 passed / 0 failed):

- `lists every execution separately when aggregation is turned off`
- `aggregates fills within the same second`
- `aggregates one close order filled across several seconds`
- `aggregates split stop loss fills into single fill with combined PnL`
- `aggregates split take profit fills into single fill`
- `does not aggregate fills with different assets`
- `does not aggregate fills with different close directions`
- `does not aggregate fills in different seconds from different orders`
- `links same-second and same-order groups into one entry`

## This round's review fixes — proof mapping

| Fix | Covered by the recipe? | Proof |
|-----|------------------------|-------|
| Design-system `Checkbox` replaces `ButtonBase` | yes | `ac1-wait-control` still matches `activity-screen-aggregated-checkbox`, `ac2-press-control` still toggles it, and both screenshots show the pill rendering correctly checked and unchecked |
| Toggle still re-renders from cache into per-fill rows | yes | `ac2-wait-after-toggle` matches `transaction-item-12`, a row index that only exists once the order's fills are listed individually; the screenshots show 0.00179 → 0.00163 + 0.00016 and 0.00128 → 0.00125 + 0.00003 |
| `flattenFills` dedupe removed | no — unit-level | `usePerpsActivityQuery.test.ts` 'keeps both executions when two fills of one order share timestamp, size and price', verified to fail with the dedupe restored. The fixture account's testnet history holds no two fills identical in all four values, so the live list cannot discriminate this |
| Content-derived individual row ids | partially | The recipe proves the ids still resolve the rendered list; id stability under a prepended fill is proven by `transactionTransforms.test.ts` 'leaves existing execution ids unchanged when a newer fill is prepended', which fails on the old `acc.length` scheme |
| `{ fillDisplay }` options object | no — refactor | Type-level change with no runtime behaviour; covered by `yarn lint:tsc` plus the updated call-site assertions in `usePerpsActivityItems.test.ts` and `usePerpsDetailsItem.test.ts` |

## Notes

- Provenance: `RECIPE_SOURCE=pr-body-llm`, staged as `pr-body-llm-extracted-untrusted`. Reviewed under the task trust gate before promotion — a single `command` node running `yarn jest` on a repo test file into `temp/tat-3932/artifacts/`, everything else `ui.*` / `app.*` / `assert_exit_code` / `index_artifacts`. No env probing, credential access, writes outside the repo, or non-MetaMask hosts. Recipe executed unmodified; no migration was needed.
- The harness's own `launch --verify` smoke recipes were blocked by `RECIPE_TRUST_REQUIRED` on bundled actions in this slot. `mm-harness doctor --expect-live` passed (runtime ready, `mm-1` booted, fixture READY), and the recipe ran with the reviewed plan digest approved.
- Two discarded attempts preceded the pass: a flaky wallet unlock (`keyringUnlocked: true`, route stuck on `Login`) and a 60s Metro bundle timeout while Metro rebundled the edited files. Neither touches code in this branch; the run passed once the bundle warmed.
- Account state: the recipe needs trade *history* with multi-fill orders on the fixture account (`0x316b…01fa`, Hyperliquid testnet), not live positions. Nothing was converged, closed, or cancelled.
- 109 application warning/error events were recorded as non-blocking side findings, consistent with the 111 seen on the original run; not investigated, stored in `artifacts/recipe-run/diagnostics.json`.
