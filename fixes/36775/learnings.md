# Learnings

- Round 2: the independent review caught another zero-transition gap. Removing `onPress` stops *new* focus but leaves an already-open keypad active. When a control is disabled by live data, test the transition from the "open/editing" state, not just the resting state.
- The live proof for that needs the keypad open *at* the moment the limit drops: set and validate the retained amount first, reopen the keypad, then mutate from outside. A negative control (effect removed, app restarted) failed at exactly that assert, which shows the node discriminates.
- Never commit or touch git while `mm-harness run` is active: the runner fingerprints product status and invalidates the evidence.
- After `yarn install` changes the tree, Metro can keep a stale file map ("exports ... file does not exist" for a file that is on disk). `launch --verify` alone and app restarts don't fix it; the one-time `--clear-metro` retry does. Follow it with `app.lifecycle restart` + doctor before a run.
- Under heavy machine load (other slots), setup nodes can hit CDP timeouts that clear within minutes; probe with a trivial bridge eval before retrying rather than rebuilding.
- The PR sits at 998/1000 counted lines; any further change must be net-neutral or trim tests.

Round 1:
- Display-priority bugs between errors and explanations need tests that move between states. Mocks that hold one limit steady can hide the transition under test.
- The inherited family `recipe.json` had drifted from the PR-body recipe; diff before re-validating (it drifted again for round 2, so promote the last passing recipe explicitly).
