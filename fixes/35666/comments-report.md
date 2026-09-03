# Comments report — PR #35666

## PR context

Non-blocking far-from-market warning for Pro limit and scale prices (>5% from near-touch). Place stays enabled. Reduce-only skipped. Crossing-the-market is TAT-3904, out of this PR.

## Fetched comments

### Actionable

| # | Source | Author | File | Content |
|---|--------|--------|------|---------|
| 1 | review_comment 3921505031 | cursor[bot] | usePerpsProOrderForm.ts:2967 | Scale warning fires mid-keystroke: `hasScaleValidationInteraction` is set in `onStartPriceChange`/`onEndPriceChange`, so a partial start such as `8` can still produce a successful ladder and fire the banner + telemetry. Limit path uses `hasBlurredLimitPrice`. |
| 2 | issue_comment 5521208683 | github-actions[bot] | usePerpsProOrderForm.test.ts / limitPriceFarFromMarket.test.ts | Flaky-test detection: J9 (module-level lets), J10 (spyOn without restoreAllMocks), J3 (missing clearAllMocks). Historical failure rate 0/170–0/431. |

### Skipped status-only (4, no reply)

| id | author | why skipped |
|----|--------|-------------|
| 5521150818 | github-actions[bot] | CLA signature |
| 5521172212 | metamask-ci[bot] | PR template workflow (changelog prefix / unchecked Android box). Not a code review comment. |
| 5521234163 | github-actions[bot] | Smart E2E selection |
| 5521401204 | github-actions[bot] | Performance results (all passed) |

No REQUEST_CHANGES reviews. cursor[bot] review 5098298968 is a COMMENTED summary of comment 1, not a separate finding. No existing replies on the inline thread.

## Triage

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | cursor[bot] | usePerpsProOrderForm.ts:2967 | REAL | Gate scale far-from-market on start/end blur, matching `hasBlurredLimitPrice`. Reset the flag on start/end change so a later edit does not warn mid-keystroke. |
| 2a | github-actions[bot] | usePerpsProOrderForm.test.ts:57 | FALSE POSITIVE | J9: `beforeEach` already resets all 25 module-level lets plus `mockOrderForm` / `mockValidation` fields. Bot claimed only type/direction/executionOptions are reset. |
| 2b | github-actions[bot] | usePerpsProOrderForm.test.ts:5800 | FALSE POSITIVE | J10: both `splitScaleSizes` spies already call `mockRestore()` in the same test; override is `mockImplementationOnce`. File-wide `restoreAllMocks` is pre-existing hygiene, not this PR. Historical rate 0. |
| 2c | github-actions[bot] | limitPriceFarFromMarket.test.ts:7 | FALSE POSITIVE | J3: the `toHaveBeenLastCalledWith` assertion runs after that test's own `strings()` call, so last-call is always from the current test even under `--randomize`. No `toHaveBeenCalledTimes` in the file. Historical rate 0. |

## Inherited recipe AC coverage

Family recipe `artifacts/recipe.json` (TAT-3897 scale/limit fat-finger warning). 6/6 ACs proven by state:

| AC | Claim | Nodes |
|----|--------|-------|
| AC1 | Scale long farthest endpoint >5% below bid warns | helper + hook tests |
| AC2 | Scale short farthest endpoint >5% above ask warns | helper tests |
| AC3 | Limit far below bid warns | helper + hook tests |
| AC4 | Exactly 5% does not warn | helper + hook tests |
| AC5 | Reduce-only skips warning | helper tests |
| AC6 | Place stays enabled | hook tests + live `wait-place` |

Live graph also unlocks, opens BTC Pro, selects Scale, and screenshots the Scale form. Banner pixels are not captured (`ui.set_input` cannot type scale prices). The new blur-gate tests live in the hook suite the recipe already runs (`-t 'far-from-market'`).

## Recipe re-validation

PASS. `mm-harness run` exit 0, `status: pass`. Report: `artifacts/recipe-run/report.md`. Side-findings: 10 ambient application warnings, 0 errors.

## Replies

- review_comment 3921505031: replied + thread resolved
- issue_comment 5521208683: consolidated flaky-test triage posted (https://github.com/MetaMask/metamask-mobile/pull/35666#issuecomment-5521967622)
- 4 status-only comments: no reply

## Summary

- Total comments: 6 (1 REAL, 1 FALSE POSITIVE issue-comment covering 3 findings, 4 OUT OF SCOPE / skipped status-only)
- Actionable triage: 1 REAL, 3 FALSE POSITIVE findings, 0 OUT OF SCOPE among review findings
- Commit SHA for fixes: `2aee82c273871995a29fd027bae8796bdde4b1d2`
- Files changed:
  - `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.ts`
  - `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts`
  - `app/components/UI/Perps/utils/limitPriceFarFromMarket.test.ts` (tsc: mockStrings arity)
- Recipe re-validation: PASS
- Integration status: rebased
