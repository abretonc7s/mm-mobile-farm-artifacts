# Report — TAT-3687

Bump `@metamask/perps-controller` `^10.0.0` → `^11.0.0` and fix the breaking
changes minimally. Full detail in `approach.md` (analysis), `implementation.md`
(decisions), `recipe-coverage.md` (proof matrix) and `learnings.md`.

## Self-Review Fixes

All three findings were verified against the installed package source before
editing — each held.

- **`app/components/UI/Perps/utils/orderUtils.ts`** — deleted the
  `resolveOrderExecution` helper. Confirmed it duplicated the controller's
  exported `getTriggerExecution` exactly: same body
  (`isLimitExecutionOrderType(orderType) ? 'limit' : 'market'`,
  `dist/utils/orderTypes.cjs:55-57`), same signature
  (`(orderType: OrderType): OrderExecution`,
  `dist/utils/orderTypes.d.cts:34`), and a docblock naming this exact use case
  ("the coarse execution type that consumers predating trigger orders
  understand"). Also dropped the now-unused `OrderExecution` import.
- **`PerpsOrderView.tsx` (1007, 1016, 1513) and `usePerpsProOrderForm.ts`
  (355, 362, 489)** — the six toast-map indexing sites now call
  `getTriggerExecution` imported from `@metamask/perps-controller`, and no
  longer import the local helper from `orderUtils`.
- **`app/components/UI/Perps/utils/orderUtils.test.ts`** — removed the
  `describe('resolveOrderExecution')` block (the controller ships its own tests
  for `getTriggerExecution`) and its now-unused import.
- **`app/components/UI/Perps/utils/translatePerpsErrorCoverage.test.ts:65`** —
  `toStrictEqual([...one known gap])` → `toStrictEqual([])`, so the test now
  fails on any new unresolved key instead of carrying a real gap in a passing
  expectation.
- **`locales/languages/en.json`** — added the missing
  `perps.errors.subscriptionClientNotAvailable` string that made the above
  possible, matching its two siblings (`exchangeClientNotAvailable`,
  `infoClientNotAvailable`) in wording and placement.
- **`artifacts/pr-description.md`, `artifacts/implementation.md`** — corrected
  an inverted rationale. Both had claimed the `determineMakerStatus` change
  prevented a `Stop Market` order being priced at the maker rate. That does not
  follow: HyperLiquid's adapter resolves `orderType` through
  `getTriggerExecution` before the order reaches the app
  (`hyperLiquidAdapter.cjs:188`), so `Order.orderType` only ever holds
  `'market'` or `'limit'` at runtime and the old `=== 'market'` guard already
  returned taker. The maker-rate bug was v10 reporting such orders as `limit`,
  which the controller upgrade fixes on its own. The code change is unchanged
  and still correct — only the justification was wrong, and a reviewer would
  have approved on a premise that does not hold. Restated as aligning the guard
  with the controller's execution semantics for the widened signature,
  behaviourally identical for every value `Order.orderType` can hold.
- **`orderUtils.test.ts` `describe('Trigger Orders')`** — added a comment
  recording that these cases pin the widened contract rather than guarding a
  reachable regression, for the same reason.
- **`artifacts/recipe-coverage.md`, `artifacts/evidence-manifest.json`** —
  updated the stale `resolveOrderExecution` references so the evidence
  descriptions name the expression that actually ships.

### Deviation from the prescription

The review said to delete "`resolveOrderExecution` and its `OrderExecution` /
`OrderType` imports". Only the `OrderExecution` import was removed:
`OrderType` and `isLimitExecutionOrderType` are still used by
`determineMakerStatus`'s widened signature and its guard, so removing them
would not compile.

### Note on the recipe gate

The recipe initially failed validation (exit 5, `workflow.unresolved_call_ref`)
because the `perps` recipe library — which resolved automatically during the
original run — was no longer registered in this slot. The library directory is
intact; re-running with an explicit
`--library perps=/Users/deeeed/dev/metamask/experimental-metamask-recipe-perps`
restored it. Unrelated to the code changes.

## Self-Review Fixes — pass 2 (evidence accuracy)

Root cause: the evidence prose hard-coded live-price-derived numbers read from
the screenshots as they existed at 11:14/11:43, and the final recipe re-run at
11:50–11:51 overwrote those same PNG paths with fresh captures at slightly
different marks. The descriptions therefore no longer matched the frames
actually shipped.

Confirmed drift by re-reading all four shipped frames:

| Claim | Prose said | Shipped frame |
|---|---|---|
| Limit price (order form) | $1,898.4 | $1,898.9 |
| Auto close take profit | $2,135.8 | 2136.7 |
| Auto close stop loss | $1,803.6 | 1804.3 |
| Close-position notional | $10.06 | $10.07 |

Everything else in the prose already matched (Limit/Market order type, the $10
notional, 0.0053 ETH, the $0.01 fee, +25% / −10% presets, expected profit/loss,
the 100% close, margin/receive, and the "Order submitted" toast text).

- **`artifacts/evidence-manifest.json`** — rewrote the notes for
  `perps-order-form-mobile.png`, `perps-position-auto-close-mobile.png` and
  `perps-position-close-mobile.png`.
- **`artifacts/recipe-coverage.md`** — rewrote the screenshot sentences in rows
  C5, C6 and C7, and the toast bullet under Notes.

### Deviation from the prescription

The review asked for the quoted values to be corrected. Re-typing the current
numbers would fix this run and re-break on the next one — the recipe re-captures
these frames every time it runs, and the mark moves. So instead of refreshing
the figures, the prose is now keyed to **recipe-controlled inputs** (the $10
notional, the +25% / −10% presets, the 100% close, the selected order type) and
states which price/fee fields are *populated* rather than what they read. That
removes the coupling that caused the drift. A note under `## Notes` in
`recipe-coverage.md` records the constraint so a later editor does not
reintroduce live values.

### Gates

No source or test file changed in this pass — `git diff HEAD` over
`*.ts/*.tsx/*.js/*.jsx` is empty — so steps 4 and 5 (affected tests, bounded
ESLint gate) had nothing to run. The full recipe was not re-run: its stated
condition is "after every code-changing self-review fix", and run 5 already
passed 207/207 against the code now at HEAD. Re-running would also re-capture
the same frames at yet another mark, which is the drift this pass exists to
remove. The artifact contract gate — which does validate the two files edited
here — passes.

### Note on commit hashes

Between passes an external process rebased this branch onto `origin/main`:
`49f7c3f54a` → `446cc379b7` and `2df1785419` → `f506550989` (reflog
`HEAD@{3}..HEAD@{0}`). Content is unchanged — 15 files, all fixes verified
present after the rebase.
