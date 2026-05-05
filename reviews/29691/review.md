# PR Review: #29691 — fix: resolve `ORDER_PRICE_REQUIRED` error on perps position flip

**Tier:** standard

## Summary
The runtime change is aligned with the stated goal: `placeOrder` now fetches asset info/live price before provider-level validation, validates against `effectivePrice`, and keeps trading readiness/signing setup after validation. However, the affected Jest suite currently fails, so this PR is not ready to merge.

## Recipe Coverage
Recipe decision: skipped (`skip-backend-only`). The acceptance criteria are provider/order-placement behavior with no direct UI-visible claim; standard-tier smoke validation used code review, Jest, CDP provider probing, screenshot evidence, and Metro monitoring instead.

| # | AC | Status | Rationale |
|---|----|--------|-----------|
| 1 | "TradingService.flipPosition() deliberately omits currentPrice from the order params it passes to provider.placeOrder() — passing a stale entry price would corrupt IOC slippage calculation." | UNTESTABLE | Standard-tier recipe skipped: backend/controller behavior, no generated UI recipe. |
| 2 | "placeOrder() was running #validateOrderBeforePlacement before fetching the live price, so the minimum-USD check had no price to work with and threw ORDER_PRICE_REQUIRED on every flip." | UNTESTABLE | Standard-tier recipe skipped: backend/controller behavior, no generated UI recipe. |
| 3 | "Fix: reorder placeOrder() so #getAssetInfo runs first, compute effectivePrice (live price, or caller-supplied price if present), then pass it into #validateOrderBeforePlacement." | UNTESTABLE | Standard-tier recipe skipped: backend/controller behavior, no generated UI recipe. |
| 4 | "#ensureReadyForTrading stays after validation, so invalid orders never trigger builder-fee / DEX-abstraction signature prompts unnecessarily." | UNTESTABLE | Standard-tier recipe skipped: backend/controller behavior, no generated UI recipe. |
| 5 | "effectivePrice is hoisted above the try block so the $10-minimum retry path can also use the fetched price when the caller omits currentPrice — without this, a flip order that hit the $10 edge case would fail silently instead of retrying." | UNTESTABLE | Standard-tier recipe skipped: backend/controller behavior, no generated UI recipe. |
| 6 | "No changes to TradingService.flipPosition — the intentional omission of entryPrice is correct and preserved." | UNTESTABLE | Standard-tier recipe skipped: backend/controller behavior, no generated UI recipe. |

Overall recipe coverage: 0/6 ACs PROVEN
Untestable: AC1-AC6, standard-tier backend-only recipe skip.

## Prior Reviews
No prior reviews.

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | `flipPosition` omits current price intentionally. | PASS | Code review: no `TradingService.flipPosition` changes in PR diff. |
| 2 | Previous `ORDER_PRICE_REQUIRED` ordering bug is addressed. | PASS | `HyperLiquidProvider.ts:3566-3594` fetches live price before provider validation and passes `currentPrice: effectivePrice`. |
| 3 | Effective price prefers caller price, otherwise fetched price. | PASS | `HyperLiquidProvider.ts:3573-3577`. |
| 4 | Signing readiness stays after validation. | PASS | `HyperLiquidProvider.ts:3587-3599`. |
| 5 | $10 retry can use fetched price when currentPrice is omitted. | PASS | `HyperLiquidProvider.ts:3721-3729`; affected retry test passes, but suite still fails elsewhere. |
| 6 | `TradingService.flipPosition` remains unchanged. | PASS | PR diff only touches `HyperLiquidProvider.ts` and `HyperLiquidProvider.test.ts`. |

## Code Quality
- Pattern adherence: Provider flow uses existing helpers and preserves error mapping.
- Complexity: Minimal ordering change; no new abstraction.
- Type safety: Typecheck reports unrelated existing `Input` prop errors, none in PR files.
- Error handling: Existing `#handleOrderError` path is preserved.
- Anti-pattern findings: No new mobile imports, analytics magic strings, Sentry concerns, or subscription leaks found in changed code. The updated test at `HyperLiquidProvider.test.ts:2845` is failing because its mock setup does not clear the default WebSocket cached BTC price before asserting missing REST price behavior.

## Fix Quality
- **Best approach:** Pragmatic and minimal for this PR. Fetching the live price before validation is the right boundary because `validateOrder` needs a price for size-based market orders, while `#ensureReadyForTrading` remains after validation to avoid signing prompts for invalid orders.
- **Would not ship:** The affected Jest suite fails. Fix `HyperLiquidProvider.test.ts:2845` by making the missing-price test actually simulate a cache miss, e.g. clear `mockSubscriptionService.getCachedPrice` before `allMids` returns `{}`.
- **Test quality:** New positive tests cover the flip-shaped params and $10 retry path, but the modified missing-price regression currently fails and does not exercise its stated condition.
- **Brittleness:** The failure is mock-coupling: the default `getCachedPrice('BTC')` mock returns `50000`, so changing only `allMids` to `{}` is insufficient.

## Live Validation
- Recipe: skipped (`skip-backend-only`)
- Result: PASS for smoke navigation/CDP probe; FAIL overall due affected Jest suite
- Video: `review.mp4`
- Native changes: none
- Metro errors: no PR-specific perps placement errors. Tail included pre-existing/runtime warnings and one self-inflicted `NAVIGATE --help` warning from probing the script.
- Log monitoring: 30 seconds monitored during validation, saved to `artifacts/evidence/metro-monitor-step16.log`.

## Correctness
- Diff vs stated goal: aligned.
- Edge cases: Missing-price edge case test currently fails; this blocks confidence.
- Race conditions: none identified in the changed ordering.
- Backward compatibility: Preserved for caller-supplied `currentPrice`; positive `params.currentPrice` still wins over fetched price.

## Static Analysis
- lint:tsc: FAIL — unrelated existing `Input` prop errors in view files; no PR-file type errors.
- Tests: FAIL — `yarn jest app/controllers/perps/providers/HyperLiquidProvider.test.ts --no-coverage` failed 1 test (`handles missing price data`), 324 passed, 36 skipped.

## Architecture & Domain
The provider file and its test file both exceed the review guardrail hard limit by a wide margin (`HyperLiquidProvider.ts` 8,627 lines; `HyperLiquidProvider.test.ts` 10,619 lines). This PR does not materially worsen that by itself, but the task guardrail requires flagging touched files above 2,500 lines.

## Risk Assessment
MEDIUM — The implementation is narrow and logically correct, but the affected test suite failure means regression coverage is currently broken.

## Recommended Action
REQUEST_CHANGES

Fix the failing `handles missing price data` test and rerun the affected Jest suite before merge. The oversized provider/test files should also be split per the review guardrail.
