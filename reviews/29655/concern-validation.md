# Concern Validation

CDP status: unavailable (`app-state.sh status` cannot reach Metro at `http://localhost:8061/json/list`).

Validated by code read:

- Debounce mismatch: `PerpsGlobalErrorGate.tsx` schedules `PERPS_SCREEN_VIEWED` after `ANALYTICS_DEBOUNCE_MS = 150`; the PR body states a 1-second debounce. A flap sequence `error -> null -> error` where the first error lasts 200 ms will emit the first event before clearing, then the second event after the new debounce. That violates the stated 1-second suppression behavior.
- Sentry breadcrumb duplication: each route-level provider still mounts `PerpsConnectionProvider` with `suppressErrorView`, but the provider's breadcrumb effect is independent of `suppressErrorView`. When the shared manager error changes, every mounted provider can record `PerpsConnectionErrorView shown` even though its error view is suppressed.

Runtime validation: unavailable because CDP is offline.
