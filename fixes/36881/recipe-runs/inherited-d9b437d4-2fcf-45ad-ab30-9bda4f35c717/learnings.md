- A recipe can pass while the app shows a Metro redbox: `ui.wait_for` matched testIDs under the overlay. Only reading the screenshot caught it. Reload after any transient working-tree state before capturing.
- Pressing a disabled `ListItemSelect` through `ui.press` fails the node ("no onPress prop"). For a "cannot pick" claim, run the bridge press in a `command` node with `allow_failure` and assert that output. On the unfixed build the press succeeds, so the node stays revert-sensitive.
- The harness ships `cdp-bridge.cjs eval-async` with `Engine` in scope. That gives a live controller read (`getMarginModeLock`) from a `command` node. Literal paths are required (`$HOME` is rejected).
- Switching between branches that differ in a yarn patch needs `yarn install` plus `mm-harness launch --verify`. `app.lifecycle restart` times out at 60 s while Metro rebundles node_modules.
- The independent review found real bugs in code that had already shipped live and passed 45/45: stale picks on A → B → A switches, and the wrong account selector. Three rounds were needed. Budget for review iterations when splitting a PR.

## Static self-review (rev-claude)
- Once Cross is available, an explicit `marginMode: 'isolated'` default makes HyperLiquid's pre-sign `#validateMarginMode` run on every order. The unset default skips it. Check the provider before choosing between "undefined" and "explicit default".
- Panel tests that mock the form hook can only prove wiring. Gate logic that lives in the hook needs its tests in the hook.
