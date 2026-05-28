## Perps Domain Scan

- No controller portability or WS subscription changes.
- Feature flag follows existing version-gated selector pattern and registry entry.
- No Sentry tracing is expected for this small UI surface.
- Perps-specific blocker:
  - `PerpsCompetitionBanner.tsx:80` and `:89` do not emit MetaMetrics/Mixpanel events for close or engage, despite the linked ticket requiring tracking for both.
- Live validation note:
  - The fiber-based recipe wait for `visible:false` was stale after dismissal, but screenshot evidence shows the banner disappears and remains hidden after revisiting the Perps home screen.
