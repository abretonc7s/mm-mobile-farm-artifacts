# Recipe coverage

| AC | Claim | Proof | Primary evidence | Nodes | Verdict | Rationale |
|----|--------|-------|------------------|-------|---------|-----------|
| AC1 | Scale long farthest endpoint >5% below bid warns | state | recipe-run/report.md | run-helper-tests, run-hook-tests | PROVEN | Helper covers the distance/endpoint maths; hook test `pushes the far-from-market notice for a long ladder resting below the bid` proves the banner reaches `notices`. |
| AC2 | Scale short farthest endpoint >5% above ask warns | state | recipe-run/report.md | run-helper-tests | PROVEN | Short scale high-endpoint case in helper tests. |
| AC3 | Limit far below bid warns | state | recipe-run/report.md | run-helper-tests, run-hook-tests | PROVEN | Helper long-limit case plus the hook's limit price-card fallback test. |
| AC4 | Exactly 5% does not warn | state | recipe-run/report.md | run-helper-tests, run-hook-tests | PROVEN | Helper threshold-equality case; hook test `stays quiet for a ladder resting inside the threshold`. |
| AC5 | Reduce-only skips warning | state | recipe-run/report.md | run-helper-tests | PROVEN | `reduceOnly: true` returns undefined. |
| AC6 | Place stays enabled (warning is non-blocking) | state | recipe-run/report.md | run-hook-tests, wait-place | PROVEN | Hook test `never disables Place for a far-from-market ladder` asserts the notice is present **and** `isPlaceOrderDisabled === false`. The recipe's `wait-place` additionally proves the control is mounted on a live Scale form. |

PR-complete follow-up: hook suite now also covers the scale blur gate (`stays quiet while a scale start price is still being typed`, `hides the warning when a finished scale price is edited again`). Those tests run under the same `-t 'far-from-market'` node. Re-validation recipe-run status: pass.

Overall recipe coverage: 6/6 ACs PROVEN by state (visual: 0 — see below)

## Visual proof: not captured (honest downgrade)

`after-scale-form.png` shows the **live Pro Scale form** — order type Scale, Start (USD) and
End (USD) fields present — reached by the recipe through
`ui.press` order-type → advanced tab → Scale. It does **not** show the warning banner.

The banner needs a price typed into a scale field, and text entry into those fields is not
reachable from this adapter: `ui.set_input` fails with an opaque
`RECIPE_VALIDATION_FAILED` on every documented arg shape (including the exact form its own
`userAction` prescribes), and `ui.key_press` reaches a focused field with the numeric keypad
visible but commits no value. AC6 is therefore proven by **state, not pixels**.

### Correction to the previous coverage note

The earlier note claimed `ui.press` on the order-type control does not open the sheet. That is
false and was re-tested this pass: the sheet opens reliably and Scale is selectable. The prior
screenshot showed a default Market form only because the recipe never pressed through to Scale.
The real boundary is text entry, not sheet navigation.
