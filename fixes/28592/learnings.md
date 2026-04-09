# Learnings — TAT-2892

- **Context loss on session resume costs time.** The conversation was summarized mid-run (after step 21). Re-reading TASK.md and the git diff took ~5 tool calls before continuing. For long autonomous runs, writing a brief checkpoint note to the task artifacts dir would allow instant resume without re-reading everything.

- **`git stash pop` conflicts need care when marker and fix share a file.** The reproduction marker was in the same file (`PerpsConnectionManager.ts`) as the fix. `git stash pop` produced a merge conflict because the marker-cleanup commit removed the marker line while the stash still contained it. The correct fix: manually remove the conflict markers, keep only the fix code, then `git add` + `git stash drop`.

- **`git diff main...HEAD` vs `git diff HEAD` distinction matters for self-review.** The branch had substantial pre-existing commits, so `git diff main...HEAD` showed a large unrelated diff. For step 22 self-review, `git diff HEAD` (uncommitted changes only) was the correct scope.

- **`preserveCaches` threading is low-risk.** The fix required threading a new flag through 3 layers (`ensureConnected` → `performEnsureConnected` → `performActualDisconnection`). Because existing callers don't pass the flag, behavior is unchanged for all non-foreground-resume paths — a safe, additive change.

- **Before.mp4 moov atom failure**: first recording used `kill %1` which corrupted the moov atom. Always capture PID with `$!` immediately after `&`, and stop with `kill -INT $RECORDER_PID` — never `kill -TERM` or plain `kill`.
