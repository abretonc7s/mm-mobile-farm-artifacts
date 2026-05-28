## Concern Validation

- Dismissal validation: `ac3-press-close` returned `ok`; the fiber wait for hidden state timed out, but the failure screenshot and revisit screenshot show the banner was visually gone and stayed hidden after leaving and returning.
- Analytics concern validated by code read and `rg`: `handleDismiss` only sets local/storage dismissal state, and `handlePress` only dispatches the pending deeplink and navigates. No `track`, `trackEvent`, or `MetaMetricsEvents.PERPS_UI_INTERACTION` call exists in `PerpsCompetitionBanner.tsx`.
