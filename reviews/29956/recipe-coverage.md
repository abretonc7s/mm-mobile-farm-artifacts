# Recipe Coverage

Recipe decision: skip-telemetry-only

| # | AC (verbatim) | Target platform | Recipe nodes | Screenshot | Visual verdict | Justification |
|---|---------------|-----------------|--------------|------------|----------------|---------------|
| 1 | "Given the app is on the wallet homepage... Then no regression is observed in section layout or behavior" | both | N/A | homepage-sections.png | UNTESTABLE | standard-tier skip — telemetry-only changes, no UI-surface recipe possible; homepage screenshot confirms no visual regression |
| 2 | "Given Sentry performance data... Then Time to Content completes with expected content_state... And Homepage Section Data Fetch reflects the first load only" | both | N/A | N/A | UNTESTABLE | standard-tier skip — Sentry trace verification requires Sentry dashboard access, not exercisable via CDP; unit tests cover the hook logic |

Overall recipe coverage: 0/2 ACs PROVEN (untestable: 1, 2, weak: 0, missing: 0)
