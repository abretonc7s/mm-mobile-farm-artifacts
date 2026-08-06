# File Size Guardrail

| File | Lines | PR delta | Disposition |
|---|---:|---:|---|
| `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx` | 2,408 | +10/-13 | Suggestion: establish a follow-up split plan; this PR does not materially grow the file. |
| `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.ts` | 953 | +10/-11 | Within limit. |
| `app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.tsx` | 682 | +2/-1 | Within limit. |
| `app/components/UI/Perps/hooks/usePerpsClosePosition.ts` | 351 | +2/-1 | Within limit. |
| `app/components/UI/Perps/hooks/usePerpsOrderFees.test.ts` | 2,149 | +7/-4 | Suggestion: split the test suite by behavior in a follow-up; this PR does not materially grow the file. |
| `app/components/UI/Perps/hooks/usePerpsOrderFees.ts` | 711 | +3/-2 | Within limit. |
| `app/components/UI/Perps/hooks/usePerpsTPSLForm.ts` | 1,062 | +2/-1 | Within limit. |
| `app/components/UI/Perps/types/navigation.ts` | 356 | +1/-1 | Within limit. |
| `app/components/UI/Perps/utils/orderUtils.test.ts` | 1,557 | +59/-0 | Below the `>100`-line growth trigger. |
| `app/components/UI/Perps/utils/orderUtils.ts` | 753 | +9/-5 | Within limit. |
| `app/components/UI/Perps/utils/translatePerpsError.ts` | 447 | +31/-0 | Within limit. |
| `app/components/UI/Perps/utils/translatePerpsErrorCoverage.test.ts` | 67 | +67/-0 | Within limit. |
| `locales/languages/en.json` | 10,740 | +16/-1 | Localization registry, not an executable source module; splitting it would violate the repository's locale-file structure. No split action. |
| `package.json` | 872 | +1/-1 | Within limit. |
| `yarn.lock` | 48,498 | +6/-6 | Package-manager-generated lockfile; it cannot be meaningfully split. No split action. |

The two source/test suggestions are non-blocking because the controller-v11 adaptation is narrowly scoped and does not cause the pre-existing file size.
