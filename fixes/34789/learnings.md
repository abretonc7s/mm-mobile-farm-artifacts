# Learnings — PR #34789 review round

- **A debounced verdict and a synchronous one must be gated together, not alternately.** The
  upstream worker correctly stopped trusting the unresolved balance (`isPayBalanceLoading` gates
  the button) and correctly computed the resolved shortfall (`hasInsufficientPayTokenBalance`
  drives the funding message) — but each guard covered a different phase and neither covered the
  handoff between them. The 300 ms `PERFORMANCE_CONFIG.ValidationDebounceMs` window where the
  loading gate has dropped and the debounced `isValid` has not yet caught up was invisible from
  either guard's own point of view.

- **"The message renders from X, the button gates on Y" is a latent contradiction.** The PR's own
  stated goal was that the funding banner "compares against the same balance as validation and the
  slider so the two can no longer disagree". The place-order button was never brought into that
  same-source rule. Whenever a screen commits to one source of truth for a state, every affordance
  reading that state — including disabled-ness — has to be enumerated, not just the visible copy.

- **The bot's diagnosis was half wrong and still worth acting on.** Its first claim (unresolved
  balance leaks the Perps balance into validation) was already handled; only the second half was
  live. Triaging the halves separately, rather than accepting or rejecting the comment whole, is
  what kept the fix to two lines instead of re-plumbing `effectiveAvailableBalance`.

- **Prove the regression test by reverting the fix.** Because the default validation mock in this
  suite already returns `isValid: true`, a test asserting the button is disabled could pass for the
  wrong reason. Temporarily removing the two `isDisabled` lines and confirming the new test fails
  was the only thing that established it actually guards the window.

- **Recipe re-validation after a rebase earns its cost twice.** The inherited 21-node recipe was
  re-run against `branch + origin/main` (12 commits replayed, `yarn.lock` moved so deps were
  reinstalled) and passed unchanged, which validated both the merge and the fix in one pass — and
  the evidence screenshot doubled as proof the new gate does not over-block a fundable order.
