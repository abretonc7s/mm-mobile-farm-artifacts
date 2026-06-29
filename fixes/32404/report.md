# PR #32404 — Interactive PR-Complete Handoff

PR: feat(perps): enable RoE sign toggle on Auto Close TP/SL  
Branch: TAT-3398-feat-add-roe-sign-toggle  
Status: **done**

## Summary

Reopened PR workspace with inherited TAT-3398 family context. Prior fix commit `f94192ac81` addressed gambinish/cursor review about `hasInvalidTPSL` blocking Place Order after signed TP/SL confirm. This session fixes the **new** CHANGES_REQUESTED review (gambinish, 2026-06-29): sign toggle was clearing Auto Close validation errors when the user had typed a trigger price directly, because toggle recomputed from a clamped `0%` magnitude.

## Inherited recipe AC coverage

| AC | Claim | Recipe nodes |
|----|-------|--------------|
| AC1 | Default signs + TP / − SL | `ac1-tp-badge`, `ac1-sl-badge`, `ac1-screenshot` |
| AC2 | Tap TP +→−, value kept, trigger below entry | `ac2-fill-preset` … `ac2-flipped-screenshot` |
| AC3 | Tap TP −→+, value kept | `ac3-toggle-back`, `ac3-badge-plus` |
| AC4 | Tap SL −→+, value kept, trigger above entry | `ac4-fill-preset` … `ac4-screenshot` |
| AC5 | Preset flips badge to chip sign | `ac5-toggle-to-minus` … `ac5-screenshot` |
| AC6 | Negative TP → below-entry trigger | `ac6-toggle-to-minus` … `ac6-screenshot` |
| AC7 | Reopen resets defaults | `ac7-back` … `ac7-screenshot` |

## Files changed (this session, uncommitted)

| File | Change |
|------|--------|
| `app/components/UI/Perps/hooks/usePerpsTPSLForm.ts` | Sign toggle recomputes trigger only when RoE % is active input |
| `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx` | Per-field error display/styling (not gated on combined `isValid`) |
| `app/components/UI/Perps/hooks/usePerpsTPSLForm.test.ts` | Two regression tests for manual-price sign-toggle validation |

## Comments handled

| Comment | Triage | Status |
|---------|--------|--------|
| cursor[bot] inline 3474511814 | REAL | Fixed in `f94192ac81` (prior run) |
| gambinish review 4574797409 | REAL | Fixed in `f94192ac81` (prior run) |
| gambinish review 4593430638 | REAL | Fixed this session (uncommitted) |

See `artifacts/comments-report.md` for full triage.

## Validation

| Command | Result |
|---------|--------|
| `yarn eslint` (changed files, `--max-warnings=0`) | 0 errors; 7 pre-existing deprecation/react-compiler warnings on untouched lines |
| `yarn prettier --check` (changed files) | PASS after format write on `PerpsTPSLView.tsx` |
| `yarn jest usePerpsTPSLForm.test.ts` + `PerpsTPSLView.test.tsx` + `PerpsOrderView.test.tsx` | **230/230 PASS** |
| `yarn lint:tsc` | Skipped per worker-slot policy |
| Recipe (`artifacts/recipe.json`, slot macwork-mm-4) | **PASS 39/39** (re-run after Metro/CDP available) |

## Commit / push

**Not committed or pushed.** Operator should review diff, commit, push, and reply on GitHub.

## Remaining manual work

1. Review uncommitted diff and commit with message e.g. `fix(perps): preserve validation errors on RoE sign toggle for manual price entry`
2. Push branch and reply to gambinish on review 4593430638
3. Re-run inherited recipe once Metro is live on port 8064:
   ```bash
   temp/recipe/harness/mobile/runner/bin/metamask-recipe run temp/tasks/fix/32404-0629-230321/artifacts/recipe.json --adapter mobile --artifacts-dir temp/tasks/fix/32404-0629-230321/artifacts/recipe-run --project-root /Users/deeeed/dev/metamask/metamask-mobile-4 --slot macwork-mm-4 --json
   ```
4. Request re-review / merge when CI green
