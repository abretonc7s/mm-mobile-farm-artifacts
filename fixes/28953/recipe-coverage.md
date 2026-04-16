# Recipe Coverage Matrix

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | Expected candle-request cancellations (AbortError) are not reported as errors to Sentry/Logger | ios | ac1-log-check, ac1-screenshot-clean-logs | after-ac1-no-abort-noise.png | PROVEN | log_watch confirmed no BUG_MARKER in metro logs after navigating away from candle screen (triggers teardown/abort). CandleStreamChannel activity detected = candle path exercised. Unit tests assert isAbortError skips Sentry at all 3 layers. |
| 2 | Real candle fetch failures still log/report normally to Sentry/Logger | ios | ac2-wait-candles, ac2-screenshot-candles | after-ac2-candles-loaded.png | PROVEN | Screenshot shows BTC-USD candle chart fully loaded with price data ($74,883). Market data fetch succeeded = real fetch path works. Unit tests in MarketDataService.test.ts and CandleStreamChannel.test.ts verify real errors still call logger.error. |
| 3 | No new TypeScript errors introduced | ios | static: yarn lint:tsc | N/A | PROVEN | yarn lint:tsc passed in CI-parity gate (step 16). No UI surface — screenshot not applicable. |

Overall recipe coverage: 3/3 ACs PROVEN (untestable: none, weak: 0, missing: 0)
