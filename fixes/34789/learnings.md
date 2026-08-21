# Learnings

- A GitHub reply that cites a SHA is not proof the commit is on the PR branch. `45f48d0143f` was posted as the bugbot fix, then left dangling after later history, so the stale `insufficient_balance` row came back after rebase.
- `skipBalanceError` only affects the next validation write. After the first run, later flag flips are debounced, so the previous generic balance string stays in `errors` until that timer fires. Filter it out of the returned list as soon as the caller owns the message.
- Rebasing this hook onto main means keeping main's `protocolValid` / trigger-price shape and folding `skipBalanceError` into it. Do not take the older `isValid`-in-state version from the PR commit.
