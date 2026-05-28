## File Size Guardrail

- `app/components/UI/Perps/selectors/featureFlags/index.test.ts` is 2,099 lines: suggestion severity, approaching split threshold.
- `locales/languages/en.json` and `tests/feature-flags/feature-flag-registry.ts` are large shared registry/localization files; the PR adds only small entries, so no actionable split request for this PR.
- No touched source file exceeds the 2,500-line hard limit.
