# Recipe coverage

The inherited recipe was re-executed on iOS simulator `mm-3` against commit `cc4df7c6345174fd97654dcfb7fd4c9502f3a79f`. The run passed 13/13 nodes; see `artifacts/recipe-run/summary.json`, `trace.json`, and `artifact-manifest.json`.

| Proof target | Recipe nodes | Result |
|---|---|---|
| PT-1: selectable TWAP tab beside Positions and Orders | `wait-twap-tab`, `open-twap-tab`, `capture-twap-tab` | PASS for selector presence and interaction; visual capture framing gap noted below |
| PT-2: Active, History, and Fill History views | `wait-view-active`, `wait-view-history`, `wait-view-fill-history` | PASS — all three target selectors were present |
| PT-3: shared side/ticker filters and idle plain-TWAP label | `wait-side-filter`, `wait-ticker-only`, `capture-twap-tab` | PARTIAL — filter selectors passed; the uncounted label is not reviewable in the screenshot |

The PNG at `artifacts/recipe-run/screenshots/evidence-twap-tab.png` was read. It shows the upper BTC TWAP order form, including Runtime and Randomize, but not the management panel claimed by the capture node. It is therefore excluded as standalone proof for PT-1/PT-3. The review fix in this run (multiple accepted termination guards) is covered by focused unit tests rather than this inherited structural recipe.
