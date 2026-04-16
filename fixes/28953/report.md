# Report: TAT-2971 — Fix perps historical-candle cancellation handling

## Summary

AbortErrors from candle fetch cancellations (during normal navigation/view teardown) were treated as real errors and logged to Sentry at 3 service layers. Added `isAbortError()` utility and abort guards at all 3 catch blocks to suppress expected cancellation noise while preserving real error reporting.

## Root cause

`HyperLiquidClientService.subscribeToCandles()` (line 593) creates an AbortController whose signal is passed to `fetchHistoricalCandles` (line 609). On cleanup, `abort()` fires (line 755). The `fetchHistoricalCandles` catch block at line ~536 logs to Sentry BEFORE the caller's abort check at line 712-714 can suppress it. The error then propagates through `MarketDataService.fetchHistoricalCandles` (line ~782) and `CandleStreamChannel.fetchHistoricalCandles` (line ~537), each logging again — 3 Sentry reports for 1 expected cancellation.

## Reproduction commit

SHA: `5c0a17f06d` — added `BUG_MARKER: abort error logged to Sentry` DevLogger line in HyperLiquidClientService catch block. Metro log confirmed marker fired during candle teardown.

## Changes

| File | Change |
|------|--------|
| `app/controllers/perps/utils/errorUtils.ts` | Added `isAbortError()` utility — detects AbortError by name or message pattern |
| `app/controllers/perps/services/HyperLiquidClientService.ts` | Added abort guard in `fetchHistoricalCandles` catch — skips Sentry, re-throws |
| `app/controllers/perps/services/MarketDataService.ts` | Wrapped Sentry logging + state update in `!isAbortError()` guard |
| `app/components/UI/Perps/providers/channels/CandleStreamChannel.ts` | Added early return for abort errors before `Logger.error` |
| `app/controllers/perps/index.ts` | Export `isAbortError` from utils barrel |
| `app/controllers/perps/utils/errorUtils.test.ts` | New: 10 tests for `isAbortError` and `ensureError` |
| `app/controllers/perps/services/MarketDataService.test.ts` | Added 2 tests: abort errors skip Sentry, real errors still log |
| `app/components/UI/Perps/providers/channels/CandleStreamChannel.test.ts` | Added 1 test: abort errors skip Logger.error |

## Test plan

### Automated
- **Unit tests**: 13 new/modified tests across 3 files — all pass
- **Lint**: `yarn lint` ✓
- **TypeScript**: `yarn lint:tsc` ✓
- **Format**: `yarn format:check` ✓
- **Recipe**: `validate-recipe.sh` exits 0 — navigates to BTC market, verifies candle data loads, navigates away (triggers teardown), asserts no BUG_MARKER in logs
- **Coverage**: `yarn coverage:analyze` ✓

### Manual (Gherkin)
```
Given the user is on the Perps BTC market detail screen
And candle data is loading via WebSocket
When the user navigates away from the market detail screen
Then no AbortError is logged to Sentry
And the candle data loaded successfully before navigation
```

## Evidence

| Artifact | Description |
|----------|-------------|
| `before.mp4` | Recipe run on pre-fix code |
| `after.mp4` | Recipe run on final fixed code |
| `before-ac2-candles-loaded.png` | BTC candle chart before fix |
| `after-ac2-candles-loaded.png` | BTC candle chart after fix |
| `before-ac1-no-abort-noise.png` | Log state before fix |
| `after-ac1-no-abort-noise.png` | Log state after fix |
| `recipe-coverage.md` | 3/3 ACs PROVEN |

## Ticket

[TAT-2971](https://consensyssoftware.atlassian.net/browse/TAT-2971)
