# PR 34789 comment triage

## Final local-only verification

- Final HEAD: `07560cece3ce41d81571a737b589c9fa8b2e850c`; local branch, origin branch, and PR #34789 head were verified at this SHA after the operator-authorized push.
- Final scope: exactly seven PR files; the last cleanup touches only three test files and no production file.
- Final size: 932 additions + 67 deletions = 999 counted changed lines.
- Validation: 194/194 affected tests passed, the final validation-only correction passed 37/37, scoped ESLint/Prettier and `git diff --check` passed.
- Internal sub-agent verdict: APPROVE; all five test-coverage regressions found during consolidation were restored.
- The final commit was pushed only after explicit operator authorization. No GitHub reply/thread was changed, and no terminal completion signal was written.

## Reloaded context

- Inherited context: Farmslot family `9da27bd0-481b-42cd-9cc3-8a2b6807543e` for TAT-3742, resolved from the parent run.
- Original scope: fix lite-mode pay-with-token error handling, action-button visibility, slider usability, and the below-$10 state.
- Prior diagnosis: the order screen consumed a stale `payToken.balanceUsd` snapshot while the picker consumed a reactive account balance. Follow-up passes added explicit balance readiness, consolidated duplicate funding surfaces, kept the CTA disabled while the balance is unknown, and strengthened transition/integration tests.
- Trusted recipe: `artifacts/recipe.json`, byte-identical to the inherited parent recipe. It has 21 nodes and covers four inferred acceptance criteria: one non-contradictory funding message, a reachable place-order button, a usable slider while balance is unresolved, and the minimum-order message for a resolved below-minimum balance.
- Prior proof: 21/21 recipe nodes passed, the focused and affected test suites passed, TypeScript passed, and the packaged before/after evidence was quality-reviewed as PASS. AC1/AC2 use mixed/visual proof; AC3/AC4 use focused state tests.
- Missing inherited artifact: recipe library. This is not required to reuse the seeded trusted recipe.

## Live comment triage

Classifications are against current head `df4752e9e723f7a79c94a08519f9523613c1360f`, including replies and current thread state.

| Comment | Author | Classification | Current disposition |
| --- | --- | --- | --- |
| `3781582063` — Place Order ignores a live token shortfall during the validation debounce | `cursor[bot]` | `REAL` | Fixed and resolved. Both Place Order variants synchronously gate on `hasInsufficientPayTokenBalance`; a regression test covers the resolved-shortfall/stale-validation window. |
| `3781855756` — fee alerts skip a known raw balance while USD is missing | `cursor[bot]` | `REAL` | Fixed and resolved. Fee validation gates on `balanceRaw !== undefined`, independently of USD readiness, with a regression test. |
| `3783645243` — represent unresolved balances with the existing properties rather than extra readiness flags | `matthewwalsh0` | `REAL` | Fixed and resolved. `usePayTokenAccountBalance` returns `undefined` for unresolved USD/raw values and preserves a measured zero as `'0'`. |
| `3793297994` — do not fall back to the selected-token snapshot because it may belong to the original account | `matthewwalsh0` | `REAL` | Fixed and resolved. The preferred-token path no longer reads the selected-token balance snapshot; its required display value falls back to zero when the live value is unresolved. |
| `3793303225` — ensure unresolved balances fail closed | `matthewwalsh0` | `REAL` | The Perps CTA is correctly fail-closed via `isPayBalanceLoading`. The later owner review (`3838998505`) establishes that broad standard-confirmation gating is unnecessary because those flows already wait for quotes; that overbroad follow-up has been removed locally. |
| `3793304361` — avoid an account-override-unsafe balance fallback in Pay With row | `matthewwalsh0` | `REAL` | Fixed and resolved. The row formats unresolved live balance as zero and does not use the pay-token snapshot. |
| `3815225399` — a previous generic balance error persists during the debounce after switching payment method | `cursor[bot]` | `REAL` | Fixed and resolved. Validation records its generic balance error and filters it immediately when `skipBalanceError` flips, without waiting for the next debounced run. |
| `3831856026` — all standard confirmation continue paths can fail open while the balance is unresolved | `cursor[bot]` | `FALSE_POSITIVE` | Superseded by the confirmation owner’s current review: standard deposit confirmations already block until a quote is available. Perps has its own explicit unresolved-balance CTA gate. The global hook/Footer/CustomAmount response expanded scope and has been removed locally. Any further investigation belongs to confirmations and does not block this PR. |
| `3838984434` — design-system migration is out of scope | `matthewwalsh0` | `REAL` | Open and actionable. Revert only the `Box` import/layout migration in `pay-with-row.tsx`; keep balance-related behavior. |
| `3838998505` — scope has grown into standard Footer and CustomAmount confirmation components | `matthewwalsh0` | `REAL` | Open and actionable. Remove `useIsPayTokenBalanceUnresolved` and its global consumers/tests; retain `usePayTokenAccountBalance`’s explicit missing state and the Perps CTA gate. |

### Human conversation regression report

Comment `5299847404` classified the four flaky-test suggestions below. Each is `FALSE_POSITIVE`:

- PerpsOrderView J6: `setTimeout(0)` deliberately flushes this file’s timer-backed `requestAnimationFrame` within `act`; it is not a DOM sleep. Historical failure rate was 0/360 when triaged and is 0/429 in the latest bot sample.
- PerpsOrderView J9: the top-level setup and nested teardown cover the mutated pay mocks; Jest still runs ancestor `beforeEach` hooks for focused/nested tests.
- usePerpsOrderValidation J8: the suite explicitly advances its debounce timer before `fastWaitFor`; the flagged fake-timer combination is pre-existing and has no historical failures.
- usePerpsToasts J9: both module-level variables are reset in `beforeEach`; a failed test does not skip the next test’s `beforeEach`.

