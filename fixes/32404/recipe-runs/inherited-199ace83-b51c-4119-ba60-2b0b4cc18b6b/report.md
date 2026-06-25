# Report: TAT-3398

## Self-Review Fixes

- `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx:758` — added
  `accessibilityLabel` (`perps.tpsl.toggle_take_profit_sign`) and
  `accessibilityState={{ disabled: inputsDisabled }}` to the Take Profit RoE sign
  badge so a screen reader announces the toggle's purpose and disabled state
  instead of only the bare "+"/"-" glyph.
- `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx:965` — same fix
  on the Stop Loss RoE sign badge (`perps.tpsl.toggle_stop_loss_sign` +
  `accessibilityState`).
- `locales/languages/en.json` — added the two `strings(...)` keys
  (`perps.tpsl.toggle_take_profit_sign`, `perps.tpsl.toggle_stop_loss_sign`)
  backing the new accessibility labels.

Verification: `PerpsTPSLView.test.tsx` — 31/31 passed (includes RoE Sign Badge
render + toggle cases). Trivial a11y-only change; no behavior or logic change.

ESLint (`--max-warnings=0`) on the changed file: 0 errors, 5 warnings — all
pre-existing `@typescript-eslint/no-deprecated` (`ElementRef` at 93–96,
`ButtonIcon` at 555), none in this diff. The original self-review already logged
these as pre-existing/non-blocking. Not fixed here: migrating them is unrelated
scope creep on lines this change never touches.

### Round 2 — Analytics sign recompose

- `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx:439` — confirm
  `trackingData` parsed `formattedTakeProfitPercentage` /
  `formattedStopLossPercentage`, but those display strings are now unsigned
  magnitudes (the badge owns the sign). Recompose the sign from
  `takeProfitSign` / `stopLossSign` so a negative TP reports a negative RoE and a
  gain-side (`+`) SL reports a positive RoE instead of both collapsing to the
  bare magnitude. Added `takeProfitSign`/`stopLossSign` to the `useCallback`
  deps.
- `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.view.test.tsx` —
  added two confirm tests: toggling the TP badge reports
  `takeProfitPercentage: -10`; toggling the SL badge reports
  `stopLossPercentage: 10` (real component + real hook, no mocks).

Verification:
- `PerpsTPSLView.view.test.tsx` — 5/5 passed (incl. the 2 new signed-metadata
  tests).
- `PerpsTPSLView.test.tsx` — 31/31 passed (no regression; empty display →
  `undefined` still holds).
- ESLint `--max-warnings=0` on the two changed files: 0 errors; only the same
  pre-existing deprecation warnings noted above, none on the edited lines.
- Recipe regression (`recipe.json`, mobile adapter): 39/39 PASS
  (`recipe-run-selfreviewfix/`). Analytics-payload-only change — no UI/behavior
  surface for the recipe, confirmed green. Artifact-contract gate
  (`check-task-artifact-contract.mjs`) is orchestrator-owned and absent from this
  checkout, so it is run by the gateway, not this worker slot.

### Round 3 — Direct unit assertion for signed metadata

- `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.test.tsx` — added a
  confirm test (mocked hook) asserting the recompose at `PerpsTPSLView.tsx:439`:
  with `takeProfitSign: '-'` + `formattedTakeProfitPercentage: '10%'` and
  `stopLossSign: '+'` + `formattedStopLossPercentage: '10%'`, `onConfirm`
  receives `takeProfitPercentage: -10` / `stopLossPercentage: 10`. Closes the
  "Test quality: weak" finding (the original `.test.tsx` had no signed-metadata
  confirm assertion; the prior `.view.test.tsx` tests covered it via the real
  hook, this adds the direct unit-level guard on the flagged line).

Verification:
- `PerpsTPSLView.test.tsx` — 32/32 passed (incl. the new signed-metadata test).
- ESLint `--max-warnings=0` on the changed file: 0 errors.
- Test-only diff (no production/runtime change in this round), so the recipe
  regression result above is unaffected; not re-run.
