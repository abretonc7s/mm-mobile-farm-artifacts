# Static Validation Against Published HEAD

- Reviewed commit: `f506550989cedd3a7ec84d4296291a2b77c5998f`.
- `OrderType` in perps-controller 11.0.0 contains `market`, `limit`, `stop_market`, `stop_limit`, `take_profit_market`, and `take_profit_limit`.
- The controller's `getTriggerExecution` maps `limit`, `stop_limit`, and `take_profit_limit` to `limit`; all other order types map to `market`. The six changed toast lookups therefore remain exhaustive and retain the intended execution-mode bucket.
- `isLimitExecutionOrderType` uses the same limit-execution set. The changed `determineMakerStatus` branch preserves market/limit behavior and handles the widened trigger-order union consistently.
- The remaining direct market/limit branches receive values from UI paths that expose only the existing market/limit selector or close-position toggle. No trigger placement type is reachable through those current callers.
- No speculative correctness concern survived this concrete code-path trace.

Runtime/CDP validation was intentionally not performed because this review was changed by the operator to the light/static tier.
