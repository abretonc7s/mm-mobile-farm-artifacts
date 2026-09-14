# Learnings

- Header-only `canGoBack` fixes miss native-stack swipe and Android hardware back. Those still dispatch GO_BACK/POP, so the same dropped-Home single-entry stack pops `PERPS.ROOT` unless `beforeRemove` shares the fallback.
- Stamping only the replace path is not enough. `dropPerpsHomeFromStackHistory` can leave `[MARKET_LIST, MARKET_DETAILS]`; a later list `push` without `preserveHomeDroppedFromHistory` looks like an Explore entry.
- Extra route params compile until they are on `PerpsStackParamList`. Home→Pro resets already dropped the stamp that way. Type the flag on every route the helper writes.
- List back is a second copy of the header hole. After Home is dropped, market back pops to the list, then list `navigateBack` pops out of Perps.
