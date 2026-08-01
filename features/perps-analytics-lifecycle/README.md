# Mobile Perps analytics lifecycle evidence

This bundle records a live iOS run of the composable Mobile Perps analytics
recipe. The running app navigated from Home to the visible Perps market list,
then its real MetaMetrics client delivered the measured events to the local
Segment-compatible collector.

## Result

- 10/10 recipe nodes passed in 32,461 ms.
- Exactly one `Perp Screen Viewed` and one `Asset Viewed` matched the required
  Perps-home properties.
- The run used `--heal off`; it performed no rebuild, restart, recovery, or
  runtime mutation.
- Product checkout: `MetaMask/metamask-mobile@200c45b10127390149a0b3b32f3107c1da8e26fb`, clean at execution.
- Recipe library: `MetaMask/experimental-metamask-recipe-perps@c7cd11526ba85c2601463ede7f8cdf9697e8bde0`, `dirty: false` in provenance.
- Runner: `MetaMask/experimental-metamask-harness@19a06b6e6ccd886f0a1d3c5b0be16acaa022b9ab`.
- Runtime: `@farmslot/recipe-harness@0.11.0`.

Review [summary.json](summary.json) for the verdict and provenance,
[trace.json](trace.json) for node outputs and counted assertions, and
[diagnostics.json](diagnostics.json) for retained non-blocking application
findings.

## Reproduction

```sh
mm-harness run /path/to/experimental-metamask-recipe-perps/recipes/perps/analytics-lifecycle.mobile.recipe.json \
  --adapter mobile \
  --target /path/to/metamask-mobile \
  --device <device> \
  --library perps=/path/to/experimental-metamask-recipe-perps \
  --heal off \
  --artifacts-dir temp/recipe/mobile-analytics/composable-live-clean \
  --json-stream
```

The installed Mobile bundle must already point its Segment data endpoint at
the loopback collector and retain a valid product write key. The recipe enables
consent before its measurement cursor.

## Publication safety

Local absolute paths, the disposable fixture account, and the simulator ID are
replaced with descriptive placeholders. `SHA256SUMS` covers every published
file other than the checksum file itself.
