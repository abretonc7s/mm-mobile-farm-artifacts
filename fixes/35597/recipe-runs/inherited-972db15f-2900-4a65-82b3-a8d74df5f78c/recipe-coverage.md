# Recipe coverage audit

Recipe: `artifacts/recipe.json` (20 nodes, all `ok: true` in `artifacts/trace.json`).
Baseline: `artifacts/recipe-baseline.json`, run against pre-fix code, exit 0.

## Before / after read directly (visual + mixed ACs only)

| File | What is actually on screen |
|---|---|
| `before-ac1-back-lands-on-order-screen.png` | The **Long BTC** order form ($10, 3x, Market, "Long BTC" CTA) — i.e. Back from the post-order market page reopened the trade screen. |
| `after-ac1-back-lands-on-perps-home.png` | **Perps home** — Perps / HyperLiquid header, $632.68 balance, Withdraw / Add funds, and "Your positions" listing the BTC 3x long that was just opened. |

The delta matches the bug → fix described in the tickets: the same user path now ends on the screen
the trader came from, and the order the recipe placed is visible in the destination's position list
(so the screenshot is the post-order state, not an unrelated home screen).

## Coverage matrix

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes (IDs) | Visual file if any | Evidence verdict | Justification |
|---|---------------|------------|------------------|--------------------|--------------------|------------------|---------------|
| 1 | TAT-3906 / TAT-3838 — "Expected behavior = previous screen (ex: perps home or wallet home or whatever screen you came from in step 1)" | mixed | state | `gate-perps-home`, `setup-open-market`, `setup-clean-market`, `gate-market-page`, `ac1-open-order-form`, `ac1-wait-order-form`, `ac1-place-order`, `ac1-wait-position-open`, `ac1-press-back`, `ac1-assert-order-screen-gone`, `ac1-assert-back-to-perps-home`, `ac1-screenshot-perps-home` | `after-ac1-back-lands-on-perps-home.png` vs `before-ac1-back-lands-on-order-screen.png` | **PROVEN** | The full user path runs through visible controls only (no injected values): Long → Place order → Back. `ac1-assert-order-screen-gone` requires the order form's testID to be **absent** after Back — it is present in the pre-fix baseline run and absent here, which is exactly the popped-vs-pushed difference. `ac1-assert-back-to-perps-home` then requires the Perps home heading, and the screenshot shows that screen carrying the freshly opened BTC position. All 12 nodes are `ok: true` in `trace.json`. |
| 2 | TAT-3874 — "Pressing 'back' should take the user to the previous screen (BTC perps pro screen) instead of back to the add funds screen." | state | test | `ac2-run-navigation-unit-tests`, `ac2-assert-navigation-unit-tests-pass`, `ac2-index-test-log` | none (state AC — no screenshot claimed) | **PROVEN** (code-level) / live device proof **UNTESTABLE** | The Pro add-funds return path is `useNavigateToPerpsHome`, called from `useTransactionConfirm.ts:186` after a `perpsDeposit`. The recipe runs the focused suites in-run (`151 passed`, log at `artifacts/ac2-navigation-unit-tests.log`, exit code asserted `0`), including "pops back to the Pro market instead of stacking a duplicate over the caller". **Live device proof is untestable in this slot**: reaching it needs a confirmed, funded Arbitrum Sepolia deposit — an `external-mutation` action with no funding request/preflight/consent artifacts available here. No screenshot is offered, because a screenshot cannot prove a navigation-stack contract that was never exercised on the device. |

Overall recipe coverage: 2/2 ACs PROVEN (untestable: AC2 live-device evidence only — its code-level claim is proven by test; weak: 0, missing: 0)

## Forbidden-pattern scan (step 13 list)

| # | Pattern | Result |
|---|---|---|
| 1 | `switch` with `default` routing around an AC assertion | none — recipe has no `switch` node |
| 2 | `eval_sync` returning a skip-reason string | none — no `eval_*` nodes at all |
| 3 | `wait` > 500ms substituting for `ui.wait_for` | none — no `wait` nodes; every settle point is a `ui.wait_for` |
| 4 | DOM/fiber-only assertion for a visual claim | none — AC1's visual claim is paired with `ac1-screenshot-perps-home`; AC2 claims no visual proof |
| 5 | Node ID outside `ac<N>-` / `setup-` / `teardown-` / `gate-` | none — verified programmatically over all 20 IDs |
| 6 | Missing screenshot for a visual/mixed AC, or screenshot as sole proof for a state AC | none — AC1 (mixed) has one; AC2 (state) has none |
| 7 | ES6+ syntax in a typed `metamask.*` or `command` node | none — the only `command` node is POSIX shell |
| 8 | UI value injection | none — the order uses the form's own defaults, submitted with `ui.press`. `metamask.perps.start_state` / `teardown_state` only establish and restore fixture state, never a form value. |

## Known measurement limitation

`ui.wait_for expected: "visible"` is unreliable against this app's fixed footers and the Perps home
heading: the accessibility viewport-intersection probe reports `present: true, visible: false` for
controls that are plainly on screen (observed on `perps-market-details-long-button`,
`perps-order-view-place-order-button` and `perps-home-heading`), and `ui.scroll scroll_into_view`
fails on the footer with "No scrollable near testID". Those gates therefore assert `present`, and
the visual claim is carried by the screenshots, which were read directly rather than inferred from
the recipe's pass status.
