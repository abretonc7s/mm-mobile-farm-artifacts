# PR #34789 review-comment triage

Context reviewed: live PR description, TAT-3742 ticket snapshot and comments, the complete `origin/main...HEAD` diff, all live root review threads, general PR comments, and `CHANGES_REQUESTED` reviews.

| # | Source / ID | Author | File | Triage | Action |
|---|---|---|---|---|---|
| 1 | issue_comment 5290199503 | github-actions[bot] | conversation | OUT OF SCOPE | Routine CLA status; no reply. |
| 2 | issue_comment 5290235689 | github-actions[bot] | PerpsOrderView.test.tsx; usePerpsOrderValidation.test.ts | FALSE POSITIVE | J6 flushes this suite's timer-backed `requestAnimationFrame` inside `act`; J9 mutations are restored by the owning describe's `afterEach`; J8 advances the SUT debounce before observing the settled result. The existing consolidated response (5299847404) already records this triage, so do not duplicate it. |
| 3 | issue_comment 5290647503 | abretonc7s | conversation | OUT OF SCOPE | Previous worker report; status-only, no reply. |
| 4 | issue_comment 5299847404 | abretonc7s | conversation | OUT OF SCOPE | Existing response to the flaky-test bot; status-only, no reply. |
| 5 | issue_comment 5299855089 | github-actions[bot] | conversation | OUT OF SCOPE | Informational test-selection output; no reply. |
| 6 | issue_comment 5299865719 | abretonc7s | conversation | OUT OF SCOPE | Previous worker report; status-only, no reply. |
| 7 | issue_comment 5299938577 | sonarqubecloud[bot] | conversation | OUT OF SCOPE | Passing quality-gate summary; no reply. |
| 8 | issue_comment 5299967679 | metamask-ci[bot] | PR template | OUT OF SCOPE | Informational PR-template status; recipe evidence is revalidated by this task, while attachment/upload is outside the review-fix commit. No reply. |
| 9 | issue_comment 5299978971 | github-actions[bot] | conversation | OUT OF SCOPE | Non-blocking performance run with no green main baseline and a `no_performance_metrics` infrastructure failure; no reply. |
| 10 | review_comment 3793297994 | matthewwalsh0 | app/components/Views/confirmations/hooks/pay/usePayWithPreferredToken.ts:49 | REAL | Remove the unsafe `selectedToken.balanceUsd` fallback; unresolved live balance must fall back to zero without reading the original transaction/account snapshot. |
| 11 | review_comment 3793303225 | matthewwalsh0 | app/components/Views/confirmations/hooks/alerts/useInsufficientPayTokenBalanceAlert.ts:139 | FALSE POSITIVE | The lite-mode Place Order CTA explicitly includes `isPayBalanceLoading` in both button variants, and the regression test `disables the place order button while the balance is unresolved` pins the guard. This preserves the ticket requirement to avoid claiming an unmeasured zero balance. |
| 12 | review_comment 3793304361 | matthewwalsh0 | app/components/Views/confirmations/components/rows/pay-with-row/pay-with-row.tsx:217 | REAL | Remove the unsafe `payToken.balanceUsd` fallback and render zero until the override-aware live account balance resolves. |

Skipped without reply: 8 routine/status-only comments (rows 1, 3–9). The flaky-test summary already has a consolidated response, so it will not receive a duplicate reply.

## Inherited acceptance-criteria coverage

The trusted family-inherited recipe covers all four TAT-3742 outcomes:

- AC1 (mixed): after switching to a wallet token, the Perps-balance warning and false `Available: $0` row are absent; the screenshot captures the resulting single-message-or-no-message state.
- AC2 (visual): the Place Order CTA remains present through payment-method selection and settling, with screenshot evidence for viewport reachability.
- AC3 (state): the focused `pay with token funding state` Jest block verifies the slider remains usable while the live balance is unresolved.
- AC4 (state): the same focused tests verify a resolved token below the protocol minimum shows the minimum-order message and disables the slider for that reason.

Post-rebase recipe result: **PASS** — 21/21 nodes passed in 52 seconds after one automatic mobile-runtime recovery. The screenshot was inspected at original resolution: the wallet-token payment method is selected, no contradictory funding/zero-balance error is visible, the slider remains rendered, and the Long ETH CTA is present in the viewport. The nine non-blocking console diagnostics are unrelated runtime noise (TradingView load/circuit-breaker warnings, an existing selector warning, an invalid Fragment prop warning, and a reverted read call); none correspond to the two review fixes or failed recipe assertions.

## Final summary

- Total comments: **12** (**2 REAL, 2 FALSE POSITIVE, 8 OUT OF SCOPE**).
- Fix commit: `5632184c17416068b2d51f44b637994238e3dec5`.
- Integration status: **rebased** onto `origin/main`; two `PerpsOrderView.tsx` conflicts were reconciled and the force-with-lease push published the linear history.
- Recipe re-validation: **PASS** (21/21 nodes, screenshot inspected).
- Review threads: all three current human threads replied to and resolved. The flaky-test issue comment already had a consolidated response, so no duplicate top-level reply was posted.
- Local validation: changed-file ESLint with zero warnings, `yarn lint:tsc`, `yarn format:check`, the checklist-selected five test files, and the two directly changed suites all passed. Directly changed suites: 2 suites / 33 tests.

Files changed in the review-fix commit:

- `app/components/Views/confirmations/hooks/pay/usePayWithPreferredToken.ts`
- `app/components/Views/confirmations/hooks/pay/usePayWithPreferredToken.test.ts`
- `app/components/Views/confirmations/components/rows/pay-with-row/pay-with-row.tsx`
- `app/components/Views/confirmations/components/rows/pay-with-row/pay-with-row.test.tsx`

The pay-with-row file's four legacy `Box` usages were migrated to the design-system `Box` API because the mandatory changed-file ESLint gate treats its pre-existing deprecation warnings as failures under `--max-warnings=0`; this was a local mechanical cleanup with unchanged layout classes.
