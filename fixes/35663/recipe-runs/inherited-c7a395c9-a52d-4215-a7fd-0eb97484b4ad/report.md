# TAT-3904 — Scale order spread warning

Warn a trader when the endpoints of a Perps Pro scale (laddered) order sit on the wrong
side of the book. Those rungs fill immediately as taker orders instead of resting, which
defeats the point of laddering. The warning is advisory: placement is never blocked.

## What changed

- `app/components/UI/Perps/utils/triggerOrderValidation.ts` — new exported
  `getScalePriceCrossingWarning`, placed beside the existing `getLimitPriceCrossingWarning`
  it mirrors. Pure function: canonicalizes each endpoint to venue precision, compares it to
  a reference price, and returns localized copy. Counting how many endpoints cross is what
  lets the copy distinguish a partly-affected ladder from one entirely on the wrong side.
- `usePerpsProOrderForm.ts` — three additions:
  - `scaleCrossingReferencePrice`: best ask for a long, best bid for a short, falling back
    to mid when top-of-book has not arrived yet (the same fallback the shipped single-limit
    check uses).
  - A Scale branch in `priceCardMessage`, evaluated *before* the limit-field branches.
    Scale mode has no limit field, so the `hasBlurredLimitPrice` gate must not apply — the
    warning has to show while the trader is still typing, not only after a blur.
  - Submit-time re-check in `onPlaceOrderPress` against the freshest top-of-book, since the
    book can move between the last keystroke and the tap.
- `locales/languages/en.json` — two keys for the partial-impact copy. The full-ladder case
  reuses the existing `limit_price_above/below_warning` strings rather than duplicating them.
- `triggerOrderValidation.test.ts` — 9 cases for the new helper.

## Acceptance criteria

| AC | Status | Proof |
|----|--------|-------|
| 1 — Long crossing best ask warns | PASS | recipe `expect-full-above` + `evidence-ac1-long-full-cross.png` |
| 2 — Short crossing best bid, mirrored copy | PASS | recipe `expect-full-below` + `evidence-ac2-short-full-cross.png` |
| 3 — Partial vs full-ladder copy | PASS | recipe `expect-partial-above` vs `expect-full-above` + `evidence-ac3-partial-cross.png` |
| 4 — Re-evaluates on endpoint/side edit + submit re-validation | PARTIAL | Edit and side-flip proved by recipe (`expect-quiet` → `expect-partial-above` → `expect-full-above`, and `flip-short` → `expect-cleared-on-flip`). The submit-time half is **not** asserted by the recipe — see below. |
| 5 — Non-blocking | PASS | recipe `expect-still-placeable`; all three frames show Place order enabled beside the warning |

### AC 4 caveat

The submit-time re-check is implemented and unit-covered through the helper it calls, but
the recipe does not assert it. It emits a `DevLogger` line rather than changing visible
state, and placing a real order to observe it would mutate account state. Calling this
fully proven would overstate the evidence, so it is recorded as partial. `recipe-quality.json`
carries the suggested delta (a `watch_logs` node read from a captured baseline offset).

## Verification

- `yarn jest triggerOrderValidation.test.ts` — 71 passed
- `yarn jest usePerpsProOrderForm.test.ts` — 271 passed
- ESLint on changed files, `--max-warnings=0` — clean; Prettier reports no changes
- Recipe: 26/26 nodes pass (`artifacts/recipe-run/summary.json`), run with `--hud hide`
- Failing-first: with the implementation stashed and the app restarted onto that source,
  the recipe **fails** at `expect-partial-above`. Removing the implementation breaks the
  recipe, which is the self-test the task requires.

Full-project `tsc` was not run — worker slots are barred from it; that gate belongs to CI.

## Self-Review Fixes

The prior run stopped after recording its approach and shipped nothing; self-review
correctly found an empty diff. Every issue it raised traced to that single cause, so the
fix was to implement the ticket rather than patch seven separate findings.

- `app/components/UI/Perps/utils/triggerOrderValidation.ts:329` — added the missing
  `getScalePriceCrossingWarning` helper (AC 1-3).
- `usePerpsProOrderForm.ts:1311,2403,3466` — added the reference-price memo, the Scale
  branch in `priceCardMessage` ahead of the blur gate, and the submit-time re-check (AC 4).
- `locales/languages/en.json:1748` — added the two partial-impact copy keys (AC 3).
- `triggerOrderValidation.test.ts:302` — added 9 unit cases; the review noted no tests
  existed for the helper.
- `artifacts/recipe.json` — wrote the missing validation recipe and proved it failing-first.
- `artifacts/report.md`, `recipe-coverage.md`, `recipe-quality.json` — added the missing
  artifacts. The review's point that the earlier contract PASS was vacuous was right: it
  passed because nothing existed to check. It now passes with a real recipe and sidecars.

### Note on visual evidence

I initially judged the screenshots the review asked for to be impossible: the warning renders
low in the order form and the recipe HUD covered it. That was wrong, and the correction found
real defects.

`mm-harness run --hud hide` suppresses the overlay for the whole run, and `ui.capture_surface`
stitches the scrolling panel so nothing is clipped. Anchoring the scroll on the scale fields
rather than the message keeps the message in frame, since it renders just below them.

Capturing the frames then exposed two defects in the recipe that the state assertions had
missed, because a `ui.wait_for` on the warning passes regardless of what else is on screen:

1. The ticket had no order count or size, so a blocking validation error occupied the same
   message slot. The assertion passed; the trader would never have seen the warning.
2. The full-cross values put start above end, tripping "Start price must be lower than end
   price" and disabling Place order — so the frame meant to prove "non-blocking" showed a
   disabled button.

Both are fixed. The lesson is that a green assertion proves the element exists, not that the
user would see it in a usable state.