### Informational automation comments

- CLA status, Smart E2E selection, and Sonar quality-gate comments: `OUT_OF_SCOPE` informational status only.
- Performance result `5373302120`: `OUT_OF_SCOPE`; the non-blocking failure reason is `no_performance_metrics`, not an observed performance regression, and the Perps Add Funds performance test passed.
- Flaky detector Footer J3: `FALSE_POSITIVE`; `jest.clearAllMocks()` clears usage data but does not erase mock implementations/return values.
- Flaky detector Footer J10: `OUT_OF_SCOPE`; the flagged spy hygiene is pre-existing and outside changed behavior. The later scope fix removes this PR’s Footer test hunk entirely.
- The three blank-body `CHANGES_REQUESTED` reviews are review-state containers; their substantive inline comments are classified above.

## Minimal fixes applied

1. Reverted the unrelated `Box`/Tailwind migration in `pay-with-row.tsx`.
2. Removed `useIsPayTokenBalanceUnresolved`, its tests, and its Footer/CustomAmount consumers/tests.
3. Preserved the explicit unresolved balance values, alert readiness guards, Perps funding-message cleanup, live-balance wiring, and Perps CTA gating.

## Validation results

### Local checks

- Targeted Jest: PASS — 9 suites, 446 tests, 0 failures, 0 snapshots. Existing React `act()` and selector-stability console warnings remain non-failing.
- TypeScript: PASS — `NODE_OPTIONS='--max-old-space-size=8192' yarn lint:tsc` exited 0 with no diagnostics.
- Formatting: PASS — `yarn format:check` reported all matched files use Prettier style.
- Scoped ESLint: 0 errors, 10 warnings; `--max-warnings=0` therefore exited 1. All ten are `@typescript-eslint/no-deprecated` warnings on legacy `Box`: six in CustomAmountInfo, which is restored byte-for-byte to the PR base, and four in the Pay With layout the open human review explicitly requires restoring. The final diff versus the PR base changes only balance formatting in that row, not those layout sites.

### Inherited recipe re-validation

- Trusted recipe provenance was rechecked: `artifacts/recipe.json` is byte-identical to the family-inherited recipe. No compatibility migration was required.
- Harness readiness: `doctor` required checks passed; initial runtime was cold. `mm-harness launch ios` rebuilt the bundle for this checkout and established the bridge; the post-launch `mm-harness verify --json` passed.
- Post-change run: BLOCKED — `artifacts/recipe-run/summary.json` reports 1/2 executed nodes passed. `setup-status` passed; `setup-unlock` timed out after 30 seconds waiting for the password input (`WALLET_STATE_REQUIRED`).
- Bounded recovery: standalone `metamask.wallet.ensure_unlocked` failed identically. A native screenshot showed the Login error boundary, not a missing fixture. One visible `Try again` press returned to the same error.
- Exact runtime blocker: the current JS bundle throws `Invariant Violation: new NativeEventEmitter() requires a non-null argument` in `ScreenshotDeterrentWithNavigation` on the Login screen (`temp/recipe/runtime/metro.log`). This indicates the installed iOS dev client is missing/incompatible with the native module expected by this checkout. Resetting the disposable wallet fixture would not address the native mismatch and was not attempted.
- Result: no post-change recipe success is claimed. `latest-valid-recipe-run.json` intentionally remains pointed at the inherited family evidence package; the failed current run remains under `artifacts/recipe-run/` for diagnosis.

## Operator handoff

- The scoped rollback and test-only size consolidation are committed and pushed. Local and remote PR head are `76f51c552eddf742c5ade4e86bf42f4e74c112cc`.
- GitHub draft PRs #35220 and #35221 were created as confirmations-owned references. No replies were posted, no threads were resolved, and neither draft was added to the review queue.
- Suggested reply for `3838984434`: “Addressed: reverted the Pay With row design-system migration from this PR. The final diff keeps the existing layout and changes only unresolved balance formatting here. The optional cleanup is preserved separately in confirmations draft #35220; it is non-blocking and can be revised or closed by that team.”
- Suggested reply for `3838998505`: “Addressed: removed `useIsPayTokenBalanceUnresolved` and its Footer/CustomAmount consumers and tests. The explicit `undefined` contract remains in `usePayTokenAccountBalance`, and only the Perps CTA gates on its unresolved balance state. The broader approach is preserved for reference in confirmations draft #35221 and does not block this PR.”
- After reviewing the pushed diff, the operator can post the suggested replies and resolve those two threads.
- PR 34789's description now explains the minimal Perps scope and links #35220/#35221 as confirmations-owned, non-blocking drafts.
- Runtime follow-up: install/build an iOS dev client compatible with `ScreenshotDeterrentWithNavigation`, relaunch `mm-2`, and rerun `artifacts/recipe.json` into `artifacts/recipe-run/`. Do not promote the current failed run.
- Lint follow-up: accept the ten base `Box` deprecation warnings for this scoped PR or migrate them in a separate design-system change; the open review explicitly rejects doing that migration here.
- Confirmations ownership: draft #35220 independently preserves the design-system migration, and stacked draft #35221 preserves the general unresolved-balance approach. Confirmations may investigate, revise, ask us for help, or close either draft. Neither blocks the minimal TAT-3742 fix or its merge.
