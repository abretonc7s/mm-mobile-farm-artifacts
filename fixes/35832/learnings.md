# Learnings — PR-complete #35832

- No reviewer-driven learnings — no actionable comment fixes on this run.

- Rebase onto main hit a two-line conflict: main passed `lastViewedMarketSymbol` into `buildDefaultProMarket`, the PR wrapped the params object with `withHomeDroppedFromHistory`. Keep both. Dropping either undoes TAT-3786 (unstamped Home drop) or the last-viewed Pro market work on main.

- `metamask.wallet.ensure_unlocked` can fail the stability window on a freshly launched sim even when doctor shows Login/locked. Restart the app (`app.lifecycle restart`) and rerun before treating unlock as a product regression. The AC journey never started on the first attempt.

- Flaky-test comments get edited in place. A prior J9 reply does not cover later J4/J6/J3 findings on the same issue comment. Triage the live body, not the snapshot.
