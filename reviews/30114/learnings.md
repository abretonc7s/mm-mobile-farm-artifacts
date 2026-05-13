# Learnings — PR #30114

- HyperLiquid has multiple abstraction modes (`dexAbstraction`, `default`, `disabled`, `unifiedAccount`, `portfolioMargin`) with different migration paths — `dexAbstraction` requires user-signed EIP-712, while `default`/`disabled` use silent agent transitions.
- MetaMask supports 5 hardware keyring types: Ledger Hardware, Trezor Hardware, OneKey Hardware, Lattice Hardware, QR Hardware Wallet Device. These are inlined as strings (not imported from `@metamask/keyring-controller`) to keep the perps service portable.
- The `#ensureUnifiedAccountEnabled` method has a layered guard structure: compatible mode check → defer check → unknown mode bail → migration dispatch. Understanding this ordering is critical for reviewing changes to the migration flow.
- TradingReadinessCache is a global singleton that survives provider reconnections — important for preventing repeated signing prompts across session boundaries.
- The `MIGRATABLE_ABSTRACTION_MODES` set in `hyperLiquidAbstraction.ts` and the explicit guard in `HyperLiquidProvider.ts:747-751` must stay in sync — a potential maintenance hazard worth watching.
- CDP returning empty `[]` from `app-state.sh status` means the bridge is not connected, not that the app is healthy with no data. Future reviews should treat this as offline.
- Circuit breaker warnings in metro.log are normal during provider reconnections and not indicative of PR-related issues.
- `HyperLiquidProvider.ts` (8,633 lines) and its test file (10,751 lines) are the largest files in the perps domain — any PR touching them should consider extraction opportunities.
