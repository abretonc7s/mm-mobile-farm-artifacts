# Recipe Coverage — TAT-3904

Recipe: `artifacts/recipe.json` (19 nodes, all pass)
Run: `artifacts/recipe-run/` — `summary.json` status `pass`, exitCode 0.

Proof is **mixed**: a `ui.wait_for` assertion on the rendered tree for every claim, plus a
screenshot of each warning variant.

The warning renders low in the Pro order form, which at first looked like it ruled out
visual proof. It does not. Two flags solve it: `mm-harness run --hud hide` suppresses the
recipe progress overlay for the whole run, and `ui.capture_surface` stitches the scrolling
panel into one image so nothing is clipped. Anchoring the scroll on the *scale fields*
rather than on the message matters too — the message sits below those fields, so scrolling
to the message itself pushes it off the top of the viewport.

| AC | Claim | Proof mode | Recipe nodes | Screenshot |
|----|-------|-----------|--------------|------------|
| 1 | Long scale order crossing the best ask warns | mixed | `full-start` → `expect-full-above` (asserts "Limit price is above current price") | `evidence-ac1-long-full-cross.png` |
| 2 | Short scale order crossing the best bid warns with mirrored copy | mixed | `short-start`, `short-end` → `expect-full-below` (asserts "Limit price is below current price") | `evidence-ac2-short-full-cross.png` |
| 3 | Partly-crossing ladder gets distinct copy from a fully-crossing one | mixed | `partial-end` → `expect-partial-above` (asserts "Part of your order is above current price"), contrasted with `expect-full-above` on the same side | `evidence-ac3-partial-cross.png` |
| 4 | Warning re-evaluates on endpoint edit and on side flip | state | Endpoint edit: `expect-quiet` (absent) → `partial-end`/`expect-partial-above` (present) → `full-start`/`expect-full-above` (escalated). Side flip: `flip-short` → `expect-cleared-on-flip` (absent without touching either endpoint) | — |
| 5 | Warning is non-blocking; the order can still be placed | mixed | `expect-still-placeable` asserts the place-order control is present while the warning is showing | All three frames show Place order enabled beside the warning |

## Failing-first

The recipe was run against the branch with the implementation stashed out
(`git stash push` of the three source files, app restarted onto that source).
Result: **fail**, exitCode 1, first behavioural assertion `expect-partial-above`
timed out — `last result={"present":false,...}`. Nodes 1-8 (navigation and the
no-warning baseline) passed, which is correct: with no feature, no warning ever
appears, so the "absent" baseline still holds and only the "present" assertions fail.
With the implementation restored, all 19 nodes pass.

This is the self-test the task requires: removing the implementation makes the recipe FAIL.

## Recipe defects found while capturing evidence

The screenshots caught two defects in the recipe that the state assertions had missed,
because a `ui.wait_for` on the warning passes regardless of what else is on screen:

1. **The ticket was incomplete.** Without an order count and size, a blocking validation
   error ("Order count must be between 2 and 20", then "must meet the market minimum lot
   size") occupied the same message slot. The warning assertion still passed, but the
   trader would never see the warning in that state. Fixed by setting 2 rungs and a $35
   size so the ticket is genuinely placeable.
2. **The ladder was mis-ordered.** The first full-cross values put start above end, which
   trips "Start price must be lower than end price" and disables Place order — so the
   frame proving "non-blocking" showed a disabled button. The form requires start < end on
   both sides; fixed by moving the whole well-ordered range across the market instead of
   inverting the endpoints.

Both were invisible to state assertions and obvious in a screenshot. That is the argument
for capturing the frame even when an assertion already passes.

## Gap

`expect-quiet` (the no-warning baseline) also passes without the implementation, since
the message element is absent in both worlds. It is retained because it guards the
opposite regression — a future change that warns on every scale order would fail it.
