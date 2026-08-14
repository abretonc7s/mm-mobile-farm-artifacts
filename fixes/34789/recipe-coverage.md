# PR #34789 (TAT-3742) — recipe coverage, pr-complete re-validation round

This round did **not** author a new recipe. The family's inherited recipe
(`artifacts/recipe.json`, 21 nodes, `RECIPE_SOURCE: family-inherited`) was re-run
unmodified against `branch + origin/main` after the rebase, with the review fix
(`27e68e176f5`) applied. The full per-AC audit from the authoring round stands and is
kept verbatim at `inputs/inherited/recipe-coverage.md`; this file records what changed.

Inputs read directly for this round:

- `artifacts/recipe-run/screenshots/evidence-ac1-after-payment-switch.png` — read with the
  Read tool, not judged from its filename
- `artifacts/recipe-run/summary.json` — `status: pass`, `exitCode: 0`
- `temp/tasks/fix/tat-3742-0813-171821/artifacts/funding-state-tests.log` — the focused Jest
  run the recipe asserts on, **17 passed** this round

## Re-validation result

| # | AC (abbreviated) | Proof mode | Recipe nodes | This round | Note |
|---|------------------|------------|--------------|------------|------|
| 1 | At most one funding message, none reporting a balance the user does not have | mixed | `ac1-assert-no-perps-balance-warning`, `ac1-assert-no-zero-available-row`, `ac1-screenshot-single-message`, `ac3-ac4-assert-funding-state-tests` | PASS | Both absence assertions green post-merge; fresh capture shows a trade screen with no funding message at all. |
| 2 | Place-order button stays inside the viewport | visual | `ac2-assert-action-button-visible`, `ac2-assert-button-still-visible`, `ac1-screenshot-single-message` | PASS | Button present after the switch and once it settles; read capture shows "Long ETH" at the bottom of the viewport. |
| 3 | Slider not left disabled by an unresolved pay-token balance | state | `ac3-ac4-run-funding-state-tests`, `ac3-ac4-assert-funding-state-tests` | PASS | Unchanged; both sides of the gate still pinned by the inherited tests. |
| 4 | Screen states the minimum order size for balances below $10 | state | `ac3-ac4-run-funding-state-tests`, `ac3-ac4-assert-funding-state-tests` | PASS | Unchanged. |

Coverage this round: **4/4 inherited ACs re-PROVEN**, 0 weak, 0 missing.

## Coverage added by this round

The review fix closes a window none of the four ACs named: for ~300 ms
(`PERFORMANCE_CONFIG.ValidationDebounceMs`) after the pay-token balance resolves as too
small, `isPayBalanceLoading` had already dropped while `usePerpsOrderValidation` still
carried the verdict it reached against the Perps balance, leaving the place-order button
tappable for a trade the live token cannot fund.

New coverage lands **inside** the existing AC3/AC4 assertion surface rather than beside it:
the test `disables the place order button while validation still reports the pre-resolution
verdict` sits in the `pay with token funding state` describe block that
`ac3-ac4-run-funding-state-tests` executes and `ac3-ac4-assert-funding-state-tests` gates on
exit code — so the recipe now guards this defect with no node changes. The block went from
16 to 17 passing tests.

Proof mode is `state`, correctly: button disabled-ness during a 300 ms debounce is not
something a screenshot can establish. The gate was verified by reverting the two
`isDisabled` lines and confirming the new test fails, then restoring them.

## Deltas and gaps carried forward

- **Runner action gap (unchanged).** `ui.wait_for expected: "visible"` remains unusable on
  this screen — host nodes report `present: true, visible: false`. Assertions stay on
  `present`/`absent` and AC2's viewport claim still rests on a read screenshot.
- **Flake risk (unchanged, warn).** The screenshot content still tracks the live fixture
  token balance rather than a seeded fixed balance.
- **New finding, not worked around.** The `ac3-ac4-run-funding-state-tests` command node
  writes its log to the *parent* run's directory (`temp/tasks/fix/tat-3742-0813-171821/artifacts/`).
  It resolved here only because that directory still exists in this checkout. A future
  inheritance should rewrite the path to the current `TASK_DIR`; it was left untouched this
  round because step 10 forbids non-mechanical recipe edits on a passing run.
- **Run-level noise.** One `mobile.runtime_recovered` (HUD/CDP transient, absorbed by the
  runner without failing a node) and 15 app warning/error side findings whose relation to
  the task is undetermined — same character as the authoring round.
