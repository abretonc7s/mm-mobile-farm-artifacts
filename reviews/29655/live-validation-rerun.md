# Live Validation Rerun

Rerun trigger: CDP became available after the original review.

App-relevant evidence:

- `yarn a:status` and `bash scripts/perps/agentic/app-state.sh status` reached the iOS app on `mm-1`.
- After unlocking, `bash scripts/perps/agentic/app-navigate.sh --no-screenshot PerpsHomeView` attempted to enter the Perps stack.
- The app entered the root error boundary instead of rendering Perps.
- Metro repeatedly reported:

```text
Warning: Error: A navigator cannot contain multiple 'Screen' components with the same name (found duplicate screen named 'PerpsClosePositionModals')
This error is located at:
    in PerpsGlobalErrorGate (created by PerpsScreenStack)
    in ErrorBoundary (created by Root)
```

Recipe status:

- A no-screenshot recipe was added at `artifacts/recipe.json`.
- Dry-run passed schema validation.
- Live run could not proceed once the app was already in the root error boundary because the route precondition could not evaluate.
- Restarting and navigating reproduced the same duplicate-screen app error.

Conclusion: live validation fails because `PerpsScreenStack` registers duplicate `Stack.Screen` names, blocking Perps from rendering.
