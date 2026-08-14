# TAT-3742 learnings

- **Investigation dominated: ~2h to root-cause, ~25 min to fix.** The ticket named four
  symptoms with no ACs and no screenshots, and all four turned out to be one unresolved
  `payToken.balanceUsd === '0'` fanning out. What cost the time was that the window is
  timing-dependent: the first two manual reproductions worked, then five consecutive
  recipe runs did not. The unlock was realising `pendingConfig.selectedPaymentToken`
  persists, so the screen re-opens already on the token and pressing the row is a no-op.
  Adding a `setup-reset-to-perps-balance` node (re-select Perps balance first, then
  switch) made the repro deterministic. **Any pay-with-token repro must force the
  Perps-balance → token transition explicitly.**

- **`ui.wait_for expected="visible"` does not work on the Perps trade screen.** Probed in
  isolation, the place-order button, the funding message and the slider all return
  `{"present": true, "visible": false, "error": "Target exists in fiber tree but no
  measurable native node was found"}`. This is a silent trap: `expected: "hidden"` then
  passes for *everything*, so a baseline recipe asserting "the button is hidden" looks
  like proof and is worthless. I had already captured a baseline on that bogus assertion
  and had to re-author both recipes and re-record. **Probe `expected: "visible"` on one
  target with `mm-harness call` before building a recipe around it.**

- **`ui.press --arg text=...` resolves the wrong element on Perps screens.** Pressing
  text `ETH` and `BNB` in the pay-with sheet both navigated to that asset's *market*
  screen instead of selecting the row. Row testIDs are not in `Perps.testIds.ts` — they
  live in `usePayWithCryptoSection.ts` / `usePayWithPerpsSection.tsx`
  (`pay-with-crypto-section-preferred-token-row`, `pay-with-perps-section-balance-row`,
  `pay-with-crypto-section-other-assets-row`). Worth knowing before hunting for them.

- **`git stash pop` after committing a change in the same file conflicts.** Step 25 tells
  you to stash, commit the marker removal, then pop — but the stash still contains the
  marker, so the pop conflicts on the very hunk you just deleted. Resolving means taking
  the stashed side and re-deleting the marker block. A note in TASK.md would save the
  detour.

- **Metro logs answered a question the code could not.** The `$0` balance is not a pure
  race: the Arbitrum balance multicall in this slot returns `httpStatus 401`, so the read
  genuinely never lands. Grepping `metro.log` for the multicall revert was what turned
  "probably a timing flash" into a fact, and it is why the fix guards the *display* of
  the value rather than trying to fix the read.

## Self-review (rev-claude)

- **Suppressing a message is not the same as suppressing a state.** The fix correctly keeps
  `isValid: false` while hiding the balance string, but every consumer of `errors[0]` then has to
  tolerate an empty array. Checking who reads `errors[0]` — not just who renders `errors` — is what
  surfaced the blank-toast path at `PerpsOrderView.tsx:1408`.
- **A disabled button is not proof a branch is dead.** The `!isValid` guard inside `handlePlaceOrder`
  looked unreachable until the post-deposit re-entry (`handleDepositConfirm(..., () =>
  handlePlaceOrder(true))`) turned up — a second caller that never touches the button.
- **Warning counts need a baseline before they mean anything.** ESLint reported 7 warnings on the
  changed files; running the same constructs against `origin/main` showed all 7 pre-date the diff.
  Same for the `act()` warnings — the pre-existing describe blocks emit them too.
- **Verify evidence provenance by hash, not by filename.** `md5` matched the packaged before/after
  PNGs to `recipe-baseline-run/` and `recipe-run/` outputs, which is what makes the visual delta
  trustworthy rather than merely plausible.

## Self-review fix pass

