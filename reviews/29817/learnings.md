# Learnings — PR #29817

- **TradingService error logging has two formats:** catch blocks use verbose `{tags, context: {name, data}}` format; non-throwing failure paths use lightweight `#getErrorContext` returning `{controller, method, ...}`. Both route to Sentry but produce different event shapes.

- **`ensureError` utility** at `app/util/errorUtils.ts` handles string, undefined, null, and Error inputs — safe to use for provider error strings that may be undefined.

- **Perps error reporting layers:** Controller (TradingService) owns Sentry reporting via `logger.error`. UI hooks own toast notifications and `onError` callbacks. Duplicating Sentry calls in both layers causes double-reporting.

- **TradingService write methods follow a consistent pattern:** try block with success/failure branches + catch block for exceptions. The failure branch (`{success: false}` result) was previously not logging to Sentry in several methods — only the catch branch (thrown exceptions) was covered.

- **Batch operations (cancelOrders, closePositions)** have two code paths: native batch (`provider.cancelOrders`) and fallback per-item loop. The `provider.cancelOrders &&` guard correctly scopes batch-level logging to the native path only.

- **File size concern:** TradingService.ts (2,119 lines) and its test file (2,413 lines) are both above the 2,000-line threshold. The service handles 7+ operations with similar boilerplate — ripe for extraction into per-operation modules.

- **CDP eval on this slot** had intermittent issues with background command output not being captured. Direct foreground execution works but background tasks may silently produce empty output files.

- **Recipe skip decision for pure logging PRs:** When all claims concern internal error logging with no UI surface, skipping the recipe is correct — unit tests are the right proof mechanism. No value in a visual walkthrough.

- **Pre-existing Metro warnings** (Spinner module resolution, react-native package.json) are noise in log monitoring — filter these out when checking for PR-specific errors.
