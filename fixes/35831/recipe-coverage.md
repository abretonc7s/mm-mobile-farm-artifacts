# Recipe coverage — PR #35831 review round

Recipe executed against the review-fix commit `b11117780de` (rebased on `origin/main` `954c6fe85cf`): **41/41 nodes pass**, 60s, artifacts in `artifacts/recipe-run/`.

Fixture: dev1 (`0x8dc6…9003`), Hyperliquid testnet. One live Cross ETH position, 0.0051 @ 2394.1, `leverage.type=cross`, venue `liquidationPx: null` (order `60226912393`). The account's pre-existing isolated BTC position was closed first with explicit user authorization (order `60226752331`).

| Proof target | Recipe node(s) | Evidence |
|---|---|---|
| Selected account is dev1, Hyperliquid, testnet | `wallet`, `account`, `environment` | PASS. `environment` stdout confirms address, provider, `isTestnet: true` |
| Exactly one live Cross ETH position | `positions`, `require-cross`, `require-cross-mode`, `require-cross-market` | PASS. Controller and fresh venue read agree |
| Venue liquidation is literal null (not "", 0, false) | `price-kind`, `require-null-price`, `require-null-falsy`, `require-null-not-string/zero/false` | PASS |
| Cross badge in Pro and Lite | `pro-tag`, `lite-tag` | PASS. `cross-summary-pro.png` shows the `Cross` badge |
| Position-scoped collateral label, renamed this round | `pro-margin`, `lite-margin` (text "Position margin used") | PASS. `cross-summary-pro.png` shows "Position margin used $12.23" beside the account-level values |
| Margin edit control absent on Cross | `pro-no-edit`, `lite-no-edit` | PASS |
| Explicit no-liquidation state | `pro-price`, `lite-price` | PASS. `cross-summary-pro.png` renders "No liquidation price" |
| Shared-collateral explanation | `pro-info`, `pro-explanation`, `lite-info`, `lite-explanation` | PASS. Exact tooltip copy matched; `cross-explanation-{pro,lite}.png` |
| Privacy masking with the Cross flag on | none (component-test scope) | `PerpsPositionCard.test.tsx` enables the flag, asserts masked dots and absent unmasked text |
| Margin-mode error copy dedupe | none (not runtime-reachable in this slice) | One definition per key after the fix; verified in the diff |

Not covered: Android, mixed-book grouping, account-wide refresh, the numeric-liquidation fixture this round (null branch only), and the Pro margin-mode picker (disabled in this slice).

Cleanup: fixture closed (order `60227080843`), ETH leverage restored to the isolated 3x baseline, final read 0 positions / 0 orders.
