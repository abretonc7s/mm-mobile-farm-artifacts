# Report: TAT-3094 — Mobile decimals on open orders

## Summary

Open orders (limit, TP, SL) on compact order rows displayed trigger/limit prices with a fixed 2-decimal format (`PRICE_RANGES_MINIMAL_VIEW`) instead of market-appropriate decimals. Fixed by switching to `PRICE_RANGES_UNIVERSAL` which respects the same decimal rules used for market prices (e.g., 0 decimals for BTC >$10k, up to 6 for micro-cap tokens).

## Root cause

`PerpsCompactOrderRow.tsx:52` passed `PRICE_RANGES_MINIMAL_VIEW` to `formatPerpsFiat()` for the order trigger/limit price. `PRICE_RANGES_MINIMAL_VIEW` has a hard max of 2 decimals across all price ranges. The expanded order card (`PerpsOpenOrderCard.tsx:291`) already correctly uses `PRICE_RANGES_UNIVERSAL`.

Data flow: `resolveOrderDisplayPriceAndLabel()` → `formatPerpsFiat(priceValue, { ranges: PRICE_RANGES_MINIMAL_VIEW })` → renders with 2 decimals regardless of price magnitude.

## Reproduction commit

SHA: `24307af0a0` — `debug(pr-29799): add reproduction marker`

The marker logged the buggy formatting with `PRICE_RANGES_MINIMAL_VIEW` vs the correct output.

## Changes

| File | Description |
|------|-------------|
| `app/components/UI/Perps/components/PerpsCompactOrderRow/PerpsCompactOrderRow.tsx` | Changed import and usage from `PRICE_RANGES_MINIMAL_VIEW` to `PRICE_RANGES_UNIVERSAL` for order price formatting |
| `app/components/UI/Perps/components/PerpsCompactOrderRow/PerpsCompactOrderRow.test.tsx` | Updated mock to export `PRICE_RANGES_UNIVERSAL`, added test asserting it's used |

## Test plan

### Automated
- Unit tests: 17/17 pass (`PerpsCompactOrderRow.test.tsx`)
- Lint: pass
- TypeScript: pass (pre-existing errors in unrelated files)
- Format: pass
- Recipe: pass (5/5 nodes)

### Manual (Gherkin)
```gherkin
Given the Trading account has open BTC TP/SL orders
When I navigate to BTC market details
Then the compact order rows show trigger prices with 0 decimals (matching market price format)
And the expanded order card shows trigger prices with 0 decimals
```

## Evidence

- `before-evidence-ac1-market-details.png` — BTC market details before fix
- `after-ac1-market-details.png` — BTC market details after fix
- `recipe.json` — Validation recipe
- `recipe-coverage.md` — AC coverage matrix (2/2 PROVEN)

## Ticket

[TAT-3094](https://consensyssoftware.atlassian.net/browse/TAT-3094)
