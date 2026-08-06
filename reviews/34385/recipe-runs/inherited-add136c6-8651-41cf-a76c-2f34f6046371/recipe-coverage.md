# Recipe coverage — TAT-3687

The ticket specifies no acceptance criteria, so the rows below are the task
claims derived from its one-line requirement: *"fix all breaking changes
minimally and validate all the flows in the app via recipe to make sure there
are no regressions."*

Recipe: `artifacts/recipe.json` (13 authored nodes; 207 nodes after the five
called library flows are resolved).

| # | Claim | Proof mode | Primary evidence | Recipe nodes | Verdict | Rationale |
|---|---|---|---|---|---|---|
| C1 | Mobile declares and resolves `@metamask/perps-controller` 11.x | state | `state` — `recipe-run/trace.json` | `assert-declared-version`, `assert-resolved-version` | PROVEN | Asserts the `^11.0.0` range in `package.json` *and* that the installed tree resolves to `11.0.0`, so every later node demonstrably ran against v11 rather than a stale lockfile. |
| C2 | Every v11 breaking change is fixed — the repo type-checks clean | state | `test` — `tsc --noEmit` exit 0 | `typecheck`, `assert-typecheck-clean` | PROVEN | This is the removal test. The bump produced 19 errors across 8 files; reverting any of the six widened signatures, the toast-bucket resolution, or the 14 error-code entries reintroduces them and fails `assert-typecheck-clean`. |
| C3 | The widened `OrderType` / `PerpsErrorCode` adoption is behaviourally correct | state | `test` — Jest exit 0 | `unit-tests`, `assert-unit-tests-pass` | PROVEN | 8 suites. `determineMakerStatus` is asserted for both trigger execution modes; `ERROR_CODE_TO_I18N_KEY` is asserted to cover every code the *installed* controller exports and to resolve to real English copy. |
| C4 | Market-order placement has no regression | state | `state` — `recipe-run/trace.json` | `prove-market-order` (54 resolved nodes) | PROVEN | Drives a real ETH market order with take profit *and* stop loss through the Mobile UI — order form, fee hook, TP/SL route params, order toasts — then asserts the position opened via controller state. Its screenshots are overwritten by C5 (see note), so the binding proof here is `assert-open-position`. |
| C5 | Limit-order placement has no regression | mixed | `state` + `ui.screenshot` — `recipe-run/screenshots/perps-order-form-mobile.png`, `perps-order-result-mobile.png` | `prove-limit-order` (46 resolved nodes) | PROVEN | Places a real ETH limit order at the live Bid preset and asserts it rests as an open order. The form screenshot shows the Limit order type at the recipe's $10 notional, with the limit price and a non-zero fee both populated — the fee hook running on the widened `OrderType`. |
| C6 | Position Auto close (TP/SL update on an open position) has no regression | mixed | `state` + `ui.screenshot` — `recipe-run/screenshots/perps-position-auto-close-mobile.png` | `prove-auto-close` (38 resolved nodes) | PROVEN | Sets take profit and stop loss on an existing position through the Auto close sheet, exercising `updatePositionTPSL` — the method v11 changed most — and asserts the position survives. Screenshot shows take profit at the +25% preset and stop loss at the −10% preset, each with its trigger price and expected profit/loss populated. |
| C7 | Position close has no regression under v11's reduce-only sizing changes | mixed | `state` + `ui.screenshot` — `recipe-run/screenshots/perps-position-close-mobile.png` | `prove-close-position` (30 resolved nodes) | PROVEN | Closes an ETH position through the Mobile UI and asserts it is gone. Directly exercises v11's size-grid rounding and the removed $10-minimum retry. Screenshot shows the 100% Market close with margin, fee and receive amount populated. |
| C8 | Full open → verify → close → clean lifecycle has no regression | state | `state` — `recipe-run/trace.json` | `prove-lifecycle` (20 resolved nodes) | PROVEN | End-to-end controller-driven lifecycle: clean prestate, open, assert open, cancel orders, close, assert closed, teardown. |

**Overall recipe coverage: 8/8 claims PROVEN (untestable: none, weak: 0, missing: 0).**

## Run record — flake disclosure

The recipe was executed five times. Reporting all five, not just the green
ones (runs 1-4 on the original code, run 5 after the self-review fixes):

| Run | Result | Note |
|---|---|---|
| 1 | **207/207 pass**, exit 0 | Full clean pass. |
| 2 | 110/112 fail | `prove-market-order/restore-market` — library teardown asserted "no open orders" 0.8s in, while the two TP/SL trigger orders from the just-filled parent were still live. Passing runs spend ~9.6s in this node. |
| 3 | **207/207 pass**, exit 0 | Full clean pass from cleaned state. |
| 4 | 110/112 fail | `prove-limit-order/assert-open-order` — the limit order filled instead of resting. The library flow's own parameter doc states the Bid/Ask preset "may rest or fill as price moves". |
| 5 | **207/207 pass**, exit 0 | Full clean pass after the self-review fixes (helper swapped for the controller's `getTriggerExecution`). |

Both failures are in **library-flow assertions that depend on live HyperLiquid
testnet state**, they landed in **different** nodes each time, and both were
preceded by the same nodes passing. Neither touches the changed code: run 2's
failure is a teardown-timing assertion and run 4's is a venue fill race. The
three full 207/207 passes are the substantive proof.

Corroborating evidence that cancellation itself is healthy on v11: the two
orphan triggers left by run 2 were cancelled successfully through the
controller's own `cancelOrders` path (`successCount: 2, failureCount: 0`)
before run 3.

## Notes

- C2 and C3 are `state` mode with `test` evidence on purpose. The change is
  almost entirely type-level, so a screenshot cannot prove it — a screenshot of
  an unchanged screen would be evidence of nothing. The compiler and the unit
  suites are the only artifacts that fail when the fix is removed.
- C5–C7 screenshots come from the called library flows and were each opened and
  read, not trusted by filename. They show the real limit order form, the order
  result, the Auto close sheet, and the close-position sheet, with live values
  in every case.
- **These descriptions quote only recipe-controlled inputs** ($10 notional, the
  +25% / −10% presets, the 100% close, the selected order type) and say which
  price/fee fields are populated, rather than quoting the values themselves.
  Every mark-derived figure moves between runs, so a description pinned to one
  run's prices silently stops matching the shipped frames the next time the
  recipe is re-run — which is exactly what happened to an earlier revision of
  this file.
- **`perps-order-result-mobile.png` is the strongest single frame in the set**:
  the "Order submitted" toast is visible with its Long direction and size, and
  that toast is emitted by `PerpsToastOptions.orderManagement[getTriggerExecution(orderForm.type)].submitted(...)`
  — the exact expression this change introduces. It is the one user-visible
  surface the diff touches, and it renders correctly.
- **`prove-market-order` and `prove-limit-order` write to the same two
  screenshot paths**, so the limit run overwrites the market run's captures.
  C4 is therefore graded `state` rather than `mixed`: its proof is the
  `assert-open-position` controller assertion, not a screenshot. Fixing this
  would mean parameterising the filename in the library flow, which is out of
  scope for this ticket.
- No screenshot is claimed for C1, C2, C3 or C8, which assert file, compiler,
  test-runner and controller-state facts with no user-visible surface.
- `after.mp4` (76 MB, valid `moov` atom) records the full passing run end to end
  and covers every flow above.
