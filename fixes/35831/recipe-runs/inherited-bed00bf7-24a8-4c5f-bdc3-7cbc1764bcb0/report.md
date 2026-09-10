# CI second-pass triage

Reviewed current Mobile HEAD fc11c3ec0cc41173543e6b7f7b9ebdd9d545439c, matching the flaky-test bot analysis. All ten current unit-test shards pass. Read full current lint:tsc and label-check logs, inline comments and conversation comments. Historical zero failure rates are not the basis for the findings below.

- OUT OF SCOPE / dependency: lint:tsc has exactly four TS2339 errors at translatePerpsError.ts:77/79/81/83 for ORDER_MARGIN_MODE_* constants absent from the committed registry package. Core #10136 is still OPEN and unmerged at c99b20455. Preserve the user-approved merge → release → Mobile dependency update/revalidation sequence.
- FALSE POSITIVE as a lint code failure: current lint job 101985286127 is CANCELLED. No code diagnostic is supplied; this is not evidence of an ESLint violation.
- OUT OF SCOPE / intentional gate: check-pr-labels rejects blocked. The prerequisite remains unresolved, so keep the label.
- Bot 5581571760, J4 PerpsPositionsView: FALSE POSITIVE. TypeScript AST inspection found 16 waitFor calls, all with expect assertions and none empty. The cited empty callback at line 56 does not exist.
- Bot J4 PerpsCrossMarginInfoButton: FALSE POSITIVE. This file neither imports nor calls waitFor; its modal tests use fireEvent and direct assertions. The proposed source snippet does not exist.
- Bot J3 PerpsProPositionCard: FALSE POSITIVE. beforeEach at lines 35–38 clears call state and restores useSelector(false). Both test-specific selector overrides are restored by that setup. resetAllMocks is not required after clearAllMocks.
- Bot J3 PerpsCard: FALSE POSITIVE. beforeEach at lines 69–93 clears calls and restores both mutable return values: privacy selector and markets. Blanket resetAllMocks would also erase the stable event-tracking factory, which is deliberately preserved.
- Bot J3 PerpsPositionCard: FALSE POSITIVE. beforeEach at lines 206–259 clears calls and reinstates theme, PnL, markets, prices and selector behavior. The suite retains hook factories for TP/SL and close actions; blanket reset would erase these defaults. No implementation leak is identified by the suggestion or the source audit.
- Other conversation automation is status-only; no inline review comments. Reply once to the actionable flaky-test comment, with all five dispositions and source evidence.

No REAL new code finding. Follow step 4 no-change path: do not rerun local code gates, tests or financial fixtures, do not commit/push, and retain existing local yalc transport edits and pre-existing .codex. Earlier validation evidence remains historical, not a new execution claim.

## Outcome and evidence

No code or dependency changes, no commit/push, and no local tests or runtime recipes rerun on this no-change path. HEAD remains fc11c3ec0cc41173543e6b7f7b9ebdd9d545439c. Local yalc edits and .codex are unchanged. Existing CI unit results are current remote evidence; earlier local validation is preserved in ci-fix-first-report.md, not claimed as a new run.

Posted the consolidated five-finding response: https://github.com/MetaMask/metamask-mobile/pull/35831#issuecomment-5581695034

Evidence files: ci-fix-second-review.json, ci-fix-second-comments.json, ci-fix-second-checks.json, ci-fix-second-core.json, ci-fix-second-mobile.json, ci-fix-second-tsc.log, ci-fix-second-labels.log, ci-fix-second-waitfor-audit.json and ci-fix-second-bot-reply.md. The waitFor audit parses the current TSX syntax tree and lists every call with its assertion and empty-body checks. Mock lifecycle was checked directly in all three cited suites.

Core must merge and publish a controller release before Mobile adopts it and revalidates. The blocked label stays in place. Other remote checks were still running at the captured snapshot; no claim that all CI passes.
