# Learnings — PR #28897

- **Perps navigation**: `navigate("Perps")` sets `initialTab: "perps"` on the Wallet route — the route name stays `Wallet`, not `Perps`. Use `wait_for route: Wallet` after navigating to Perps.
- **Eval ref qualification**: Recipe eval_ref actions require fully qualified names like `perps/auth`, not just `auth`. The runner does not auto-prefix.
- **Video recording**: `kill -INT %1` in Bash tool doesn't reliably reach the simctl process. Use `pkill -INT -f "simctl io.*recordVideo"` instead for reliable moov atom finalization.
- **Controller-only changes**: When a PR modifies internal method parameters (like removing a field from an order object), the change is not observable via CDP or UI. Unit tests are the definitive proof. Recipe value is limited to system health smoke tests.
- **HyperLiquidProvider pricing**: `placeOrder` always calls `#getAssetInfo` to fetch live price (line 3399). The `currentPrice` param on `OrderParams` is an optional optimization hint — when absent, the provider uses live price. This means omitting `currentPrice` does NOT add an extra API call.
- **Fee pre-validation pattern**: Client-side fee estimation before order placement is fragile — it uses stale prices and duplicates provider-side validation. Removing it (as this PR does) is a net positive.
- **Test revert-proofing**: The gold standard for testing "field X is not passed" is: exact match assertion (`toHaveBeenCalledWith({...})`) + negative assertion (`not.toHaveBeenCalledWith(expect.objectContaining({field: expect.any(Type)}))`). This PR demonstrates the pattern well.
- **File size awareness**: TradingService.ts (2,042 lines) and TradingService.test.ts (2,184 lines) are both above the 2,000-line threshold. Future PRs adding to these files should consider splitting.
- **trace.json**: The recipe runner's `validate-recipe.sh` does not always produce `trace.json` — rely on stdout output for pass/fail counts when trace file is absent.
- **Recipe pre-conditions**: `wallet.unlocked` and `perps.feature_enabled` are useful gate checks. `perps.ready_to_trade` would be needed for trade-execution recipes.
