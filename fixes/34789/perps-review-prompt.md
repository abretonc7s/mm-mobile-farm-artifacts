Fresh full review of PR #34789's Perps changes at commit 16cfc2e940b8247f81cce2e516d7fa4fbe9cdf74 versus merge base 19c16f08452d2f5445887275fbad59f477756d0e. No prior review context or findings should influence this review.

You are in an immutable read-only worktree pinned to the reviewed commit. Do not modify files, switch commits, or use the live checkout as the review target. Run any inspection command only from your current `/tmp/perps-review-16cfc2e940b.eLOew3/repo` worktree. Do not `cd` to `/Users/deeeed/dev/metamask/metamask-mobile-2`; that path is supplied below only to read the installed knowledge files. Do not rerun tests: the orchestrator already proved 4/4 targeted suites with 237/237 tests, the component-view suite with 5/5 tests, TypeScript, formatting, scoped ESLint with 0 errors (the 7 reported warnings all predate the merge base), and `git diff --check` at this exact commit. The complete diff is exactly 7 files and 984 changed lines, below the repository's 1,000-line check; the final commit only consolidates duplicate test scaffolding and does not change production code.

Before reviewing, read and enforce every Perps knowledge file below:

- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/review-antipatterns.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/architecture.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/connection-architecture.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/caching-architecture.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/formatting-rules.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/mobile-extension-map.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/shared-package-analysis.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/feature-flags.md
- /Users/deeeed/dev/metamask/metamask-mobile-2/.agents/skills/mms-perps-review-pr/knowledge/screens.md

Authoritative scope boundary from the human confirmations reviewer:

- They agree usePayTokenAccountBalance should make a missing balance explicit.
- Perps should consume that explicit state and disable its CTA when there is no pay token or balance.
- Standard Footer, CustomAmountInfo, Pay With row migration, preferred-token, toast, confirmation-wide gating, minimum-order validation changes, funding-message redesign/deduplication, Runway, and native runtime changes are out of scope. They are absent from this final seven-file base diff and preserved separately only as optional draft references where applicable.
- The primary goal is the minimal TAT-3742 Lite Perps fix: use the matching live wallet-token balance instead of a stale snapshot; represent a missing pay token or matching balance explicitly; avoid transient fabricated-zero/contradictory funding UI; keep the Place Order CTA visible and fail-closed; and preserve the last usable form/slider capacity only for the same transaction-account-or-selected-group + normalized chain + normalized token while the live balance is unresolved. A brand-new unresolved source receives an internal fail-closed capacity cap of zero instead of falling back to Perps funds; readiness is carried separately so this cap is never rendered as a measured wallet-token zero.
- Existing message placement and unrelated validation behavior should otherwise remain unchanged. The USD-dependent `InsufficientPayTokenBalance` alert and generic balance error are hidden while live USD balance is unresolved; `InsufficientPayTokenFees` is hidden only while live raw balance is unresolved; native-gas, no-quote, minimum-order, and protocol validation remain visible and blocking. The focused whole-view unit tests use the real order provider/form boundary because component-view presets cannot drive transaction-pay readiness/account-token transitions; the live recipe covers the rendered device flow, and the unchanged component-view suite remains green.
- An unresolved balance disables and directly guards Place Order, but intentionally does not show a loading spinner: a missing matching token or fiat rate can remain unresolved, so tying the button's loading state to readiness could create a permanent spinner. Treat that non-spinner fail-closed behavior as intentional unless you find a concrete correctness issue.
- Existing non-opt-in confirmation callers must preserve exact chain-ID matching and their snapshot fallbacks. Only the explicit live-balance overload canonicalizes equivalent EVM hex chain IDs; arbitrary CAIP/non-EVM asset IDs must remain safe to inspect. Live matching, fiat-rate lookup, and the Perps retention key share that safe normalizer.
- The resolved insufficient-balance CTA gate is intentionally synchronous: order validation is debounced after its first run, so this Perps-local check closes the render window before validation state catches up. It does not add confirmation-wide gating.
- Do not require a new terminal message for a live balance that remains unresolved. Distinguishing loading from a permanently missing token/rate and choosing new copy is a broader funding-UX/product change; this PR intentionally keeps the normal long/short label visible but disabled and hides fabricated balance messaging.
- The disabled-button regression deliberately invokes the underlying press callback to prove the direct handler guard; a normal `fireEvent.press` cannot exercise that callback once the design-system button is disabled.

Review the complete diff, not only the latest commit: git diff 19c16f08452d2f5445887275fbad59f477756d0e..16cfc2e940b8247f81cce2e516d7fa4fbe9cdf74.

You gate this before any human sees it. Every Perps anti-pattern and every nit (correctness, races, hooks, naming, magic numbers, missing testID, weak tests, fallback-display versus zero, hidden unrelated errors, scope/minimality) is a blocker. APPROVE only if nothing is left to improve. Do not reject the opt-in missing-balance contract merely because its hook lives under confirmations; that exact contract and Perps consumption are explicitly approved by the human owner. Do flag any actual behavior change to existing non-opt-in callers.

Return exactly this structure:

VERDICT: APPROVE | REQUEST_CHANGES
COMMIT: 16cfc2e940b8247f81cce2e516d7fa4fbe9cdf74
BLOCKERS:
- <file:line> — <issue> — <fix>
NITS:
- <file:line> — <issue> — <fix>
EVIDENCE:
- <files/commands inspected>

Use `- None` for empty BLOCKERS or NITS. Any non-None entry requires REQUEST_CHANGES.
