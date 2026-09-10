# CI second-pass learnings

- Verify bot snippets against the analyzed SHA. The two empty-waitFor examples were absent; the actual positions-view callbacks all contain assertions and the info-button suite has no waitFor calls.
- clearAllMocks and resetAllMocks solve different problems. Inspect mutable mock overrides and beforeEach restoration instead of erasing stable factory implementations by default.
- Repeated CI alerts can represent an intentional unresolved release dependency. The four missing Core constants and blocked label must wait for the approved Core merge/release/adoption sequence.
- Use the checklist's no-change path when evidence finds no new code defect. Current remote unit results and source inspection were sufficient; another commit or testnet fixture would not resolve the dependency.
