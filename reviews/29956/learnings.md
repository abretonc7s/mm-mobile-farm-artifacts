# Learnings — PR #29956

- **useSectionPerformance hook** is the central telemetry hook for homepage sections. It tracks TTC (Time to Content), Data Fetch Latency, and Re-render Monitoring. All ref-based bookkeeping — no extra re-renders.
- **contentStateForTrace** is a new optional override that takes priority over `isEmpty`-derived content_state. This pattern (explicit override > derived default) is clean and backward-compatible.
- **analyticsName vs HomeSectionNames**: Some sections have different values for their Sentry `section_id` (was `HomeSectionNames` enum) and their analytics section name. This PR aligns them — downstream Sentry queries may need updating.
- **Telemetry-only PRs** are hard to validate via CDP/device — Sentry trace data is not observable at runtime without Sentry dashboard access. Unit tests become the primary proof.
- **PredictionsSection** is the most complex homepage section (737 lines) with multiple data sources (positions, claimable, markets) and three rendering variants (default, positions-only, trending-only). Only the default variant has performance tracking.
- **TokensSection** conflates error and empty in `isEmpty` but the `contentStateForTrace` override corrects the final trace value. Semantic purity vs functional correctness tradeoff.
- **Circuit breaker warnings** in Metro logs are pre-existing and unrelated to PR changes — don't flag them.
- **Video recording on iOS simulator**: `xcrun simctl io <device> recordVideo` requires foreground execution (not `run_in_background`). The `&` backgrounding in shell works correctly.
