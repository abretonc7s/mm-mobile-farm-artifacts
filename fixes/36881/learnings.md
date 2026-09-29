# Learnings — PR #36881 pr-complete (round 2)

- Reviewers caught provider scoping twice. Symbol-only lookups (`usePerpsMarketData`, `useHasExistingPosition`) broke once the same symbol could exist on several providers. For multi-provider perps UI, key every market/position read on symbol plus `providerId` from the start.
- A Cross recipe that passed before failed on live config: remote `perpsTerminalBackendEnabled` turned on (min 8.3.0), and the PR keeps Cross off on the Terminal path. Recipes whose outcome depends on a gate should pin every flag the gate reads, not just the feature flag.
- The same gate probably explains the Jira report "flag on but still can't choose Cross". When a reporter says a flagged feature is missing, read the live flag set before suspecting the code.
- mm-6 `.js.env` ships `OVERRIDE_REMOTE_FEATURE_FLAGS="true"`, which silently disables every version-gated perps flag, Pro mode included, even with harness overrides. The failure only shows up as "Perps did not reach pro mode".
- Inherited recipe command nodes hardcode another task's log folder. It failed only because the folder was missing; recipe command outputs should use a task-relative path.
