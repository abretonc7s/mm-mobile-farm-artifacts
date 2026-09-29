# mm-harness check diff

Verdict: pass
Profile: fast
Fix: no
Base: origin/main (github-pr: main)
Changed files: 20

## Checks

- PASS policy-suppressions (/Users/deeeed/dev/metamask/metamask-mobile-6/temp/tasks/fix/36881-0928-221345/artifacts/policy-suppressions.log)
- PASS eslint (/Users/deeeed/dev/metamask/metamask-mobile-6/temp/tasks/fix/36881-0928-221345/artifacts/eslint.log)
- PASS prettier (/Users/deeeed/dev/metamask/metamask-mobile-6/temp/tasks/fix/36881-0928-221345/artifacts/prettier.log)
- PASS jest (/Users/deeeed/dev/metamask/metamask-mobile-6/temp/tasks/fix/36881-0928-221345/artifacts/jest.log)
- PASS jest-integration (/Users/deeeed/dev/metamask/metamask-mobile-6/temp/tasks/fix/36881-0928-221345/artifacts/jest-integration.log)
- SKIP typecheck — profile=fast; run with --profile full for repo-wide typecheck

## Changed Files

- .yarn/patches/@metamask-perps-controller-npm-18.0.1-1106ae680a.patch
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.ts
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.tsx
- app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx
- app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.tsx
- app/components/UI/Perps/hooks/useHasExistingPosition.test.ts
- app/components/UI/Perps/hooks/useHasExistingPosition.ts
- app/components/UI/Perps/hooks/usePerpsMarginModeLock.test.ts
- app/components/UI/Perps/hooks/usePerpsMarginModeLock.ts
- app/components/UI/Perps/hooks/usePerpsMarketData.test.ts
- app/components/UI/Perps/hooks/usePerpsMarketData.ts
- app/components/UI/Perps/integration/marginModeLock.integration.test.ts
- app/components/UI/Perps/utils/orderParams.test.ts
- app/components/UI/Perps/utils/orderParams.ts
- locales/languages/en.json
- package.json
- tests/integration/harnesses/perps/perps.ts
- yarn.lock
