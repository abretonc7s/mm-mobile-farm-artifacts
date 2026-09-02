# Learnings

- Dynamic feature-gated tab sets cannot safely share numeric selection state. A typed tab key keeps TWAP and Chase distinct even when either tab is absent.
- Hyperliquid schedule streaming is not sufficient for Fill History because slice fills arrive through a separate path. Streaming must coexist with bounded REST reconciliation unless both streams are subscribed.
- Account, provider, and network identity belong in the TWAP hook lifecycle, and async reads need generation guards so stale responses cannot restore canceled or previous-account schedules.
- Privacy, load-error, and reduce-only termination states need explicit UI assertions; happy-path card and toast tests did not expose the sensitive-size leak or misleading directional copy.
- Large fill histories need a bounded rendering strategy from the start. Runtime recipe proof remained unavailable because Metro could not resolve an installed nested `domutils` package after one harness recovery attempt.
