# Learnings

- **The root cause was in `node_modules`, not the app.** React Navigation v7's `StackRouter`
  NAVIGATE case only pops back to an existing entry when `pop: true` is set; otherwise it pushes a
  duplicate. Reading `@react-navigation/routers/src/StackRouter.tsx` and
  `core/src/useNavigationBuilder.tsx` took ~10 minutes and settled it outright. Three tickets
  (TAT-3906, TAT-3838, TAT-3874) collapsed into one two-line fix. Worth grepping `{ pop: true }` in
  this repo first — Bridge, Card, QrSync and the deeplink handlers already hit this.

- **`cdp-bridge.cjs get-state` is the single best debugging tool for navigation bugs** and is not
  mentioned anywhere in the task docs. It dumps the whole React Navigation tree, so the bug is a
  literal array read (`[..., RedesignedConfirmations, PerpsMarketDetails]`) instead of a theory.
  `mm-harness actions` does not surface it; `node <harness>/adapters/mobile/bridge-runtime/cdp-bridge.cjs`
  with no args lists `get-route`, `get-state`, `eval`, `press-test-id`, `go-back` and more.

- **`mm-harness call` defaults to watcher port 8161, not the slot's port.** Every `call` needs
  `--watcher-port 8061` explicitly or it fails with `METRO_UNREACHABLE`; `run` needs it too even
  when `--slot macwork-mmdev-1` is passed. This cost several wasted cycles early on.

- **`ui.wait_for expected: "visible"` is unreliable in this app.** Fixed footer buttons
  (`perps-market-details-long-button`, `perps-order-view-place-order-button`) and
  `perps-home-heading` all report `present: true, visible: false` while plainly on screen, and
  `ui.scroll scroll_into_view` fails on the footer with "No scrollable near testID". Three recipe
  iterations were burned on this. Gate on `present` and let the screenshot carry the visual claim.

- **Perps market state silently changes which controls exist.** Once a position is open the market
  page renders Close/Modify instead of Long, so a rerun of the same recipe presses a button that no
  longer exists and the press appears to "hang". `metamask.perps.start_state` with
  `profile: clean_market_testnet` is mandatory setup, not optional hygiene. Also note the app
  restores its navigation stack across relaunch, so stale duplicate routes survive a restart —
  back out to wallet home before re-running.

- **The harness refuses to run when the loaded bundle is stale** (`MOBILE_SOURCE_NOT_LOADED`).
  Every source edit needs `mm-harness call app.lifecycle --arg command=restart` before the next
  recipe run. Useful guard, but budget ~2 minutes per edit/validate cycle.

## Self-review (rev-claude)

- **Reading `node_modules` beat reasoning about the fix.** The worker's root-cause claim was
  verifiable in ~3 minutes by reading `StackRouter.tsx:385-396` and `:456` plus
  `useNavigationBuilder.tsx:692-742`. That also answered three review questions the diff alone could
  not: `pop` cannot double-fire (guarded by `isNestedParamsConsumed`), a missing target degrades to
  the old push instead of failing, and no `getId` exists on `MARKET_DETAILS` to pre-empt the pop
  branch. Verifying a navigation fix without opening the router source is guesswork.

- **`pop` belongs in the nested screen params, not the third `navigate` argument.** Most repo
  precedent uses `navigate(name, params, { pop: true })`, which targets the *parent* router. For a
  nested navigator the flag has to ride inside `{ screen, params, pop }` so it reaches the child.
  Nearly flagged the diff for not matching the majority pattern — the two forms are not
  interchangeable.

- **Lint baselining is worth the extra command.** `--max-warnings=0` failed with 7 warnings, all
  pre-existing. Diffing the same lines against `origin/main` (including confirming the deprecated
  `navigate` call sat at `:238` before and `:247` after) separated legacy debt from introduced
  problems and kept the verdict honest.

- **The only blocker was hygiene, not behavior.** The fix, tests, recipe, and screenshots all held
  up; what failed review was five ticket references deleted from unrelated comments. Checking
  whether the convention is real (`git grep -o "TAT-[0-9]*"` → 69 hits across 43 files) turned a
  style opinion into a defensible finding.

- **Screenshot claims need reading, not trusting.** The `after` PNG's real strength was not the
  Perps home header but the BTC 3x long in "Your positions", which proves it is the post-order state
  rather than an unrelated home screen. Filename and recipe pass status would not have shown that.

## Self-review fix pass

- **A reviewer finding can be correct and still not be the right action.** The only blocker was five
  ticket references stripped from comments, and the reviewer's case was well evidenced (69 `TAT-`
  refs across 43 Perps files). But those removals came from an explicit operator instruction given
  mid-run. Silently restoring them to satisfy a bot would have reversed a human decision; the fix
  loop's own "don't apply a change just to silence the reviewer" clause exists for exactly this.
  Surfacing the conflict cost one question and produced a decision on record in `report.md`.

- **Take the reviewer's non-blocking notes seriously — one was about my own new text.** The doc
  comment I wrote for `pop: true` asserted all six `useNavigateToPerpsHome` callers sit above the
  target, which is false for `BrowserTab` and `PerpsDetails`. That was the only genuine defect this
  pass found, and it was filed under "non-blocking" rather than in the Issues list.

## Self-review round 2 (rev-claude)

- **A declined finding is closed, not pending.** Round 1's only blocker was the five stripped ticket
  references. Round 2 found them still stripped — but `report.md` records the operator instructing
  the removal and reaffirming it when the finding was put back. Re-raising it would have started a
  loop the human had already ended. The check that mattered was reading the worker's report before
  re-diffing, not after.

- **Re-review the delta, then re-verify the whole.** `132af96bbac` was five comment lines in one
  file, but lint, all three suites, the recipe trace, and the contract gate still got re-run. Two of
  those (byte-identical lint output, unchanged recipe hash) were what proved the delta introduced
  nothing — a claim that reasoning about a comment-only diff cannot make on its own.

- **Promoted evidence can drift from the latest run.** The `after` PNG in `artifacts/` was from the
  17:28 run while the post-fix re-run wrote a newer one to `recipe-run/screenshots/` at 18:10, with a
  different hash. Reading both settled it (same screen, same position) instead of assuming the
  promoted file was current. Worth checking hashes whenever a re-run happens after evidence was
  promoted.

- **A recipe that places a real venue order will flake on venue state.** The first re-run failed at
  `ac1-wait-position-open` because Hyperliquid testnet was rejecting market orders post-upgrade
  (`"Only post-only orders allowed immediately after network upgrade"`). The Metro log turned what
  looks like a fix regression into an obvious external cause in one read.

- **A red regression gate is not automatically your regression.** `ac1-wait-position-open` failed on
  a comment-only change, which is impossible as a code defect. Metro had the real reason:
  Hyperliquid testnet answered `"Only post-only orders allowed immediately after network upgrade"`,
  so the market order could not fill. Reading the provider response before touching the diff saved
  chasing a phantom; a retry 60s later passed clean.
