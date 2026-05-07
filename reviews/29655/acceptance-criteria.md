# Extracted Acceptance Criteria

Source: PR body problem/solution and manual testing scenarios; no linked ticket criteria were provided.

1. Only one `PerpsConnectionErrorView` is displayed when multiple Perps provider stacks are mounted and the shared connection manager reports an error.
2. `PERPS_SCREEN_VIEWED` for the connection error screen fires exactly once for an error occurrence instead of once per provider instance.
3. The connection error view disappears and Perps content is restored when the connection error clears.
4. Tapping retry calls `PerpsConnectionManager.reconnectWithNewContext({ force: true })` and preserves a single visible error view.
5. Each retry attempt emits one connection-error screen-view analytics event with the updated retry attempt count.
6. Rapid error -> null -> error flaps within the debounce window do not emit duplicate connection-error screen-view events.
7. All route-level `PerpsConnectionProvider` instances suppress their own error UI so the centralized gate owns error rendering.
