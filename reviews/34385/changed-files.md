# Changed-file classification

| File | Category | Live-testable? |
|---|---|---|
| `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx` | React component | Yes — navigate |
| `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.ts` | React hook / component support | Yes — navigate |
| `app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.tsx` | React component | Yes — navigate |
| `app/components/UI/Perps/hooks/usePerpsClosePosition.ts` | React hook / component support | Yes — navigate |
| `app/components/UI/Perps/hooks/usePerpsOrderFees.test.ts` | Test file | No — run Jest |
| `app/components/UI/Perps/hooks/usePerpsOrderFees.ts` | React hook / component support | Yes — navigate |
| `app/components/UI/Perps/hooks/usePerpsTPSLForm.ts` | React hook / component support | Yes — navigate |
| `app/components/UI/Perps/types/navigation.ts` | Config/types | No direct live surface |
| `app/components/UI/Perps/utils/orderUtils.test.ts` | Test file | No — run Jest |
| `app/components/UI/Perps/utils/orderUtils.ts` | Utility | Indirect — exercised through order UI/tests |
| `app/components/UI/Perps/utils/translatePerpsError.ts` | Utility | Indirect — exercised through errors/tests |
| `app/components/UI/Perps/utils/translatePerpsErrorCoverage.test.ts` | Test file | No — run Jest |
| `locales/languages/en.json` | App JSON / localized displayed copy | Yes when matching errors occur; deterministic via tests |
| `package.json` | Config | No |
| `yarn.lock` | Config | No |

No native files are changed; no native rebuild is required for this diff.
