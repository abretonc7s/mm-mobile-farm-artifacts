# TAT-3561 report

Local commit `51e6f2e4074` added Auto Close %RoE +/− badges. Self-review then asked for typed analytics constants. That follow-up is below.

## Self-Review Fixes
- `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx:614` — `PERPS_UI_INTERACTION` ACTION `'tp'` → `PERPS_EVENT_VALUE.ACTION.TP`
- `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx:638` — ACTION `'sl'` → `PERPS_EVENT_VALUE.ACTION.SL`

Re-verified on HEAD `ac6fc667c20`: `PerpsTPSLView.test.tsx` 44/44, eslint `--max-warnings=0` clean, recipe 31/31 after `app.lifecycle restart` (`MOBILE_SOURCE_NOT_LOADED`), artifact contract PASS.

## Badge alignment
- `PerpsTPSLView.tsx` — `ButtonBase` `self-start` pinned the +/− chip to the top of the %RoE field. `RoeSignBadge` forces `self-center` and `BodyMd` so it lines up with `$` / value / `%`.
- Recipe re-run after the fix: 31/31 at `2026-09-14T14:33:17Z`. New PNGs copied to `artifacts/after-ac-*.png`.
