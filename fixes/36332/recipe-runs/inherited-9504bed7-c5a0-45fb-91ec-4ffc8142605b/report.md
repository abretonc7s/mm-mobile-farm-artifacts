# TAT-3931 — Perps activity showed only part of a multi-fill trade

## Self-Review Fixes

- **app/components/UI/Perps/utils/transactionTransforms.ts:120** — bounded the same-second
  cross-order grouping rule to the close category. Groups are now seeded per order id; only
  `Close Long`/`Close Short`/`Sell`/`Auto-Deleveraging` seed by second, which is the trigger-order
  split (TAT-2196) the rule was written for. Reproduced the regression first against the committed
  code: two distinct `Open Long` orders 0.8 s apart returned 1 row of size 2.
- **app/components/UI/Perps/utils/transactionTransforms.ts:139** — the transitive union-find chain
  across unrelated orders is gone as a consequence of the above, not by weakening the linking step.
  Order-seeded groups are already whole, so the link can only join groups that genuinely share an
  order id; the close side keeps the cross-second linking it needs. Reproduced first:
  `A@+0.1s, B@+0.9s, B@+2.1s, C@+2.9s` returned 1 row of size 4.
- **app/components/UI/Perps/utils/transactionTransforms.test.ts:313** — added two negative tests
  that actually discriminate: two opens of different orders inside one second stay separate, and a
  chain across three order ids does not collapse. Verified both fail on the pre-fix seed key
  (`2 failed, 120 passed`) and pass on the fix.
- **app/components/UI/Perps/utils/transactionTransforms.test.ts:757** — added a flip assertion at
  the display-transform layer. A 37.66 long flipped into a 5.57 short (43.23 traded, split over two
  seconds) now yields one row with `subtitle` `43.23 ETH` and `fill.size` `5.57`. Verified it fails
  when flips are excluded from grouping, where the same fixture produces two rows (`13.23 ETH`
  size 5.57 and `30 ETH` size 7.66) — the partial view the ticket describes.
- Doc comments on `aggregateFillsByTimestamp` updated to state the two rules and why the
  cross-order one is limited to the close side.

### On the ticket's "5.57"

The review flagged that the flip fixture renders `fill.size` of `5.57`, the number TAT-3931 calls
wrong. `5.57` is correct post-fix and means something different from the ticket's `5.57`:
`fill.size` for a flip is `|startPosition − totalSize|`, the position the flip left open. Post-fix
it is computed from the earliest fill's `startPosition` and the whole order's traded size; pre-fix
it was computed per fill, so the user saw a number derived from one slice of the order. The new
display-layer test pins both numbers — the `43.23` traded (what the Perps lists render as
`subtitle`) and the `5.57` resulting short — and fails if flips stop being grouped.

## Verification after self-review fixes

- `transactionTransforms.test.ts` 123/123; 5 affected suites 297/297
- scoped `yarn eslint --max-warnings=0` over the 2 changed files: pass
- `mm-harness run recipe.json`: pass, exit 0, 27/27 nodes, re-recorded `after.mp4` and both
  `after-*.png` on the final code
- `check-task-artifact-contract.mjs`: `TASK_ARTIFACT_CONTRACT_PASS`

## Not changed (with reasons)

- `transactionTransforms.ts:42-71` duplicating the direction parsing at `:355-362` — extracting a
  shared `parseFillDirection` helper is a refactor across a function this ticket does not touch,
  outside the self-review scope discipline. Worth a follow-up.
- `transactionTransforms.ts:245` latest-fill timestamp churning the derived row id while an order
  is still filling — cosmetic remount, no user-visible effect, and changing it would undo the
  correct "order completes at its last fill" ordering.
- `app/util/activity-adapters/adapters/perps-transaction.ts:295` showing the flip delta while the
  Perps lists show the total traded — pre-existing divergence, not introduced here. The new
  display-layer test documents both numbers rather than silently changing one.
- Extension parity (`metamask-extension-1/.../transactionTransforms.ts:42` has the identical
  defect) — needs its own ticket and PR; recorded in the PR body.

## Self-Review Fixes — round 2

- **app/components/UI/Perps/utils/transactionTransforms.ts:142** — corrected the linking comment.
  It claimed the step "can only chain groups that genuinely share an order id"; that holds per link
  but not across the transitive union, so `X@s1, {X,Y}@s2, {Y,Z}@s3` really do land in one entry.
  The comment now states the chain is transitive, why the hops are bounded (each needs a
  same-second close collision — the condition the pre-fix code already merged on), and why
  order-seeded groups (opens, buys, flips) cannot take part.
- **app/components/UI/Perps/utils/transactionTransforms.ts:348** — replaced the stale call-site
  comment and the matching `transformFillsToTransactions` JSDoc, both of which still described
  close-only, same-timestamp aggregation.
- **app/components/UI/Perps/utils/transactionTransforms.ts:102** — renamed
  `aggregateFillsByTimestamp` to `aggregateFillsByOrder`. The old name described the rule the fix
  replaced; order id is now the primary key and the second is the close-side exception. One caller
  and one test import, mechanical rename, 297 tests still pass.
- **artifacts/pr-description.md** — the Screenshots/Recordings section said nothing. It now states
  what each capture shows and points at `evidence-manifest.json`. Deliberately no hand-written
  local paths: the gateway substitutes this section from the manifest at publish time, and literal
  `artifacts/...` paths would render as broken links on GitHub.

### Declined: gating the same-second seed on a trigger `detailedOrderType`

The review suggested bounding the residual close-side chain by seeding on the second only for
fills carrying a Stop / Take Profit `detailedOrderType`. That would silently disable the TAT-2196
close aggregation on two of the three surfaces this ticket covers:

- `detailedOrderType` is enriched onto fills in exactly one hook,
  `usePerpsTransactionHistory.ts:197` (the Activity page). `usePerpsHomeData` and
  `usePerpsMarketFills` pass `getOrderFills` results straight through.
- The provider-side enrichment at
  `node_modules/@metamask/perps-controller/dist/providers/HyperLiquidProvider.cjs:3370` is
  best-effort: it awaits a separate historical-orders fetch inside its own try/catch, explicitly so
  "a malformed order never discards fetched fills". When that fetch fails or returns nothing the
  field is simply absent, and WebSocket live fills never carry it at all.

So the gate would be off precisely when a TP/SL fires and the user is watching — the case the rule
exists for. The review itself called the current behaviour defensible; the comment was the real
defect, and that is what was fixed.