- **Suppressing a message without a replacement is a hole, not a fix.** My
  `skipBalanceError` correctly kept `isValid: false` while hiding the duplicate row, but
  I never asked what consumes `errors[0]` afterwards. Two callers did: a toast typed
  `error: string` and a `PERPS_ERROR` telemetry field, both reachable via the
  post-deposit re-entry that bypasses the disabled button. **When you remove a string
  from a collection another layer indexes into, grep every read of that collection
  before shipping.**

- **A useCallback dependency array is evaluated at declaration time, not call time.** The
  reviewer's suggested `errors[0] ?? payTokenFundingMessage ?? …` would have crashed with
  `Cannot access before initialization`: `handlePlaceOrder` is created ~400 lines above
  where `payTokenFundingMessage` is declared, and adding it as a dep evaluates the
  binding in its TDZ every render. The closure *body* running later is fine; the deps
  array is not. Solved by deriving the fallback from a flag already in scope instead of
  hoisting 40 lines.

- **Having the hook report *why* it stayed silent beat duplicating its predicate.** The
  view needed to know "the balance error was withheld", and the two candidate fixes were
  re-deriving `marginRequired > spendableBalance` in the component or returning
  `hasSuppressedBalanceError` from the hook. The second is a handful of lines and cannot
  drift — worth preferring over the smaller-looking duplicate, which is the same
  fragility class the reviewer had already flagged for the message-string de-dup.

- **The dead mock was a leftover from a discarded theory.** I added
  `useIsTransactionPayLoading` while hunting for a readiness signal, settled on
  `useIsTransactionPayQuoteLoading`, and never removed the first. Cheap to catch with
  `git grep <hook> -- <feature dir>` before committing a test file.

## Self-review loop 2 (rev-claude)

- **Verifying a fix means checking every write site of the new state, not the happy path.** The
  value of `hasSuppressedBalanceError` matters most in the branches nobody thinks about — the catch,
  the zero-size reset, the `assetPrice === 0` spread. Reading all four `setValidation` sites is what
  made "fixed" a statement rather than a guess.
- **A fallback can introduce its own regression.** Feeding `strings('perps.order.validation.failed')`
  into a toast whose *title* is already that string turns a previously clean one-line toast into a
  duplicated one. Checking the consumer (`getPerpsToastLabels` skips a falsy secondary) was what
  revealed that `undefined` had actually been rendering gracefully all along — the real defect was
  only in telemetry.
- **Re-check the evidence, not just the code, on a fix loop.** The `after` PNG had been regenerated
  (new mtime, new byte size); re-reading it and re-matching its md5 to the fresh `recipe-run` output
  is the only way to know the packaged proof tracks the current HEAD.
- **A fix hunk with no test that fails when it is reverted is a coverage note worth stating.** Half
  of this fix (the rendered message) is pinned by a new test; the other half (toast + telemetry) is
  not, because the disabled button makes the branch hard to reach.

## Self-review fix pass 2

- **I fixed "never pass `undefined`" without reading what the parameter *is*.**
  `validationError(error)` looks like it takes the message; it actually takes an
  optional detail line under a fixed "Order validation failed" title. My non-`undefined`
  fallback used that exact title, so the toast printed it twice. **Before hardening a
  call against a nullish argument, open the callee and find out whether the argument is
  the content or an optional embellishment — `undefined` was the correct value all
  along, and only the telemetry sibling needed a fallback.**

- **Two consumers of one variable wanted opposite things.** The toast wanted `undefined`
  to stay `undefined`; telemetry wanted a string. Collapsing both onto a single
  `firstError` is what created the bug. Splitting into `suppressedFundingError`
  (nullable, for display) plus a `?? fallback` at the telemetry site cost two lines and
  removed the conflict.

- **A test that cannot reach its branch is worse than no test.** I wrote a view-level
  test for the toast argument and it recorded 0 calls: the button is disabled precisely
  when `!isValid`, and the real entry — the post-deposit re-entry — runs its callback
  inside the same press, so the closure still sees the `isValid: true` that allowed the
  press. I deleted it and pinned the contract one layer down at `usePerpsToasts`
  instead, recording the gap in `report.md` rather than leaving a green test that
  asserts nothing.

