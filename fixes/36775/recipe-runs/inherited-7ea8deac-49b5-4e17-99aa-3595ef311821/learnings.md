# Learnings — TAT-3985

- Investigation took most of the time. The formula was already correct; a fresh-REST probe (max−$0.05 accepted, max+$0.30 rejected) proved the problem was stale inputs plus zero headroom. Probing the exchange directly on testnet settled it in two calls.
- The bug is a price race, so pre-fix UI reproduction is probabilistic (~1 in 5 Max attempts on calm testnet BTC). Loop add-$20/remove-Max recipes until the marker fires, and assert deterministic proxies in recipes (zero-state explanation on a freshly opened position) instead of the racy outcome.
- A freshly opened isolated position sits exactly at the transfer-margin floor, which gives a deterministic "$0 removable" fixture via `metamask.perps.place_order`.
- The first fix still failed live: the view's own validation compared input to the headroom-reduced max, so a 1-cent tick after Max disabled Confirm. Validate against the exchange boundary; offer the buffered value.
- Tooling drift: `mm-harness validate` does not exist (use `run --plan`); `read_positions` omits margin fields; source edits need `app.lifecycle restart` (`MOBILE_SOURCE_NOT_LOADED`); DevLogger output lands in `app-console.log`, not `metro.log`; `ui.wait_for` text needs `text_match: contains` without a test_id.
- Cross margin was flag-gated for display only; the remote dev config already served the flag on, so "PM can't test" meant the trading path was never wired. Checking the live flag value (`metamask.feature_flags.read`) separates "flag off" from "feature unwired" in one call.
- Sending `marginMode` surfaces a latent controller gap: `flipPosition` re-applies isolated leverage and the venue rejects it for Cross positions. Mobile disables Reverse for Cross; the Core fix is to pass `position.leverage.type` in flip.
- Pro positions sit below the order form: `ui.scroll` could not bring the card into view, `ui.swipe` (target + duration_ms required) did.

## Self-review (rev-claude)
- `git diff main...HEAD` in the template is stale-prone; `origin/main...HEAD` gave the real 32-file diff.
- zsh does not word-split `$tests`; pass the changed test list as an array. `.view.test.tsx` files need `-c jest.config.view.js` or they match 0 tests.
- `PerpsOrderLifecycleFlow.view.test.tsx` flakes (2 of 4 combined runs) on a post-teardown haptic (`gates.ts` reading `Platform.OS`); it passes solo. The leak exists independently of this branch.
- Extension `marginUtils.ts` still offers the exact boundary with no headroom, so it likely has the same rejection. Worth a parity ticket.

## Self-review fix pass
- Absence assertions should target testIDs, not copy: `queryByText(...)).not.toBeOnTheScreen()` passes vacuously when a label changes.
- Recipes that assume live testnet state (an open BTC position) go stale overnight; converge with `ensure_positions` instead of asserting.
- `review-feedback.md` referenced by the checklist was missing; the issue text in SELF-REVIEW-FIX.md was enough to act on.
- Loop 2: a quick mutation check (revert the guard, rerun one test, restore) confirmed the rewritten test fails without the fix, which is stronger than just reading the diff.

## Static self-review (rev-codex)
- A successful fresh read with no matching position is distinct from a failed read; treating both as `null` lets a closed or liquidated position reach `updateMargin`.
- The zero-state tests need a retained nonzero input followed by a live maximum falling to zero; an initial zero input disables Confirm for unrelated reasons.
- Mobile's buffered maximum and pre-submit read have no Extension counterpart yet; the parity check found a real divergence but Mobile remains the reference implementation.

## Self-review fix pass 2
- A "fail open" fresh read must distinguish "read failed" (unknown, submit) from "read succeeded without the position" (closed, stop); collapsing both into null let a closed position reach the exchange.
- Disabling inputs isn't a zero state: Confirm and the submit guard need the same flag, or a retained amount still submits.
- `metamask.perps.ensure_mode` only proves the mode on a market screen; run it after navigating, or it reports "alreadySelected" without acting.
- `idb ui swipe` failing with "Mach port invalid, device disconnected" is a stale idb companion; `idb kill` fixes it.

## Static self-review continuation (rev-codex)
- The exact commit range kept this follow-up focused on six files and the three earlier findings.
- A successful empty position read and a failed read need separate results; the new sentinel makes that distinction explicit at submission.
- Transition tests must retain a nonzero amount before reducing the live maximum to zero, so they exercise the submit guard rather than the default empty amount.
