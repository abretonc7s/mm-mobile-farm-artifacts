# Fix Quality

Best approach:

- Centralizing the visible error screen in a single gate and suppressing provider-level error UI is the right broad shape for the stated duplicate-rendering bug.
- The pragmatic fit is good for UI rendering and analytics dedupe, but two details should be fixed before merge:
  - The debounce constant is `150` ms while the PR claims 1 second. This can fail the stated rapid-flap behavior for flaps between 151 ms and 1000 ms.
  - Suppressed providers still emit the old provider breadcrumb on errors, so the PR does not fully address the stated Sentry inflation/mislabeled "view shown" breadcrumb problem.

Test quality:

- The new tests directly cover single rendering, child restoration, retry force option, retry attempt count, analytics dedupe, polling cleanup, and suppressed child rendering.
- The tests are useful and would catch reverting the gate analytics movement or removing `suppressErrorView` from the route-level providers.
- Missing coverage: no test asserts the stated 1-second debounce window, and no test asserts suppressed providers stop emitting error-view breadcrumbs.

Brittleness:

- The gate adds a second 100 ms polling loop in addition to provider polling. It is acceptable for this narrow PR but would be cleaner long-term if the connection manager exposed a subscription-based state API.
- The 150 ms debounce is currently a module constant with no tie to a shared config or the documented behavior.
