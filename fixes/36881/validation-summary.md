# mm-harness check diff

Verdict: pass
Profile: fast
Fix: no
Base: origin/main (github-pr: main)
Changed files: 24

## Checks

- PASS policy-suppressions (/Volumes/FD/dev/metamask/metamask-mobile-2/temp/tasks/fix/36881-1001-124447/artifacts/policy-suppressions.log)
- PASS eslint (/Volumes/FD/dev/metamask/metamask-mobile-2/temp/tasks/fix/36881-1001-124447/artifacts/eslint.log)
- PASS prettier (/Volumes/FD/dev/metamask/metamask-mobile-2/temp/tasks/fix/36881-1001-124447/artifacts/prettier.log)
- PASS jest (/Volumes/FD/dev/metamask/metamask-mobile-2/temp/tasks/fix/36881-1001-124447/artifacts/jest.log)
- PASS jest-integration (/Volumes/FD/dev/metamask/metamask-mobile-2/temp/tasks/fix/36881-1001-124447/artifacts/jest-integration.log)
- PASS jest-view (/Volumes/FD/dev/metamask/metamask-mobile-2/temp/tasks/fix/36881-1001-124447/artifacts/jest-view.log)
- SKIP typecheck — profile=fast; run with --profile full for repo-wide typecheck

## Changed Files

- app/components/UI/Perps/Views/PerpsProMarketView/PerpsProCrossMargin.view.test.tsx
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.ts
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.tsx
- app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx
- app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.view.test.tsx
- app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.test.tsx
- app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.tsx
- app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx
- app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.tsx
- app/components/UI/Perps/hooks/useHasExistingPosition.test.ts
- app/components/UI/Perps/hooks/useHasExistingPosition.ts
- app/components/UI/Perps/hooks/usePerpsMarginModeLock.test.ts
- app/components/UI/Perps/hooks/usePerpsMarginModeLock.ts
- app/components/UI/Perps/hooks/usePerpsMarketData.test.ts
- app/components/UI/Perps/hooks/usePerpsMarketData.ts
- app/components/UI/Perps/integration/marginModeLock.integration.test.ts
- app/components/UI/Perps/types/navigation.ts
- app/components/UI/Perps/utils/orderParams.test.ts
- app/components/UI/Perps/utils/orderParams.ts
- locales/languages/en.json
- tests/component-view/mocks.ts
- tests/integration/harnesses/perps/perps.ts
