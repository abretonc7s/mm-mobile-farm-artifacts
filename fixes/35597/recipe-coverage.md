# Recipe coverage — pr-complete re-validation of PR #35597

Recipe: `artifacts/recipe.json`, inherited unchanged from the family run (`diff -q` clean, 20 nodes).
Run: `artifacts/recipe-run/trace.json`, **exit 0, 20/20 nodes `ok: true`**, executed against the
branch rebased onto `origin/main@9128899f301`. This re-validation therefore covers the merge as well
as the branch's own two-line change.

## Visual evidence read for this run

`artifacts/after-ac1-back-lands-on-perps-home.png` (captured 19:41 by this run, promoted from
`recipe-run/screenshots/`) was read directly rather than trusted by filename. It shows **Perps home**
— Perps / HyperLiquid header, $632.54 balance, Withdraw / Add funds — with "Your positions" listing
the **BTC 3x long ($10.02, 0.00013 BTC)** that this run's recipe had just opened. That the freshly
placed position appears in the destination is what makes it the post-order state rather than an
unrelated home screen.

The pre-fix counterpart, `before-ac1-back-lands-on-order-screen.png`, shows the Long BTC order form
($10, 3x, Market) reached by the identical Back press on pre-fix code.

## Coverage matrix

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes | Visual file | Verdict | Justification |
|---|---|---|---|---|---|---|---|
| 1 | TAT-3906 / TAT-3838 — "Expected behavior = previous screen (ex: perps home or wallet home or whatever screen you came from in step 1)" | mixed | state | `gate-perps-home`, `setup-open-market`, `setup-clean-market`, `gate-market-page`, `ac1-open-order-form`, `ac1-wait-order-form`, `ac1-place-order`, `ac1-wait-position-open`, `ac1-press-back`, `ac1-assert-order-screen-gone`, `ac1-assert-back-to-perps-home`, `ac1-screenshot-perps-home` | `after-ac1-back-lands-on-perps-home.png` vs `before-ac1-back-lands-on-order-screen.png` | **PROVEN** | The whole path runs through visible controls, no injected values. `ac1-assert-order-screen-gone` requires the order form's testID to be **absent** after Back; it is present in the pre-fix baseline run and absent here, which is exactly the popped-vs-pushed difference. All 12 nodes `ok: true` in this run's trace. |
| 2 | TAT-3874 — "Pressing 'back' should take the user to the previous screen (BTC perps pro screen) instead of back to the add funds screen." | state | test | `ac2-run-navigation-unit-tests`, `ac2-assert-navigation-unit-tests-pass`, `ac2-index-test-log` | none (state AC) | **PROVEN** (code-level); live device proof **UNTESTABLE** | The recipe runs the focused suites in-run with the exit code asserted `0`, including "pops back to the Pro market instead of stacking a duplicate over the caller". Live device proof needs a confirmed, funded Arbitrum Sepolia deposit, an `external-mutation` with no funding request/preflight/consent artifacts in this slot, so no manifest-declared action can establish it. No screenshot is offered, because a screenshot cannot prove a navigation-stack contract that was never exercised on device. |

Overall recipe coverage: 2/2 ACs PROVEN (untestable: AC2 live-device evidence only — its code-level claim is proven by test; weak: 0, missing: 0)

## Supporting validation on the same rebased tree

- `PerpsOrderView.test.tsx` + `perpsModeSwitch.test.ts` + `useTransactionConfirm.test.ts`: 200 passed.
- Scoped ESLint on the 5 changed files: 0 errors (7 pre-existing warnings, unchanged from `main`).
- Prettier: clean. Language-server diagnostics on both changed source files: no errors.

## Known measurement limitation (carried from the family run)

`ui.wait_for expected: "visible"` is unreliable against this app's fixed footers and the Perps home
heading, reporting `present: true, visible: false` for controls plainly on screen, and
`ui.scroll scroll_into_view` fails on the footer with "No scrollable near testID". Those gates assert
`present`; the visual claim is carried by the screenshot, which was read directly.
