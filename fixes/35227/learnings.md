# Learnings

- Live `currentPrice` on the same overlay payload as limit orders means every tick re-sends the full auxiliary-line message. Limit line updates have to be idempotent and must not force Y-axis autoscale.
- The PR already documented autoscale as `autoscaleInfoProvider` only, but `updateLimitOrderLines` still called `applyOptions({ autoScale: true })`. That contradiction is what Bugbot and geositta caught.
- Template-string tests that only grep source do not cover WebView overlay behavior. Extracting the overlay helpers made tick-skip and cancel-clear assertions possible.
- Rebase onto newer main can drop packages (`@rive-app/react-native`) even when the feature branch itself did not touch `yarn.lock`. `yarn install --immutable` after rebase is required before `lint:tsc`.
- Recipe re-validation can fail at wallet unlock (Login + CDP timeout) with a healthy Metro/bridge. That is environment, not overlay logic.
