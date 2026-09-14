# Recipe coverage — TAT-3786

Ticket has no `## Acceptance Criteria` section; both ACs are derived verbatim from the ticket
`## Description` (see `## Recipe ACs` in TASK.md).

## Coverage matrix

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes (IDs) | Visual file if any | Evidence verdict | Justification |
|---|---------------|------------|------------------|---------------------|--------------------|------------------|---------------|
| 1 | "When I tap '<' back arrow ... Expected behavior = then I am redirected to perps home." | mixed | state (`ui.wait_for` route/element assertions) + screenshot | `ac1-press-back`, `ac1-wait-perps-home`, `ac1-assert-not-wallet`, `ac1-screenshot-landing` | before: `before-evidence-ac1-back-lands-on-perps-home.png` / after: `after-ac1-back-lands-on-perps-home.png` | PROVEN | Before-run asserted the buggy state (`wallet-send-button` visible, `perps-market-add-funds-button` absent) and the PNG shows the wallet home token list. After-run asserts `perps-watchlist-header` and `perps-market-add-funds-button` visible; the PNG shows the Perps home screen ("Perps · Testnet", $332.73 Perps balance, Withdraw / Add funds, Watchlist). Same journey, same back press, opposite destination. |
| 2 | "When I tap 'Lite' on TDP (market page), I see the workstation / When I tap 'Pro' on workstation, I see the TDP again" | visual | ui.screenshot | `ac2-wait-lite-start`, `ac2-switch-to-pro`, `ac2-wait-pro`, `ac2-screenshot-pro`, `ac2-switch-back-lite`, `ac2-wait-lite-return`, `ac2-screenshot-lite-return` | `after-ac2-pro-workstation.png`, `after-ac2-lite-return.png` | PROVEN | Each screenshot is preceded by a `ui.wait_for` on the claimed target (`perps-pro-order-form-place-order` for Pro, `perps-market-details-long-button` for Lite). The Pro PNG shows the workstation (Pro pill, order book, Long/Short, Limit, Size, TP/SL, Place order); the Lite PNG shows the market page (Lite pill, candle period selector, Market insights, Long/Short). |

## Notes

- Trace cross-check (`artifacts/trace.json`): every `ac<N>-` node has a trace entry and all report
  `ok=true`. No AC row rests on a failed node.
- Forbidden-pattern scan (step 13): no `switch`/`default`, no `eval_sync`, no `wait` used in place of
  `ui.wait_for` (the recipe contains zero `wait` nodes), no fiber-only assertion for a visual claim,
  every node ID is prefixed `ac<N>-`/`setup-` (plus the terminal `end` node `done`), both visual/mixed
  ACs carry screenshots, no ES6+ in typed actions, and no UI value injection — the journey is driven
  entirely through `ui.press` / `ui.navigate` / typed `metamask.perps.ensure_mode`.
- The AC1 negative assertion originally used `expected: absent` on `wallet-send-button`. That failed
  because the wallet tab stays mounted in the tree behind Perps home (`visibility: "tree"`), so it was
  replaced with a positive assertion on the Perps-home-only `perps-market-add-funds-button`, per the
  "do not equate tree presence with visibility" rule.
- The Lite screenshot's chart area renders as a grey placeholder because the TradingView library fails
  to load in this sandbox (visible in `metro.log` as a network warning). This is environmental and
  unrelated to the fix; the Lite-mode claim is carried by the Lite pill and the Lite-only controls.

Overall recipe coverage: 2/2 ACs PROVEN (untestable: none, weak: 0, missing: 0)
