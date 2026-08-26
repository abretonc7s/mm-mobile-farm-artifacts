# PR 34789 interactive re-entry report

## Outcome

Final HEAD is `07560cece3ce41d81571a737b589c9fa8b2e850c`. The PR diff is restricted to seven files and 999 counted changed lines. The latest cleanup commit changes only three test files; production remains identical to the independently approved `de6bb9a9bb7` behavior. The operator explicitly requested the push; local branch, origin branch, and PR #34789 head were verified at the same final SHA. The priority remains the minimal TAT-3742 Perps fix; broader confirmations work is not a prerequisite or follow-up obligation.

No GitHub reply, thread resolution, review-queue entry, or terminal completion signal was created.

## Comments handled

- `3838984434` (`matthewwalsh0`): REAL and fixed locally. Restored the existing Pay With row `Box` layout; only the balance-related hunk remains versus the PR base.
- `3838998505` (`matthewwalsh0`): REAL and fixed locally. Removed `useIsPayTokenBalanceUnresolved`, its unit suite, Footer integration/test, and CustomAmountInfo integration/test. Perps continues to fail closed through its local `isPayBalanceLoading`/`hasInsufficientPayTokenBalance` gates.
- Earlier review findings are classified with current-head evidence in `comments-report.md`; all other REAL findings were already fixed and resolved, and the human flaky-test report is retained as first-class `FALSE_POSITIVE` evidence.

## Final seven-file scope

- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx`
- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.test.tsx`
- `app/components/UI/Perps/hooks/usePerpsOrderForm.test.ts`
- `app/components/UI/Perps/hooks/usePerpsOrderValidation.ts`
- `app/components/UI/Perps/hooks/usePerpsOrderValidation.test.ts`
- `app/components/Views/confirmations/hooks/pay/usePayTokenAccountBalance.ts`
- `app/components/Views/confirmations/hooks/pay/usePayTokenAccountBalance.test.ts`

Final diff: 932 additions and 67 deletions, 999 counted changed lines. The final cleanup commit is test-only and preserves every distinct regression assertion identified by the internal review.

## Validation

- `git diff --check` — PASS.
- Final affected Jest: PASS — 3 suites / 194 tests; after the last row-specific test correction, `usePerpsOrderValidation.test.ts` also passed 37/37 at exact final content. Existing non-failing React `act()` warnings remain.
- `NODE_OPTIONS='--max-old-space-size=8192' yarn lint:tsc` — PASS, exit 0, no diagnostics.
- `yarn format:check` — PASS: all matched files use Prettier style.
- Scoped ESLint on final cleanup: PASS with 0 errors; the wider seven-file check reports only warnings that predate the merge base.
- Scoped Prettier and `git diff --check`: PASS.
- Component-view suite: PASS — 5/5 tests. TypeScript: PASS with 8 GB heap.
- Internal sub-agent review: APPROVE at `07560cece3c`; all five cleanup coverage findings restored, no production cleanup changes.
- `check-pr-max-lines`: PASS at 999 changed lines.

## Recipe result

The trusted inherited 21-node recipe was reused without syntax migration. Harness launch and post-launch verification passed, but the post-change recipe run is BLOCKED at `setup-unlock`: 1/2 executed nodes passed, then the wallet action timed out waiting for the Login password field.

Standalone unlock and one visible “Try again” recovery reproduced the blocker. The Login error boundary and Metro log report:

`Invariant Violation: new NativeEventEmitter() requires a non-null argument`

The stack starts at `ScreenshotDeterrentWithNavigation`, indicating the installed iOS dev client is incompatible with the native module expected by the current JS bundle. No fixture reset was attempted because this is not a wallet-data failure. The failed current run is in `artifacts/recipe-run/`; `latest-valid-recipe-run.json` still points to the inherited family evidence and no fresh success is claimed.

## Remaining operator work

1. Review CI for pushed HEAD `07560cece3c`.
2. Post the suggested replies from `comments-report.md` and resolve the two human threads when satisfied.
3. Keep the optional confirmations drafts non-blocking; their owners may revise or close them.
4. Keep this interactive task open until the operator explicitly requests terminal completion.

## Non-blocking confirmations handoff

- Independent draft PR #35220 preserves the Pay With row design-system migration from `main`.
- Stacked draft PR #35221 preserves the general confirmation balance-resolution approach on top of PR 34789's balance contract.
- Both drafts are confirmations-owned references and are explicitly non-blocking for PR 34789. Confirmations can investigate, revise, or close them; we can provide context or validation help if requested.
- Reviewer-driven scope and ownership lessons are captured in `artifacts/learnings.md`.

## PR description

PR 34789's GitHub description now leads with the minimal Perps bug and its validation. A separate scope section links drafts #35220 and #35221 as confirmations-owned, non-blocking references that may be revised or closed.
