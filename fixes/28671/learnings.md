# Learnings — TAT-2057

- **cdpEvalAsync wraps expression in `Promise.resolve(<expr>)`** — `var` declarations are statements, not expressions, and silently fail inside `Promise.resolve()`. All eval_async recipe expressions must either be a single expression or wrapped in an IIFE `(function(){ ... })()`. This cost 3 debug rounds.

- **Rate limit arithmetic matters for parallel pagination** — 13 parallel `userFunding` calls at weight 20 each = 260 weight; UI's own 13 calls brings total to 520/min, safely under 1200/min. But calling the full 365-day range twice in quick succession in ac2 (26 total calls) hit the limit. Fix: use narrow 2-day window (1 call) for the consistency check in ac2.

- **git stash + same-file marker removal creates merge conflict on pop** — when the marker and fix are in the same file, `git stash pop` after committing the cleanup produces a merge conflict. Use Python to resolve by keeping the stash (fix) side. The TASK.md stash/commit/pop protocol works but the conflict resolution step is not documented.

- **Reproduce with the actual affected account** — the mm-4 slot account (437 records < 500 cap) doesn't trigger the bug. Switching to 0x316BDE (1174 records) provided a direct, quantitative proof via `count > 500` assertion. Always match the recipe's test account to the bug report's account.
