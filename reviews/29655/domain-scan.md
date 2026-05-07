# Domain Anti-pattern Scan

Tier: standard quick scan.

Findings:

1. `PerpsGlobalErrorGate.tsx:14` uses an inline `150` ms debounce while the PR body states a 1-second debounce window and the manual scenario says flaps within 1 second should be suppressed. This is a behavior/spec mismatch, not just a naming issue.
2. `routes/index.tsx:137`, `routes/index.tsx:227`, and `routes/index.tsx:271` suppress provider error UI, but `PerpsConnectionProvider` still emits the `PerpsConnectionErrorView shown` Sentry breadcrumb whenever `connectionState.error` changes, regardless of `suppressErrorView`. With three suppressed providers mounted, Sentry breadcrumbs can still duplicate and be mislabeled even though the centralized gate owns rendering.

Non-findings:

- Analytics event payload uses `PERPS_EVENT_PROPERTY` / `PERPS_EVENT_VALUE` constants; no magic event property strings in changed runtime code.
- No controller portability violations; changed runtime files are UI/provider route components only.
- Polling and debounce timers are cleaned up in `PerpsGlobalErrorGate`.
- No new WebSocket subscriptions are introduced.
