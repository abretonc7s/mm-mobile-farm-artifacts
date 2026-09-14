# Learnings — PR #36068 pr-complete

- No reviewer-driven learnings — no actionable comment fixes on this run.

- After rebasing onto main, `yarn.lock` can change even when `git diff origin/main -- yarn.lock` is empty. Compare against the pre-rebase SHA and reinstall before `lint:tsc`. The first typecheck failed on `AuthenticationController.clearState` from a package bump that was not in this PR.

- The inherited recipe still assumes the slot is already in Pro mode. `open-market` does not switch mode, so a Lite slot fails at `await-order-form`. `metamask.perps.ensure_mode mode=pro` is the recovery; do not rewrite the recipe.

- `ensure_unlocked` can fail its stability window while the app is actually unlocking (account-discovery timeouts). That is not a product regression in this branch.