- **Signature widening was the enabling change, not a cosmetic one.** `(error: string)`
  → `(error?: string)` is what makes "no detail" a legal, type-checked call rather than
  something callers work around by inventing filler text — which is exactly the mistake
  that produced this issue.

## Self-review loop 3 (rev-claude)

- **A test can pin the right contract without pinning the change.** The new `usePerpsToasts` test
  passes on the pre-fix code too — the helper already skipped a falsy detail line. It is still worth
  having (the call site now depends on that contract), but saying so plainly beats letting a green
  suite imply the call-site hunk is covered.
- **Widening a parameter to optional is safe for callers but worth walking anyway.** Checking all
  four `validationError` call sites took seconds and turned "probably fine" into a fact — and
  surfaced that Pro carries the same `errors[0]`-into-telemetry pattern, untouched and out of scope.
- **Evidence quality can improve between loops.** The loop-2 capture carried a "Refreshing…" banner
  over the header; loop 3's re-run is clean. Re-reading the PNG each loop, rather than trusting the
  earlier verdict, is what let that note be closed instead of carried forward.
- **Three loops, each finding strictly less.** Two findings, then one, then none — with each loop's
  fix verified at every write site rather than at the diff hunk. That convergence is the signal that
  the branch is done, not the absence of new ideas to raise.

## Self-review loop 4 (rev-claude, static-code)

- **Checking whether a suppressed error can come back through another door was the one thing worth
  doing.** `skipBalanceError` only removes the *UI-layer* balance message; if
  `HyperLiquidProvider.validateOrder` also reported a balance failure it would land in `errors` and
  re-stack next to the funding message. Reading the provider's `validateOrder` branches
  (`ORDER_PRICE_REQUIRED`, `ORDER_SIZE_MIN`, `ORDER_LEVERAGE_INVALID` — no balance code) closed
  that question in one grep instead of a theory.
- **String-equality de-dup is only as stable as the two producers agreeing.** The view's minimum
  comes from `useMinimumOrderAmount` (market-specific first), the hook's from the network default.
  Both are `10` today — including MYX's `MYX_MINIMUM_ORDER_SIZE_USD` — so the filter holds, but the
  agreement is a coincidence of values, not a structural guarantee. Worth stating as brittleness
  rather than raising as a defect.
- **`isValid` was rewritten, so the other callers had to be re-derived, not assumed.** With
  `skipBalanceError` undefined, `errors.length === 0 && !isBalanceInsufficient` is algebraically the
  old expression, because the insufficient case always pushed an error. Confirming that is what
  makes "no regression for ClosePositionView / PerpsProOrderForm" a statement instead of a hope.
- **Verify a test's loading seam is real before trusting the test.** `mockIsPayQuoteLoading` is only
  meaningful because it flows `useIsTransactionPayQuoteLoading → isPayTotalsLoading →
  isPayStateNotReady`. Tracing that chain distinguishes a test that exercises the fix from one that
  stubs the flag the fix reads.

## Evidence review — the miss that mattered

- **I validated the shape of my fix instead of the truth of the screen.** My acceptance
  criterion was "three stacked messages become one", and the after-capture satisfied it,
  so I passed it — four separate reads. But the single remaining message said
  "Minimum order size is $10" for a token the picker had just offered at **$9.37**, on a
  **$10 order at 2x** where the max notional is $18.74. The screenshot was internally
  contradictory and I never did that arithmetic. **When evidence contains numbers, check
  them against each other before checking them against the AC** — a capture can satisfy
  every assertion in the recipe and still show a broken product.
- **"The user was allowed to select this token" was the tell.** The picker only lists
  fundable tokens. An affordability error on a token the app itself offered is a
  contradiction on its face, and that domain check costs seconds. Recipe assertions
  cannot encode it; a human reviewer spotted it immediately.
