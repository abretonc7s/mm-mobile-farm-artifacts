# Recipe coverage

Inherited recipe `artifacts/recipe.json` was reviewed but could not be re-executed in this run.

| Proof target | Recipe nodes | Result |
|---|---|---|
| PT-1: selectable TWAP tab beside Positions and Orders | `wait-twap-tab`, `open-twap-tab`, `capture-twap-tab` | SKIPPED — iOS runtime verification failed during bundle prewarm |
| PT-2: Active, History, and Fill History views | `wait-view-active`, `wait-view-history`, `wait-view-fill-history` | SKIPPED — iOS runtime verification failed during bundle prewarm |
| PT-3: shared side/ticker filters and idle plain-TWAP label | `wait-side-filter`, `wait-ticker-only`, `capture-twap-tab` | SKIPPED — iOS runtime verification failed during bundle prewarm |

`mm-harness launch ios --verify` retried once after Metro recovery and both attempts failed because `node_modules/css-select/node_modules/domutils/package.json` was missing. No current-run recipe assertions or screenshots are claimed. The inherited family package remains referenced by `artifacts/latest-valid-recipe-run.json`.
