# Recipe Coverage Matrix — PR #29420

Trace source: `.agent/recipe-runs/2026-05-23_10-03-40_recipe/trace.json`
Summary source: `.agent/recipe-runs/2026-05-23_10-03-40_recipe/summary.json`
Trace-derived counts: 5/5 passed, 0 failed, 0 skipped

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "usePerpsPositionForAsset derives userAddress from the selected account group's EVM account, not from AccountsController.state.selectedAccount" | both | ac1-eval-evm-selector (190ms, PASS) | n/a (generate-internal) | PROVEN | CDP eval confirmed selected account group contains EVM account (`0x8dc623e964475d4d669da601fd15ea9125469003`); code review confirms all 4 hooks now use `selectSelectedAccountGroupEvmInternalAccount`; unit tests assert EVM address is used even when non-EVM account is selected |
| 2 | "Users with Bitcoin, Solana, or Tron accounts selected can open the Perps Trending view without triggering a ValiError" | both | setup-navigate-to-perps (4419ms, PASS), ac2-wait-market-visible (302ms, PASS), ac2-log-watch-no-valierror (129ms, PASS), ac2-screenshot-market (738ms, PASS) | evidence-ac2-perps-market-open.png | PROVEN | Perps BTC market detail screen opened successfully; log_watch confirmed no ValiError in window (caveat: `watch_counts` empty — absence proof limited to live window); screenshot shows live BTC-USD market at $74,643 with chart and Long/Short buttons |
| 3 | "Audit other Perps hooks for the same selectSelectedInternalAccountFormattedAddress anti-pattern and fix accordingly" | n/a | n/a | n/a | UNTESTABLE | Code audit AC — verified via grep: no remaining production Perps usage of `selectSelectedInternalAccountFormattedAddress`. Only 2 residual test mocks (usePerpsOrderFees.test.ts:32, PerpsPositionTransactionView.test.tsx:56) which are harmless dead mocks |
| 4 | "Unit test: hook correctly returns no position data (rather than throwing) when the selected account is non-EVM" | n/a | n/a | n/a | UNTESTABLE | Jest-only AC — verified by running tests: 187/187 pass across 5 suites including 2 new tests in usePerpsPositionForAsset.test.ts covering non-EVM selected account (line 266) and no-EVM-in-group empty state (line 287) |

Overall recipe coverage: 2/4 ACs PROVEN (untestable: AC3 — code audit only, AC4 — jest only; weak: 0, missing: 0)
