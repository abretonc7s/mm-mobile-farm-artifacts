# Learnings — PR #29857

- **PerpsController `#initializationPromise` never rejects** — `#performInitialization()` catches all errors and transitions to `Failed` state. This makes `await #initializationPromise` safe in all callers.
- **`#initializationPromise` lifecycle**: assigned in `init()`, cleared on failure (allows retry), cleared on testnet/chain/account changes. Key invariant: `Initializing` state always has a non-null promise.
- **HyperLiquidClientService `isInitialized()`** requires all four clients (exchangeClient, infoClient, infoClientHttp, subscriptionClient) to be non-null. Missing any one means write operations fail.
- **`HyperLiquidWalletParams`** is just `signTypedData` + optional `getChainId` function references — not key material. Safe to store for reconnection.
- **Write vs read path distinction**: The PR correctly guards only write-path methods (placeOrder, closePosition, withdraw, etc.) with the init-await. Read-path methods (getPositions, getOrders) remain fail-fast.
- **`#createTransports()` always creates both WS and HTTP transports** — the `if (this.#httpTransport)` guard in `#handleConnectionDrop()` is purely defensive.
- **File size concern**: PerpsController.ts is 5,061 lines, PerpsController.test.ts is 6,613 lines. Both well over the 2,500 line guideline.
- **CDP limitations for this review**: Cannot simulate init races or WS drops via read-only CDP — these bugs can only be validated through unit tests or destructive state manipulation.
- **tsconfig.json local modification** (extends expo/tsconfig.base) breaks `tsc --noEmit` with TS5098. This is a slot-specific issue, not PR-related.
- **Navigation from Wallet to PerpsMarketTrade** requires being on the perps navigation stack first — `app-navigate.sh` alone doesn't work from Wallet home.
