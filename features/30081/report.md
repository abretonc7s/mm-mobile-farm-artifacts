# Report: Perps Service Interruption Banner (TAT-2280)

## Summary

Adds a new outage banner component to the Perps home and market detail screens, controlled by an existing remote feature flag (`perpsPerpTradingServiceInterruptionBannerEnabled`). When enabled by CS/support, the banner displays outage messaging with links to customer support and Hyperliquid for direct position management. The `outage_banner_shown` property is tracked on `PERPS_SCREEN_VIEWED` events for both screens.

## Changes

| File | Change |
|------|--------|
| `app/components/UI/Perps/components/PerpsServiceInterruptionBanner/PerpsServiceInterruptionBanner.tsx` | New banner component |
| `app/components/UI/Perps/components/PerpsServiceInterruptionBanner/PerpsServiceInterruptionBanner.types.ts` | Props interface |
| `app/components/UI/Perps/components/PerpsServiceInterruptionBanner/index.ts` | Barrel export |
| `app/components/UI/Perps/components/PerpsServiceInterruptionBanner/PerpsServiceInterruptionBanner.test.tsx` | 7 unit tests, 100% coverage |
| `app/components/UI/Perps/Views/PerpsHomeView/PerpsHomeView.tsx` | Render banner + analytics property |
| `app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.tsx` | Render banner + analytics property |
| `app/controllers/perps/constants/eventNames.ts` | Add `OUTAGE_BANNER_SHOWN` property |
| `app/components/UI/Perps/Perps.testIds.ts` | Add test IDs for both screens |
| `locales/languages/en.json` | Add `service_interruption` i18n strings |

## Test Plan

- Unit tests: 7/7 pass, 100% statement/branch/function/line coverage
- Recipe validation: 14/14 nodes pass
- TSC: clean
- Lint: clean

## Evidence

| AC | Proof Mode | Evidence |
|----|-----------|----------|
| AC1 — Flag OFF, no banner | state | `ac1-check-no-banner` eval asserts flag not 'true' |
| AC2 — Flag ON, banner shown on Mobile | visual | `evidence-ac2-banner-visible.png` + `ac2-wait-banner` wait_for testID |
| AC6 — Flag toggled OFF, banner disappears | visual | `evidence-ac6-banner-gone.png` + `ac6-verify-flag-off` eval |

AC3-AC5 are Extension-scoped or covered by AC2 for Mobile.

## Ticket

https://consensyssoftware.atlassian.net/browse/TAT-2280
