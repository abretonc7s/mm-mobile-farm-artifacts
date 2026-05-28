# PR Review: #30731 — feat(perps): add competition banner to perps home screen cp-7.79.0

**Tier:** standard

## Summary
The PR adds the Perps competition banner behind a feature flag, places it below balance actions and above positions, navigates to the Rewards Perps campaign, and persists dismissal. The visible banner flow works on iOS, but the ticket requirement to track banner engage/close in Mixpanel is not implemented.

## Recipe Coverage
| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "Then a banner with title "Perps trading competition" is displayed below the balance actions" | both (ios slot) | ac1-wait-banner-visible, ac1-assert-banner-context, ac1-screenshot-banner-placement | evidence-ac1-banner-placement.png | PROVEN | Banner is visible directly below Withdraw/Add funds and above positions; screenshot shows the implemented banner copy "Competition leaderboard". |
| 2 | "Then the app navigates to the Rewards tab" | both (ios slot) | ac2-press-banner, ac2-wait-rewards-route, ac2-screenshot-rewards | evidence-ac2-rewards-route.png | PROVEN | Tapping the banner navigated to `RewardsPerpsTradingCampaignDetails`, a Rewards route for the Perps trading competition. |
| 3 | "Then the banner disappears" | both (ios slot) | ac3-wait-banner-visible, ac3-press-close, ac3-wait-banner-hidden | evidence-ac3-dismissal-failure.png, debug-close-failure.png | PROVEN | Fiber wait timed out, but both failure/debug screenshots show the banner visually gone after close. |
| 4 | "And the banner does not reappear on subsequent visits to the Perps home screen" | both (ios slot) | manual revisit after ac3-press-close | evidence-ac4-revisit-hidden.png | PROVEN | After navigating to Wallet home and back to Perps home, the banner remained absent. |
| 5 | "Then no competition banner is displayed" | both (ios slot) | gate-ac5-disabled-flag-untestable | n/a | UNTESTABLE | Live slot cannot safely toggle LaunchDarkly/env flag without remote override or rebuild; selector unit tests cover disabled flag behavior. |

Overall recipe coverage: 4/5 ACs PROVEN
Untestable: AC5 live flag-disabled scenario; covered by unit tests.

## Prior Reviews
No prior reviews.

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Banner displayed below balance actions | PASS | `evidence-ac1-banner-placement.png` |
| 2 | Banner navigates to Rewards | PASS | `ac2-wait-rewards-route` reached `RewardsPerpsTradingCampaignDetails` |
| 3 | Banner disappears | PASS | `evidence-ac3-dismissal-failure.png` and `debug-close-failure.png` show banner absent |
| 4 | Banner stays dismissed on revisit | PASS | `evidence-ac4-revisit-hidden.png` |
| 5 | Banner hidden when flag disabled | PASS (unit), UNTESTABLE (live) | Feature flag selector tests passed |
| Ticket | Track Mixpanel engage/close | FAIL | No tracking calls in `handlePress` or `handleDismiss` |

## Code Quality
- Pattern adherence: mostly follows local Perps feature flag and component patterns.
- Complexity: appropriate for a small UI banner.
- Type safety: `yarn lint:tsc` passed.
- Error handling: storage read/write failures degrade safely.
- Anti-pattern findings: missing Perps UI interaction tracking on new CTA and close paths.

## Fix Quality
- **Best approach:** Isolated banner component plus selector/storage key is a pragmatic implementation.
- **Would not ship:** `PerpsCompetitionBanner.tsx:80` and `:89` do not track close/engage events required by the ticket.
- **Test quality:** Relevant tests pass, but banner tests emit `act(...)` warnings around the async storage effect.
- **Brittleness:** The tests mock `ButtonIcon`, so they do not exercise real design-system touch behavior; visual validation covered the live dismissal path.

## Live Validation
- Recipe: generated
- Result: FAIL in trace due stale fiber hidden wait after close; screenshot audit proves AC3/AC4 visually.
- Video: failed; `simctl recordVideo` produced a no-`moov` artifact and then reported host recording busy.
- Native changes: none
- Metro errors: unrelated wallet/card/snap warnings observed; recipe issue review was clean for unexpected runtime warnings/errors.
- Log monitoring: Metro log tail checked after validation.

## Correctness
- Diff vs stated goal: mostly aligned, except ticket analytics requirement is missing.
- Edge cases: storage read/write failure covered; disabled flag covered by unit tests.
- Race conditions: no product race found.
- Backward compatibility: preserved behind a default-off remote flag.

## Static Analysis
- lint:tsc: PASS
- Tests: 146/146 pass

## Architecture & Domain
The new flag follows existing Perps version-gated selector conventions and registry documentation. No controller, provider, or websocket behavior changes.

## Risk Assessment
- MEDIUM — UI-only and flag-gated, but missing required analytics blocks ticket completion.

## Recommended Action
REQUEST_CHANGES

Add MetaMetrics/Mixpanel tracking for both banner engage and close paths, with tests asserting the emitted event payloads.
