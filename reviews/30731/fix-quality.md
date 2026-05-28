## Fix Quality

- Best approach: The feature split is reasonable: feature flag selector, isolated banner component, storage key, and Perps home insertion are all small and local.
- Would not ship: Engage and close handlers do not track MetaMetrics/Mixpanel events, while the linked ticket explicitly calls for engagement and close tracking.
- Test quality: Unit tests cover rendering, flag gating, dismissal persistence, navigation, and custom test ID. They miss the real design-system touch/responder behavior because `ButtonIcon` is mocked as a simple touchable.
- Test quality: The live recipe found that fiber-based hidden assertions can remain stale after visual dismissal, so screenshot evidence is stronger for this visual claim.
- Brittleness: The component test emits React `act(...)` warnings from the async storage read effect, which is not a product blocker but indicates the tests are not fully synchronized with the component lifecycle.
