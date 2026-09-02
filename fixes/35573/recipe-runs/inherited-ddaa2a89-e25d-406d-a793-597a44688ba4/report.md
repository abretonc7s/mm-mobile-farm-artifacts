# TAT-3772 report

Branch: `TAT-3772-fix-fix-perps-deposit-performance` (local only, no push)
Fix commit: `5b573e5928`
Marker commit: `03da75290c`

Perps Add funds awaited `depositWithConfirmation()` and set processing state on tap, so the confirmation skeleton could not paint. Home and market details now navigate first, haptic immediately, and fire-and-forget deposit prep with a confirmation-focused dismiss guard.

Recipe coverage: 2/2 ACs PROVEN. Evidence: `before-evidence-ac1-deposit-confirmation.png` / `after-ac1-deposit-confirmation.png`, `before-evidence-ac2-pay-with-list.png` / `after-ac2-pay-with-list.png`, `before.mp4`, `after.mp4`.

## Self-Review Fixes
- `app/components/UI/Perps/utils/depositConfirmationGuard.ts:85` — cancel the guard when a presented confirmation loses focus so a later unrelated confirmation is not dismissed on prep failure
- `app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts:192` — await handleAddFunds, assert prep has not started, then flush the deferred turn
- `app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.test.tsx:1787` — assert navigation happens before the deferred deposit prep call
