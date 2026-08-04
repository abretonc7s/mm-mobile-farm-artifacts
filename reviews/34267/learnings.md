# Learnings — PR #34267 review

## Harness / runner

- **`mm-harness` CLI has drifted from the TASK template.** The template's `launch --platform ios --preflight-mode fast --artifacts-dir …` and `run … --project-root` are all rejected. Current grammar: `mm-harness launch ios [--verify] [--json]`, and `run <recipe> --target <path>` (not `--project-root`). `mm-harness status --json` is the cheapest way to see slot/device/bridge state before launching. Always run `--help` before trusting a templated invocation.
- **`mm-harness call <action> --arg k=v --json` is the fastest probe loop.** Far quicker than authoring a throwaway recipe when you just want to know whether a testID exists or what text a node exposes.
- **Recipe `intent` strings are lint-gated.** `validate.schema` rejects an intent that "repeats an action, node id, selector, or generic verb" — writing `"Scroll the orders list…"` on a `ui.scroll` node fails. Phrase intents as the *human-visible goal* ("The stop trigger order sits further down the list; bring that card into the visible viewport…"). Cost me two dry-run cycles.
- **`--plan` catches this statically and touches no device.** Always dry-run before burning a live run.

## Mobile assertion capabilities (important for future perps recipes)

- **`ui.wait_for` `text` matching is SHALLOW.** It validates only the text belonging to the node carrying that testID, not the subtree. `ui.wait_for test_id=perps-pro-market-positions-panel text="Stop market"` fails with `last text="Positions (3)"`; an order row returns just `"BTC"`. Do not assume a container testID lets you assert descendant copy.
- **It *does* resolve `accessibilityLabel`.** `ui.wait_for test_id=perps-pro-order-form-size-input text="Size (USD)"` passes because `PerpsProCompactInput` sets `accessibilityLabel={label}` on the `TextInput`. This is a great trick for asserting labels that have no testID of their own — check whether the component forwards the label to `accessibilityLabel` before declaring a claim unassertable.
- **Negative `delta_y` on `ui.scroll` snaps the outer scroll view to the top** rather than scrolling up a little. `-230` and `-500` both jumped fully to the top. To frame content higher, reduce the *initial* downward delta instead of scrolling back up.
- **Avoid indexed order-row testIDs** (`perps-pro-market-order-row-<SYMBOL>-<index>`). Any setup step that creates an order reshuffles the indices. Sort appears to be newest-first, so a freshly created order takes index 0.

## Perps Pro navigation

- **`ui.navigate page=perps-market` lands on `PerpsMarketDetails`, which is a router, not the Pro view.** `PerpsMarketDetailsRouter` renders Pro only when the remote flag `perpsProModeEnabled` is on **and** the persisted controller mode is `PerpsMode.Pro`.
- **Toggle to Pro by pressing `perps-mode-toggle-lite`.** In `variant="active"` (the market header pill) the testID reflects the *current* mode and pressing flips to the other one — so `perps-mode-toggle-pro` does not exist while you are in Lite. Counter-intuitive; cost a failed press.
- Mode is persisted, so once flipped the slot stays in Pro across runs. Gate on `ui.wait_for test_id=perps-pro-market-view` so a silent Lite fallback fails loudly instead of producing misleading evidence.
- The Pro positions/orders panel lists orders across **all** markets, not just the market you are viewing — useful, since you can prove multi-market pill copy from a single market screen.

## Codebase patterns worth remembering

- `detailedOrderType` is **provider-native text**, not an enum. HyperLiquid returns exactly `DETAILED_ORDER_TYPES` (`Limit`, `Market`, `Stop Limit`, `Stop Market`, `Take Profit Limit`, `Take Profit Market`); `myxAdapter.mjs:308-317` returns `Take Profit` / `Stop Loss` / `Liquidation`, which are **not** in that set. Any UI rendering `detailedOrderType` directly is provider-dependent by construction — a fast, high-signal thing to grep for in perps review.
- **Checking locale coverage is cheap and finds real regressions.** A ~10-line Python pass over `locales/languages/*.json` proved `perps.order.market`/`limit` are translated in 13 locales, which turned "this looks like a hardcoded string" into a quantified regression. Worth doing on any PR that removes a `strings(...)` call.
- Orphaned locale keys are easy to miss: `rg 'order_card\.(take_profit|stop|open_limit|close_limit)' app` found five dead keys the PR created. Do this whenever a PR deletes a function that called `strings(...)`.
- Test revert-sensitivity is checkable by inspection: mocked `strings` implementations that fall back to `|| key` mean a stale key renders the raw key, so an exact `getByText` assertion still fails on revert. Good pattern; worth confirming rather than assuming.

## Process

- **`mark N` numbering ≠ the visible step numbers in TASK.md.** `enumerateChecklistCheckboxes` counts every `- [ ]` outside skipped sections, and the PR template's "Performance checks" block (3 boxes) is *not* skipped while "Pre-merge author/reviewer checklist" is. Net offset here: visible step N = `mark N+3`. Verify by running the enumerator before marking, or the first `mark 1` silently checks a PR-template box.
- **A green recipe is not proven evidence.** Three consecutive runs passed 22-23/23 nodes while the claim-2 pill sat outside the captured frame. Only reading the PNGs caught it. Node status answers "did the step run", not "does the image show the claim" — the step-32 image read is doing real work, not ceremony.
- Grouping both halves of an AND-claim into a single frame (SOL `Limit` directly above ETH `Stop market`) is stronger and shorter than two separate screenshots.
