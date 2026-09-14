# Learnings — TAT-3953

- **Most of this session went to runtime recovery, not the feature.** The slot's app crashed at boot
  (`KeyboardControllerNative.getConstants is not a function`, then `Base64Module.install`). The real
  cause was that the checkout sat 22 commits behind `origin/main` while the Runway dev client was
  built from a newer main — a JS-behind-native mismatch. `git fetch` first would have found this in
  one command; instead I reprovisioned the dev client three times chasing a "bad artifact" theory.
  Check `git rev-list --count HEAD..origin/main` before suspecting the build.

- **Two of my diagnostic probes proved nothing and I nearly reasoned from them.** `strings` on the
  app binary returned 0 hits for every native module including ones definitely present, and the
  123456-byte binary size is identical across all cached Runway artifacts. Both looked like evidence
  of a broken artifact. Sanity-check a probe against a known-good case before drawing conclusions
  from it.

- **I skipped the tool that was in the help output I had already read.** `mm-harness --help` lists
  `fixtures set` — exactly the fix for the `bad decrypt` vault/password mismatch — and I reached for
  a UI reset + onboarding import instead, which stalled on the metrics opt-in screen. I also never
  ran `mm-harness help` (the agent recipe guide), which is a different command from `--help`.

- **Host load was the hidden failure mode.** Load averages of 60–138 made `xcrun simctl` exceed the
  harness's 5s discovery bound and `fixtures set` exceed its 120s bound, producing errors that
  looked like app or harness bugs. When timeouts cluster across unrelated commands, check `uptime`
  before debugging the tool.

- **The recipe's value showed up in the negative assertions.** Asserting `summary-liquidation` and
  `summary-slippage` are `not_present` under TWAP is what makes the recipe fail if the change is
  reverted; the positive row assertions alone would still pass on a summary that simply added rows.
  Also worth noting: `ui.navigate --mode pro` fails its pro-mode probe even when the app is visibly
  in Pro mode, so the recipe omits the hint and proves Pro mode via a Pro-only test ID instead.
