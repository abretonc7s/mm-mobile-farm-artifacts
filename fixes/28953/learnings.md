# Learnings — TAT-2971

- **Investigation was fast, fix was straightforward.** Root cause (3-layer Sentry logging of AbortError) was clear from reading the catch blocks. The fix pattern (utility + guard) was obvious once the data flow was traced.
- **JSDoc ordering matters.** Inserting a new function between an existing JSDoc and its function silently orphans the doc. Self-review step caught this — always verify JSDoc attachment after insertions.
- **Video recording needs `sleep 5` after `kill -INT`.** First attempt produced corrupt moov atom with `sleep 2`. The simctl recorder needs more time to flush to disk. `sleep 5` + `wait $PID` is reliable.
- **Evidence screenshots land in `.agent/screenshots/`, not in the recipe artifacts dir.** The `validate-recipe.sh` runner saves screenshots to `.agent/screenshots/` with timestamps — must copy them to artifacts dir manually for the evidence manifest.
