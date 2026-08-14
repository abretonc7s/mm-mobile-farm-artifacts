# TAT-3742 — report

The delivery report for this task is `pr-description.md` (PR flow). This file carries
the self-review fix pass.

## Self-Review Fixes

- `app/components/UI/Perps/hooks/usePerpsOrderValidation.ts:39-45,238-245,283-291,331-338` —
  the hook now reports `hasSuppressedBalanceError` so a caller that asked for
  `skipBalanceError` can tell "invalid, but I withheld the reason" apart from
  "invalid for a reason already in `errors`". Reset to `false` on the size-guard
  early return and in the catch branch so the flag can never go stale.
- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:1407-1419` — the
  `!isValid` branch no longer passes `orderValidation.errors[0]` straight through when
  the array is empty. It falls back to the concrete
  `insufficient_funds_to_cover_trade` string when the balance message was suppressed,
  and to `perps.order.validation.failed` otherwise, so neither
  `PerpsToastOptions.formValidation.orderForm.validationError(error: string)` nor
  `PERPS_ERROR`'s `ERROR_MESSAGE` can receive `undefined` on the post-deposit re-entry
  path (`handleDepositConfirm -> handlePlaceOrder(true)`), which bypasses the disabled
  button.
- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:1714-1745` —
  `payTokenFundingMessage` also fires on `orderValidation.hasSuppressedBalanceError`.
  This closes the second half of the issue: `hasInsufficientPayTokenBalance` returns
  `false` on `!payToken`, so while a custom token is selected but its `payToken` has
  not landed the screen previously showed no funding message at all even though the
  order was blocked.
- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.test.tsx:505` — deleted
  the unused `useIsTransactionPayLoading` mock override. Confirmed dead first:
  `git grep useIsTransactionPayLoading -- app/components/UI/Perps` returned only that
  line.
- Tests pinning the above: `reports no suppression when the balance covers the required
  margin` and an extended `withholds the balance message …` assertion in
  `usePerpsOrderValidation.test.ts`, plus `states a funding message when validation
  withheld its balance error and the pay token has not landed` in
  `PerpsOrderView.test.tsx`.

### Deviation from the literal prescription

The review suggested `orderValidation.errors[0] ?? payTokenFundingMessage ?? strings(...)`.
Referencing `payTokenFundingMessage` inside `handlePlaceOrder` is not viable: the
callback is created around line 1290 while `payTokenFundingMessage` is declared around
line 1700, so adding it to the `useCallback` dependency array would evaluate the
binding in its temporal dead zone and throw `Cannot access before initialization` on
every render. Hoisting the memo above `handlePlaceOrder` would have meant moving ~40
lines of unrelated code. Instead the toast resolves its own concrete string from the
suppression flag, and the missing on-screen message — the part the reviewer's chain was
reaching for via `payTokenFundingMessage` — is fixed at the memo itself. Same two
outcomes, no code movement, no TDZ hazard.

### Verification

- `yarn jest PerpsOrderView.test.tsx usePerpsOrderValidation.test.ts --no-coverage` → 146 passed (was 144)
- Affected suites incl. `PerpsProOrderForm` → 10 suites, 351 passed
- `mm-harness run recipe.json` → exit 0, 21/21 nodes ok (`trace.json`)
- `check-task-artifact-contract.mjs` → `TASK_ARTIFACT_CONTRACT_PASS`
- scoped ESLint → 0 errors; the same 7 warnings that exist verbatim on `origin/main`

## Self-Review Fixes — pass 2

The previous pass replaced an `undefined` toast argument with
`strings('perps.order.validation.failed')`. That string is already the toast's own
title, so the toast rendered it twice — bold, then plain. The argument is an optional
*detail* line, not the message.

- `app/components/UI/Perps/hooks/usePerpsToasts.tsx:204,1054` — widened
  `formValidation.orderForm.validationError` to `(error?: string)` on both the
  interface and the implementation, so "no detail" is expressible. This matches
  `adjustmentFailed: (error?: string)` directly above it, and `getPerpsToastLabels`
  (`:229-253`) already appends the secondary line only when the argument is truthy.
- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:1408-1424` — the
  suppressed-funding string is now resolved into its own `suppressedFundingError`
  binding that stays `undefined` when nothing was suppressed. `firstError` is
  `errors[0] ?? suppressedFundingError` and is passed to the toast as-is, so the
  no-message case renders a clean single-line toast again.
- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:1431-1432` —
  `PERPS_EVENT_PROPERTY.ERROR_MESSAGE` keeps a concrete value via
  `firstError ?? strings('perps.order.validation.failed')`, preserving the original
  goal of never emitting `undefined` telemetry.
- `app/components/UI/Perps/hooks/usePerpsToasts.test.tsx:1266-1281` — added
  `returns a single line when no detail is available`, pinning that
  `validationError()` produces exactly one label.

### Coverage note — what is and is not tested

The caller-side branch (`PerpsOrderView.tsx:1407`) is **not** reachable from a unit
test, so no test asserts the argument the view passes. Two independent blockers: the
place-order button is disabled whenever `!orderValidation.isValid`, so
`fireEvent.press` never invokes `onPress` (verified — a test written against it
recorded 0 calls); and the production entry point, the post-deposit re-entry
`handleDepositConfirm(meta, () => handlePlaceOrder(true))`, runs its callback inside
the same press, so the closure still sees the `isValid: true` that let the press
through. Reproducing the real interleaving would need a re-render between the press
and the callback.

Rather than ship a test that exercises nothing, the guarantee is split: the toast test
pins "no detail ⇒ single line", and the `(error?: string)` signature makes the absent
detail a legal, type-checked call. The removed attempt is recorded here rather than
left in the suite.

### Verification

- `yarn jest usePerpsToasts.test.tsx PerpsOrderView usePerpsOrderValidation.test.ts PerpsProOrderForm --no-coverage` → 11 suites, 420 passed
- `mm-harness run recipe.json` → exit 0, 21/21 nodes ok
- `check-task-artifact-contract.mjs` → `TASK_ARTIFACT_CONTRACT_PASS`
- scoped ESLint → 0 errors, 3 pre-existing warnings on `PerpsOrderView.tsx`

## Follow-up fix — stale pay-token balance (found during PR evidence review)

Reported by the author while reviewing this PR's own after-screenshot: it showed
"Minimum order size is $10" with a disabled slider and an "Insufficient funds" button
for a token the picker had just offered at $9.37, on a $10 order at 2x. Those numbers
contradict each other — $9.37 at 2x supports an $18.74 notional, well over the $10
minimum. I had read that capture four times and checked it only for the shape I
expected (one message instead of three) rather than for whether the message was true.

Diagnosis, from probing both balance sources side by side on device:

```
snapshotBalanceUsd: "0"                     ← what PerpsOrderView read
liveBalanceUsd:     "9.3670768275998875…"   ← what the token picker reads
symbol: ETH · chainId: 0xa4b1
```

`payToken.balanceUsd` is produced once by `updatePaymentToken` → `getPaymentToken` →
`getTokenBalance` at selection time and is never refreshed, so it freezes at `0` when
the balance has not been polled yet. The confirmations layer already knew this:
`usePayTokenAccountBalance` exists solely to work around it, and its own comment says
*"payToken.balanceUsd is a one-time snapshot that can be stale (race with AccountTracker
polling)"*. The token picker used it; the Perps trade screen did not.

- `PerpsOrderView.tsx:2470-2480` — `effectiveAvailableBalance` now derives from
  `usePayTokenAccountBalance()` instead of the frozen snapshot, guarded so a missing
  `payToken` still falls back to the Perps balance rather than a hard `0`.
- `PerpsOrderView.tsx:771-786` — `hasInsufficientPayTokenBalance` compares
  `marginRequired` against `spendableBalance`, the same balance validation and the
  slider use. Two independent balance sources on one screen was the defect class; this
  removes the second one instead of keeping them in sync by hand.
- `PerpsOrderView.test.tsx` — the helper now pins the stale snapshot at `'0'` for every
  case, so anything reading it fails. Added `funds the trade from the live pay token
  balance, not the stale snapshot on payToken`. Two pre-existing tests
  (`states one funding message when the selected pay token cannot cover the trade`,
  `fires warning event when hasInsufficientPayTokenBalance is true`) encoded the
  snapshot behaviour and were rewritten to express the shortfall through the balance
  the screen now uses.

Evidence re-captured against the fixed code: `after-ac1-after-payment-switch.png`
(md5-matched to `recipe-run/screenshots/`) and `after.mp4` now show no funding message,
an enabled slider and an enabled "Long ETH" button at margin $5.01.

### Verification
- 11 suites, 421 passed
- `mm-harness run recipe.json` → exit 0, 21/21 nodes ok
- scoped ESLint → 0 errors, pre-existing warnings only

## Self-Review Fixes — pass 3 (static reviewer)

- `usePayTokenAccountBalance.ts:14-67` — the hook now returns `isResolved`. It has three
  paths that fall back to the stale `payToken.balanceUsd` (no pay token, no matching
  account token, no USD rate) and previously gave callers no way to tell those apart
  from a confirmed balance. `false` on all three, `true` only when the figure comes from
  the reactive account source and a real rate.
- `PerpsOrderView.tsx:626,773` — `isPayBalanceLoading` now also requires
  `isPayBalanceResolved`. Quote readiness was standing in for balance readiness, so once
  the quote settled an unresolved balance could still be read as a confirmed zero and
  reproduce the disabled slider and false minimum-order message.
- `PerpsOrderView.tsx:2473-2489` — the wrapper withholds `effectiveAvailableBalance`
  until the balance resolves, so the form falls back to the Perps balance rather than
  receiving a confirmed-looking `0`.
- `PerpsOrderView.tsx:1159` — **removed** `|| isPayBalanceLoading` from `skipValidation`.
  This is the reviewer's second issue and the fix shrinks the diff: skipping validation
  made the hook early-return without touching state, so the *previous* payment method's
  `Insufficient balance … Available: $0` row stayed on screen through the transition
  that is supposed to be message-free. `skipBalanceError: hasCustomTokenSelected` already
  suppresses that message by category, so the extra guard was redundant as well as harmful.
- `PerpsOrderView.test.tsx` — the context mock now records the props handed to
  `PerpsOrderProvider` and renders the real provider, so
  `hands the order provider the live pay token balance, not the stale snapshot` observes
  the integration boundary instead of a value the test injected downstream. Verified
  fix-sensitive: reverting the wrapper to `payToken.balanceUsd` fails it with
  `Expected: 1000, Received: 0`. Added `withholds the balance from the order provider
  until it resolves`.
- `PerpsOrderView.test.tsx` — the render helper is async and flushes the timer-backed
  `requestAnimationFrame` update inside `act()`. The funding-state describe now emits
  **0** `act()` warnings (28 remain elsewhere in the file, all pre-existing and untouched).
- `PerpsOrderView.test.tsx` — funding copy is derived from
  `strings('perps.order.validation.minimum_amount' | '…insufficient_funds_to_cover_trade')`
  through the file's own i18n mock instead of repeated as literals.
- `usePayTokenAccountBalance.test.ts` — existing strict-equality expectations carry
  `isResolved`; added cases for the resolved path and the missing-rate path. Note the
  zero-`rawBalance` case is `isResolved: true` — an account that genuinely holds nothing
  is a confirmed zero, not an unknown one.

### Note on the first issue's ownership

`usePayTokenAccountBalance` is owned by `@MetaMask/confirmations` per CODEOWNERS. The
change is purely additive (a new field; no existing return value or behaviour altered)
and is the same readiness concept that upstream issue #34787 asks for. Flagging it so
the cross-team review is deliberate rather than incidental.

### Verification
- 53 suites, 1047 passed (Perps + confirmations pay/alerts/pay-with-row consumers)
- `mm-harness run recipe.json` → exit 0, 21/21 nodes ok
- `check-task-artifact-contract.mjs` → `TASK_ARTIFACT_CONTRACT_PASS`
- scoped ESLint → 0 errors, 7 pre-existing warnings (a new `no-shadow` introduced by the
  mock was removed by renaming, back to baseline)

## Self-Review Fixes — pass 4

- `PerpsOrderView.tsx:1746` — **removed** the `orderValidation.hasSuppressedBalanceError`
  arm from `payTokenFundingMessage`. Validation is debounced but `isPayBalanceLoading`
  clears the instant the balance resolves, so for one beat the flag still described the
  pre-switch Perps balance while the freshly resolved token balance covered the trade —
  rendering "Insufficient funds to cover the trade" against a balance that could pay.
  The arm was also already unreachable for the case it was written for: with `payToken`
  undefined the hook reports `isResolved: false`, so the memo returns at the
  `isPayBalanceLoading` guard before reaching it. Only the live check may answer here.
- `PerpsOrderView.test.tsx` — replaced the test that hard-coded that impossible
  resolved-balance-plus-stale-flag pairing (it masked the regression) with
  `drops the withheld balance error once a sufficient balance resolves`, which rerenders
  from unresolved to resolved while the suppression flag stays stale. Verified
  regression-sensitive: restoring the removed arm fails it.
- `PerpsOrderView.test.tsx:497` — the `jest.fn<>` return type now declares `isResolved`,
  so the mock literals match the hook's contract instead of exceeding the declared type.
- `pay-with-row.test.tsx:162,257` and `usePayWithPreferredToken.test.ts:88` — added the
  now-required `isResolved` to each typed `mockReturnValue`. Confirmed by grep that these
  are the only sites constructing the hook's return type; the two non-test consumers
  (`useInsufficientPayTokenBalanceAlert.ts`, `pay-with-row.tsx`, `usePayWithPreferredToken.ts`)
  only destructure, so the added field is safe for them.

### On the typecheck

The reviewer was right that a green Jest run only proves these files transpile. Because
the finding was itself a TypeScript gate failure — the case the checklist carves out —
`yarn lint:tsc` was run this pass rather than deferred: **exit 0, no output**. The
contract is verified, not assumed.

### Verification
- 53 suites, 1047 passed (one earlier run reported a suite-level jest worker flake with
  0 failing tests; clean on re-run)
- `yarn lint:tsc` → exit 0
- `mm-harness run recipe.json` → exit 0, 21/21 nodes ok
- `check-task-artifact-contract.mjs` → `TASK_ARTIFACT_CONTRACT_PASS`
- scoped ESLint → 0 errors, 7 pre-existing warnings

## Self-Review Fixes — pass 5 (no change)

The checklist was re-dispatched with both issues already fixed in `d2acd00a750`, and the
only review-feedback file present now reads **PASS**. Verified both against HEAD rather
than assuming: the stale suppression arm is gone from `payTokenFundingMessage` (the flag
survives only inside `handlePlaceOrder`), and all four typed mock sites carry
`isResolved`. Re-ran the gates on unchanged HEAD — 830 tests, `lint:tsc` exit 0, recipe
exit 0 with 21/21 nodes, contract gate pass. Full write-up in `no-change-report.md`;
disposition `no-change`.

## Self-Review Fixes — pass 6

Two surfaces I had not consolidated, both undermining AC1's "at most one funding message".

- `useInsufficientPayTokenBalanceAlert.ts:64-80,138,149` — the alert compared
  `balanceUsd`/`balanceRaw` from `usePayTokenAccountBalance` without consulting
  `isResolved`, so while the balance was unresolved it could raise a **blocking**
  insufficiency from the stale snapshot. Added `isPayBalanceKnown` and required it for
  the two pay-token comparisons only. The money override reads a different source and
  the source-network and no-quote checks use their own inputs, so all three still run
  independently — exactly the carve-out the review asked for.
- `PerpsOrderView.tsx:2265,2286` — both place-order disabled conditions now include
  `isPayBalanceLoading`, so an unknown balance blocks the CTA instead of being reported
  as zero. Without this, suppressing the alert would have left the button enabled on a
  balance nobody has measured.
- `PerpsOrderView.tsx:806-816,1930,2218` — `payTokenFundingMessage` and the blocking
  pay-alert row rendered independently, so a genuinely insufficient token could show
  both at once. The blocking alerts are now split by kind: the *balance* alert becomes
  the lowest-priority arm of `payTokenFundingMessage` (minimum → cannot-cover → alert),
  and the bottom row carries only the **no-quote** message, which is a different failure
  and keeps its own row.
- `PerpsOrderView.tsx` — removed `blockingPayAlertMessage`, orphaned by the above.

### Tests

- `shows one funding row when the calculation and a blocking balance alert both fire` —
  the overlap case the review asked for. Verified regression-sensitive: restoring the
  independent alert row fails it.
- `still surfaces an unrelated no-quote failure alongside the funding state` — guards the
  carve-out so the consolidation cannot silently swallow no-quote errors.
- `returns no alert while the pay token balance has not resolved` (alert suite) — same
  shortfall as its sibling but with an unresolved balance; asserts `[]`.
- `useInsufficientPayTokenBalanceAlert.test.ts` — these cases configure the balance
  through the pay token, and the hook previously reached its snapshot fallback in that
  fixture. Mocked `usePayTokenAccountBalance` to mirror the configured pay token as a
  *resolved* account balance, so the suite tests the alert rather than the balance hook's
  fallback (which has its own suite).
- `PerpsOrderView.test.tsx` — the shared `usePayTokenAccountBalance` mock now defaults to
  `isResolved: true`. The loading window is the exception; only the tests exercising it
  opt in. Six unrelated button-enabled tests were failing purely on that default.

### Verification
- 81 suites, **1384 passed**
- `yarn lint:tsc` → exit 0
- `mm-harness run recipe.json` → exit 0, 21/21 nodes ok
- `check-task-artifact-contract.mjs` → `TASK_ARTIFACT_CONTRACT_PASS`
- scoped ESLint → 0 errors, 7 pre-existing warnings (two new `no-shadow` on `alert`
  introduced by this pass were removed by renaming)

### Cross-team note

This pass touches `useInsufficientPayTokenBalanceAlert.ts`, owned by
`@MetaMask/confirmations` (as is `usePayTokenAccountBalance.ts` from the previous pass).
Both changes are readiness gates in service of upstream issue #34787.

## Self-Review Fixes — pass 7 (test quality)

Six findings, all on tests I added in the previous two passes.

- `PerpsOrderView.test.tsx` helper — `isResolved: !isBalanceLoading` welded quote
  loading to balance resolution, so neither the balance gate nor the disabled-CTA
  behaviour was independently covered. The helper now takes `isQuoteLoading` and
  `isBalanceResolved` separately, with two new tests for the case the review named:
  quote settled but balance unresolved → slider stays usable, no funding message, and
  the place-order button is disabled.
- `still surfaces an unrelated no-quote failure alongside the funding state` — ran with a
  *sufficient* balance, so the funding state its name claimed never existed. Now uses a
  below-minimum balance and asserts **both** rows, which is the actual coexistence claim.
- Alert mocks were reset after the assertions, so a failed assertion leaked the
  implementation into later tests. Moved into the describe's `afterEach`.
- Absence assertions in this describe now use `not.toBeOnTheScreen()` per
  `docs/testing/unit-testing.md:235,250`, and the no-quote row is selected by a
  centralized testID rather than raw copy.
- `PerpsOrderView.tsx` / `Perps.testIds.ts` — added
  `PAY_TOKEN_NO_QUOTE_MESSAGE` so that row is addressable.
- `usePerpsToasts.test.tsx` — the new assertion sources its label from
  `strings('perps.order.validation.failed')` instead of repeating production copy.
- `useInsufficientPayTokenBalanceAlert.test.ts` — added
  `returns no fees alert while the pay token balance has not resolved`, so the guarded
  *fee* comparison has direct cover, not just the input comparison. Both readiness tests
  verified regression-sensitive: removing the two `isPayBalanceKnown` guards fails them.

### Verification
- 81 suites, **1387 passed**
- `yarn lint:tsc` → exit 0
- `mm-harness run recipe.json` → exit 0, 21/21 nodes ok
- `check-task-artifact-contract.mjs` → `TASK_ARTIFACT_CONTRACT_PASS`
- scoped ESLint → 0 errors, 7 pre-existing warnings
