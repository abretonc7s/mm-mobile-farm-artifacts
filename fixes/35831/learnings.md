# Learnings — PR #35831 review round

- Duplicate keys in `en.json` fail silently: JSON keeps the last definition, so new copy added earlier in the same object never renders. Grep the target object for existing keys before adding strings.
- Reusing an existing label ("Margin used") for a different scope on the same screen was caught by review. An earlier test had already worked around it with `getAllByText(...).toHaveLength(2)`; a test accommodating duplicate text should prompt a label review.
- A privacy-masking test that leaves the feature flag off only covers the old branch. When a component is flag-gated, tests for the new branch must enable the flag and assert the new text is absent.
- Label copy changes ripple into tests that use real strings (`PerpsProPositionCard.test.tsx`) and into recipe text assertions; run all affected suites, not only the file under review.
- Recipe replay needs the shared testnet account empty. A foreign open position (an isolated BTC position this task did not create) blocked fixture setup; I stopped and asked rather than closing it, and the operator's call was to clear it. Worth surfacing the choice early instead of terminating the run as blocked.
- Raw `evalAsync` against the CDP bridge timed out repeatedly outside a harness run, while the identical script succeeded through `mm-harness call command`. Drive bridge work through the harness rather than importing the bridge directly.
