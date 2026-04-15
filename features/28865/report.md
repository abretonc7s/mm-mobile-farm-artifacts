# TAT-2954 Report

## Summary

Changed `fetchHistoricalCandles()` in `HyperLiquidClientService` to use HTTP transport instead of WebSocket for candleSnapshot requests. This eliminates the abort race condition that causes 429 rate limiting during rapid market navigation on extension.

## Changes

| File | Change |
|---|---|
| `app/controllers/perps/services/HyperLiquidClientService.ts` | `getInfoClient()` → `getInfoClient({ useHttp: true })` in `fetchHistoricalCandles()` |
| `app/controllers/perps/services/HyperLiquidClientService.test.ts` | Updated 25 mock references from `mockInfoClientWs` to `mockInfoClientHttp`; added explicit HTTP transport assertion test |

## Test Plan

- Unit tests: 77/77 passed (`HyperLiquidClientService.test.ts`)
- Type check: `tsc --noEmit` passed
- Lint: no errors
- Recipe validation: 27/27 nodes passed — rapid switching across 6 markets (BTC → ETH → SOL → HYPE → BTC → ETH), no candle-related errors

## Evidence

- `after.mp4` — simulator recording of recipe execution
- `evidence-rapid-switch-chart-loaded.png` — screenshot of final market detail page after rapid switching

## Ticket

https://consensyssoftware.atlassian.net/browse/TAT-2954
