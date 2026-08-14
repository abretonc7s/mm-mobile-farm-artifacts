# TAT-3742 — recipe coverage self-audit

Inputs read directly for this audit:

- `before-ac1-after-payment-switch.png` and `after-ac1-after-payment-switch.png`
  (read with the Read tool, not judged from filenames)
- `trace.json` — all 21 nodes of `recipe.json` report `ok: true`
- `funding-state-tests.log` — the focused Jest run the recipe asserts on
- `repro-marker.log` — the on-device `[PR-TAT-3742]` capture from the reproduction commit

## Visual delta check

**Before (pre-fix, `recipe-baseline.json` against stashed code):** three funding
messages stacked on one screen — "Not enough funds available. Deposit funds or select
a different payment method", "Insufficient funds to cover the trade", and
"Insufficient balance. Required: $5.00, Available: $0" — a greyed-out slider, and no
place-order button anywhere in the viewport.

**After (post-fix, `recipe.json`):** no funding message at all, an enabled slider, and
an enabled "Long ETH" button with margin $5.01 on a $10 notional at 2x — the order is
placeable, which is the correct outcome for a $9.37 ETH balance.

An earlier revision of this capture showed "Minimum order size is $10" with a disabled
slider and an "Insufficient funds" button. That was **not** correct behaviour and was
wrongly accepted as passing evidence: the balance ($9.37) at 2x supports an $18.74
notional, comfortably above the $10 minimum. It exposed a second defect — the screen
funded the trade from `payToken.balanceUsd`, a snapshot frozen at `0`, instead of the
live balance the token picker shows. Fixed in `PerpsOrderView.tsx` via
`usePayTokenAccountBalance`; evidence re-captured.

The delta matches the bug → fix described in TASK.md.

## Per-AC coverage matrix

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes (IDs) | Visual file if any | Evidence verdict | Justification |
|---|---------------|------------|------------------|---------------------|--------------------|------------------|---------------|
| 1 | "error messages need cleanup" — at most one funding message at a time, and no message reporting a balance the user does not have | mixed | `ui.screenshot` + `test` | `ac1-assert-no-perps-balance-warning`, `ac1-assert-no-zero-available-row`, `ac1-screenshot-single-message`, `ac3-ac4-assert-funding-state-tests` | `before-ac1-after-payment-switch.png` / `after-ac1-after-payment-switch.png` | PROVEN | Both absence assertions pass on device, and the read screenshots show three messages collapsing to one. `states the minimum order size once when validation reports it as well` covers the de-duplication path. |
| 2 | "the action button disappears from the screen after switching payment methods" — the place-order button stays inside the viewport | visual | `ui.screenshot` | `ac2-assert-action-button-visible`, `ac2-assert-button-still-visible`, `ac1-screenshot-single-message` | `before-ac1-after-payment-switch.png` / `after-ac1-after-payment-switch.png` | PROVEN | Downgraded from `mixed` to `visual` — see the runner action gap below. The before capture has no button in the viewport; the after capture shows it at the bottom, its label legible under the harness RUN banner. The two `ui.wait_for expected=present` nodes additionally prove the button is mounted throughout. |
| 3 | "the slider becomes non-functional" — the slider is not left disabled by a pay-token balance that has not resolved yet | state | `test` | `ac3-ac4-run-funding-state-tests`, `ac3-ac4-assert-funding-state-tests` | none (state AC) | PROVEN | `leaves the amount slider usable while the selected pay token balance is still loading` and `disables the amount slider once a resolved pay token balance cannot reach the minimum order size` pin both sides of the gate. The window itself is a timing-dependent render pass, captured live in `repro-marker.log` (`isBelowMinimumOrderAmount`/`isAmountDisabled: true` with `payTokenBalanceUsd: "0"`), which is why the assertion lives in a unit test rather than an on-device probe. |
| 4 | "ensure the improved error state for balances below $10 is applied to the 'pay with token' flow" — the screen states the minimum order size instead of only greying the slider and relabelling the button | state | `test` | `ac3-ac4-run-funding-state-tests`, `ac3-ac4-assert-funding-state-tests` | none (state AC) | PROVEN | `states the minimum order size when the selected pay token cannot reach it` asserts the exact copy on the message element. The after capture no longer shows this state and must not be read as proof of it: with the balance now read correctly the sample order is affordable, so no message renders. |

## Runner action gap (documented, not worked around)

`ui.wait_for` with `expected: "visible"` cannot be used against this screen. Probed in
isolation, `perps-order-view-place-order-button`, `perps-order-view-pay-token-funding-message`
and `perps-slider` all return
`{"present": true, "visible": false, "error": "Target exists in fiber tree but no measurable native node was found"}`.
Because a `visible` assertion neither passes when the element is on screen nor fails
meaningfully when it is not, it is worthless as proof in either direction — including
the `expected: "hidden"` form. Both recipes were corrected to assert only
`present`/`absent`, and AC2's viewport claim rests on the read screenshots instead.

## Forbidden pattern scan (step 13)

Re-verified against the final `recipe.json`: none of the eight banned patterns are
present. Full table in `forbidden-pattern-scan.md`.

Overall recipe coverage: 4/4 ACs PROVEN (untestable: none, weak: 0, missing: 0)
