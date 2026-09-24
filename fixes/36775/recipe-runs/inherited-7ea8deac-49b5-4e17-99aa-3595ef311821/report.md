
## Self-Review Fixes
- app/components/UI/Perps/components/PerpsModifyActionSheet/PerpsModifyActionSheet.test.tsx:257 — Cross test now asserts Flip is absent via `queryByTestId(PerpsModifyActionSheetSelectorsIDs.FLIP_POSITION)` instead of copy text, so it can't pass vacuously on a label change; added the missing blank line before the `it()`.
- artifacts/recipe.json `setup-assert-position` — the testnet BTC position had been closed since the last run; the node now converges it with `metamask.perps.ensure_positions` (BTC long, $250) instead of only asserting it. Recipe re-run passes.

## Self-Review Fixes (pass 2)
- app/components/UI/Perps/hooks/usePerpsMarginAdjustment.ts:53 — a successful fresh read without the position now returns `'position_closed'`; the removal stops with a "Position not found" toast instead of reaching the exchange (a failed read still falls through, as before).
- app/components/UI/Perps/Views/PerpsAdjustMarginView/PerpsAdjustMarginView.tsx:305 — `hasNoRemovableMargin` added to `isConfirmDisabled` and the remove-mode submit guard, so a retained amount can't submit under the zero-state explanation.
- app/components/UI/Perps/components/PerpsAdjustMarginBottomSheet/PerpsAdjustMarginBottomSheet.tsx:251 — `hasNoRemovableMargin` folded into `hasInvalidAmount`, which drives both Confirm's disabled state and the submit guard.
- Tests: hook (closed position stops submit), view and sheet (retained amount blocked at zero); all three fail without the fixes. Hook test default `getPositions` now returns the tested positions.
- artifacts/recipe.json — added `metamask.perps.ensure_mode lite` after the first market navigation so a run that follows the Pro (AC5) section starts in Lite. Recipe re-run passes (after resetting a stale idb companion with `idb kill`).
