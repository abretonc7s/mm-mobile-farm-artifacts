# Recipe coverage — PR #35832 re-validation

Re-ran inherited recipe against `7690b91b7f` (branch rebased onto `origin/main` `c131648fc6`).
First attempt failed at `setup-unlock` (wallet stability window). After `app.lifecycle restart`, the full graph passed: 18/18 nodes.

## Coverage matrix

| # | AC | Proof mode | Primary evidence | Recipe nodes | Visual file | Evidence verdict | Justification |
|---|----|------------|------------------|--------------|-------------|------------------|---------------|
| 1 | After Lite → Pro → Lite, header back lands on Perps home, not wallet | mixed | `ui.wait_for` + screenshot | `ac1-press-back`, `ac1-wait-perps-home`, `ac1-assert-not-wallet`, `ac1-screenshot-landing` | `recipe-run/screenshots/evidence-ac1-back-lands-on-perps-home.png` | PROVEN | `perps-watchlist-header` and `perps-market-add-funds-button` both `visibility: viewport`. PNG shows Perps Testnet home ($629.30, Withdraw / Add funds, Watchlist), not wallet tokens. |
| 2 | Lite market → Pro workstation → Lite market again | mixed | `ui.wait_for` on claimed targets + screenshots | `ac2-wait-lite-start`, `ac2-switch-to-pro`, `ac2-wait-pro`, `ac2-screenshot-pro`, `ac2-switch-back-lite`, `ac2-wait-lite-return`, `ac2-screenshot-lite-return` | `recipe-run/screenshots/evidence-ac2-pro-workstation.png`, `recipe-run/screenshots/evidence-ac2-lite-return.png` | PROVEN | Pro wait matched `perps-pro-order-form-place-order`; PNG shows Pro pill, Isolated 3x, order book, Place order. Lite wait matched `perps-market-details-long-button`; PNG shows Lite pill, BTC market, Long/Short. |

## Trace

All `ac<N>-` and `setup-` nodes `ok=true` in `artifacts/recipe-run/trace.json`. Terminal `done` passed.

Overall: 2/2 ACs PROVEN.