- **Two sources for one number is the defect class, not the symptom.** The picker read a
  live balance, the trade screen read a frozen snapshot, and every downstream
  contradiction (dead slider, wrong banner, wrong button label) followed from that split.
  The first fix suppressed the *contradiction between the messages*; only removing the
  second source fixed the *cause*. When two surfaces disagree about one fact, delete a
  source rather than reconcile them.
- **The workaround already existed and was named after the bug.**
  `usePayTokenAccountBalance`'s comment states the exact failure mode. Grepping the
  confirmations `hooks/pay` directory for how the picker got its number would have found
  it in one step, well before I started theorising about RPC 401s.

## Static self-review (rev-codex)

- **Readiness must belong to the value being gated.** Quote loading and AccountTracker
  balance loading can settle independently; naming the former `isPayBalanceLoading`
  hides the mismatch and allows an unavailable balance to become a real zero again.
- **A regression test must cross the boundary where the regression occurred.** Injecting
  the live balance directly into both the source hook and the downstream order context
  means the test cannot detect a wrapper that still passes the stale snapshot.
- **Skipped validation preserves old user-facing state.** Adding a loading guard without
  clearing or categorizing the previous payment method's balance error can leave that
  stale row visible during a transition intended to show no funding message.
- **A passing artifact can still be stale.** The stored trace passes 21 nodes, but its
  embedded focused run contains 10 cases while the current funding-state block contains
  11, so artifact success alone does not establish coverage of the latest follow-up.

## Self-review fix pass 3 — a second reviewer, different lens

- **A readiness proxy is not readiness.** I gated the funding UI on quote/amount
  readiness because that flag was already in the file, and it looked close enough. It
  isn't: the balance source resolves independently and can still be handing back the
  stale snapshot after the quote settles. The fix was to make the balance hook report its
  own `isResolved` rather than inferring it from a neighbour. **When gating on "is X
  ready", the signal has to come from X.**

