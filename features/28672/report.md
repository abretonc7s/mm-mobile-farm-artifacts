# Report — TAT-2906: Update Hyperliquid SDK

## Summary

Updated `@nktkas/hyperliquid` from `0.30.2` to `0.32.2`. No API-breaking changes were found affecting the codebase — all existing type imports and method signatures remain compatible. All 288 perps test suites pass (1467 controller + 5503 UI tests).

## Changes

| File | Change |
|------|--------|
| `package.json` | Bumped `@nktkas/hyperliquid` from `^0.30.2` to `^0.32.2` |
| `yarn.lock` | Updated lock entry; `@nktkas/rews` bumped from 1.2.3 → 2.1.0, `valibot` from 1.2.0 → 1.3.1, `micro-eth-signer` removed (no longer a dep), CLI bin removed |

## Test Plan

- TypeScript: `tsc --noEmit` — no errors
- Unit tests: `yarn jest app/controllers/perps/` — 29 suites, 1467 tests passed
- Unit tests: `yarn jest app/components/UI/Perps/` — 259 suites, 5503 tests passed
- Recipe: 5/5 steps passed (navigate → wait route → wait market data → assert BTC found → screenshot)

## Evidence Artifacts

- `evidence-market-loaded.png` — markets list loaded successfully with SDK 0.32.2

## Ticket

https://consensyssoftware.atlassian.net/browse/TAT-2906