- **The best fix of the pass deleted a line I had added.** `skipValidation: … ||
  isPayBalanceLoading` was defensive scaffolding that turned out to be both redundant
  (the balance message was already suppressed by category) and harmful (it froze the
  previous payment method's error on screen through the transition). Removing it fixed
  the issue and shrank the diff. Worth checking whether an earlier guard has been made
  obsolete by a later one before adding a third.

- **I knew the live-balance test was weak and shipped it anyway.** I wrote at the time
  that the outer wiring "can't be observed because the context is mocked", then let the
  test stand. The reviewer independently found the same hole. Capturing the props passed
  to `PerpsOrderProvider` took ten minutes, and reverting the wrapper now fails it with
  `Expected: 1000, Received: 0`. **A known-weak test is a finding, not a footnote —
  either strengthen it or delete it.**

- **Two reviewers disagreed and one was wrong.** Reviewer A cleared the duplicated copy
  ("resolves from the test's own mock, not production i18n") and reviewer B flagged it.
  A's mechanism was right, but deriving from `strings(key)` is still better — it asserts
  the component used the intended key, not merely that some text matched. Worth doing on
  the merits rather than to settle the disagreement.

## Static self-review continuation (rev-codex)

- **A readiness flag fixes classification, not the transition by itself.** An
  unresolved-to-resolved funding path needs an explicit rerender test; steady-state
  snapshots cannot expose stale validation state carried across the boundary.
- **Removing one stale-error guard can reveal another stale source.** Validation now
  runs against the fallback Perps balance while the custom-token balance is unresolved,
  and its debounced suppression flag can briefly outlive the fallback that created it.
- **Impossible mock combinations can institutionalize a transient bug.** When the direct
  balance predicate and validation predicate use the same resolved inputs, a test that
  forces them to disagree is documenting stale state, not a valid steady state.
- **Required additive return fields still require contract-wide mock updates.** Runtime
  Jest coverage does not replace TypeScript validation; typed hook mocks must include the
  new field even when their consuming tests do not inspect it.

## Self-review fix pass 4 — a guard that outlived its reason

- **Debounced state and synchronous state must not vote on the same question.**
  `hasSuppressedBalanceError` updates on a debounce; `isPayBalanceLoading` flips the
  instant the balance resolves. Reading both in one memo meant a window where the stale
  one described the old payment method while the fresh one described the new balance —
  and the stale one won. **When combining two signals, check whether they update on the
  same clock.**

- **The fallback had already been made unreachable by a later fix, and I did not
  re-check it.** I added the suppression arm in pass 2 for "payToken undefined". Pass 3
  introduced `isResolved`, which reports `false` in exactly that state — so the memo now
  returned at the loading guard before ever reaching the arm. It could only fire on the
  false-positive case. **Every time a guard is added upstream, the guards downstream of
  it are worth re-reading; one of them may now be dead.**

- **A test can encode an impossible state and thereby hide the bug.** My pass-3 test set
  a resolved sufficient balance *and* a stale suppression flag together — a combination
  production reaches only transiently — and asserted the message appeared. It passed, and
  it was pinning the defect in place. Replacing it with an unresolved→resolved rerender
  turned it into a regression test that fails when the arm is restored.

- **Transpiling is not typechecking.** Three typed mocks were missing the new required
  field and every Jest run stayed green, because Babel strips types. The finding was
  itself a TypeScript gate failure, which is the case the checklist carves out for
  running `lint:tsc` locally — exit 0 confirmed it rather than leaving it to CI.

## Full self-review continuation (rev-codex)

- **A readiness contract is only useful when every authoritative consumer honors it.**
  The screen's direct balance predicates now gate on `isResolved`, but its standard
  blocking alert still reads the fallback value as if it were final, recreating the
  unavailable-as-zero defect through a different render path.
- **Independent error surfaces need an explicit priority contract.** The new funding
  row and the existing confirmation-alert row are each reasonable alone, but their
  independent render predicates allow the same insufficient balance to produce both.
- **Mocking a competing message source to `[]` narrows a test more than its name admits.**
  A test named “states one funding message” must activate every funding-message source
  and count the assembled result; checking one row's text cannot prove uniqueness.
- **Settled visual evidence cannot prove an asynchronous loading edge.** The after image
  is valid for the funded fixture, yet a controlled unresolved state or an alert-hook
  unit test is still required to prove that quote readiness cannot expose stale zero.

## Self-review fix pass 5 — a re-dispatched checklist

- **A reset checklist is not proof of new findings.** The file came back with
  `STATUS: pending` and 11 empty boxes, but the issue text was byte-identical to the
  previous pass and `git log` showed both already fixed. Diffing the issue list against
  the last one, and checking the feedback file's verdict (PASS) and mtime, separated
  "new work" from "re-dispatch" in about a minute. **Read the issues before trusting the
  checkbox state.**

- **No-change still deserves the full gates.** It would have been quicker to read the
  code and signal. Running tests, typecheck, and the recipe on unchanged HEAD is what
  turns "I looked and it's fine" into an evidence-backed disposition — and it is the only
  way to notice if something else drifted since the last pass.

- **The unlock timeout is now a reliable slot symptom, not a signal.** Third pass in a
  row where `ensure_unlocked` timed out inside the recipe while succeeding standalone
  moments later. Relaunch → standalone unlock → re-run is the routine; worth treating as
  known environment noise rather than re-diagnosing each time.

## Self-review fix pass 6 — consolidation I declared but did not finish

- **I claimed "exactly one funding message" while a second row was still rendering.**
  I collapsed the three messages I could see in `PerpsOrderView` and stopped there. The
  confirmation layer's blocking pay-alert row sat a few hundred lines further down and
  described the *same* shortfall from a different source. **When the fix is "show one X",
  grep for every renderer of X rather than fixing the cluster in front of you** — the
  screenshot happened not to have both firing, so the evidence did not contradict me.

- **A readiness flag is only worth as much as its adoption.** Pass 3 added `isResolved`
  and I threaded it through my own derivations, but `useInsufficientPayTokenBalanceAlert`
  reads the same hook and never got it — so the unresolved-balance-as-zero bug survived
  in a surface I had already "fixed". Adding a signal is half the job; finding its
  existing consumers is the other half.

- **Suppressing an error can silently unblock an action.** Gating the alert removed a
  blocking condition from the CTA, which would have left the button enabled on an
  unmeasured balance — a worse failure than the false error. The reviewer caught the pair
  together; fixing one without the other would have been a regression.

- **A default in a shared mock encodes an assumption.** Defaulting
  `usePayTokenAccountBalance` to `isResolved: false` made six unrelated button-enabled
  tests fail once readiness gated the CTA. The loading window is the exception, so the
  default should be the settled state and only the loading tests opt in.

## Full self-review (rev-codex)

- **Independent readiness signals need independent test controls.** The funding helper
  drives quote loading and balance resolution with one boolean, so its green loading
  tests cannot prove which side of the production `A || B` gate protected the UI.
- **A test name is a claim about arranged state, not just asserted output.** The new
  no-quote test says the message appears alongside a funding state but arranges a
  sufficient $1000 balance, leaving the named state absent.
- **Mock restoration after assertions is not teardown.** Because `clearAllMocks` retains
  implementations, restoring shared alert hooks only at the bottom of a passing test can
  turn the first failure into a cascade of misleading failures.
- **Visual proof and state proof can have different confidence levels.** The screenshots
  clearly demonstrate the settled before/after UI, while the unresolved-balance edge
  still depends on unit tests and should not be marked proven until those signals are
  decoupled.

## Self-review fix pass 7 — tests that agreed with me

- **I coupled two inputs in a helper and lost the ability to test either.**
  `isResolved: !isBalanceLoading` was convenient, but it meant "quote settled, balance
  still pending" — the exact window the previous pass was about — could never be
  expressed. A test helper that derives one input from another quietly deletes states
  from the matrix. **Helper parameters should mirror the production inputs, not a
  shorthand for them.**

- **A test name is a claim, and mine was false.** "still surfaces an unrelated no-quote
  failure alongside the funding state" ran with a *sufficient* balance, so the funding
  state never existed and the assertion proved only that a no-quote row renders on its
  own. It passed, and it was covering nothing. Worth re-reading each new test's arrange
  block against its own title.

- **Restoring mocks after the assertions only works when they pass.** I reset the alert
  mocks on the last line of two tests; a failed assertion would have leaked the
  implementation into everything after it and produced confusing downstream failures.
  Teardown belongs in `afterEach`, which runs either way.

- **The repo's own guideline had the answer.** `docs/testing/unit-testing.md:235,250`
  prescribes `not.toBeOnTheScreen()` over `toBeNull()` for absence, and prefers testID
  selection over raw copy. I had written both anti-patterns while quoting other parts of
  that same document earlier in the session.

## Incremental re-review — pass 7 (rev-codex)

- **Independent production gates require independently controllable test inputs.** The
  revised helper can now represent quote-ready/balance-unresolved, so the regression
  test proves the balance gate rather than accidentally relying on quote loading.
- **Coexistence tests must arrange both states they name.** Using an insufficient balance
  in the no-quote case now proves the two distinct messages can render together.
- **Guaranteed teardown and centralized test IDs remove avoidable test brittleness.** The
  fixes use `afterEach` restoration, localized expectations, and a shared identifier
  instead of cleanup-after-assertion or raw-copy selection.
- **A fix-only range keeps an incremental review honest.** Comparing the prior review
  commit to the worker's current commit was sufficient to verify all six findings
  without reopening unchanged implementation decisions.
