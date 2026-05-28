## **Description**

Adds a feature-flagged Related markets rail to Perps market details so users can discover markets from the same configured Collection/List and navigate directly to another asset detail page. The rail defaults off behind `perpsRelatedMarketsMobile`, tracks related-market taps and horizontal slides, and keeps the destination screen-view source as `related_markets`.

Self-review follow-up centralized the new related-market analytics source, interaction type, and properties in the canonical perps event constants, replaced a hardcoded copy assertion with a testID assertion, and added the recipe coverage artifact referenced by the validation evidence. Human-review follow-up now reuses the existing perps homepage sparkline market card so the Related markets rail matches the home format with wider graph tiles.

## **Changelog**

CHANGELOG entry: Added a Related markets rail on Perps market details for easier market discovery

## **Related issues**

Fixes: https://consensyssoftware.atlassian.net/browse/TAT-3169

## **Manual testing steps**

```gherkin
Feature: Related markets on Perps market details

  Scenario: user opens a configured Perps market and navigates to a related market
    Given the perpsRelatedMarketsMobile feature flag is enabled
    And the wallet is unlocked with Perps available

    When the user opens FET market details
    Then the Related markets rail is visible with AI market tiles

    When the user taps TAO in the rail
    Then TAO market details opens with source related_markets
    And the destination page also shows a Related markets rail

  Scenario: user opens a market without a related collection
    Given the perpsRelatedMarketsMobile feature flag is enabled

    When the user opens BTC market details
    Then no Related markets rail is rendered
```

## **Screenshots/Recordings**

<table>
<tr><td align="center" width="50%"><strong>Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac1 Fet Chart Loaded</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/30728/recipe-runs/inherited-87648c6f-fd4a-4423-bd46-b2e4525528a1/after-ac1-fet-chart-loaded.png?sha=abe29b0e7d000fcc" alt="Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac1 Fet Chart Loaded" width="400" /></td><td align="center" width="50%"><strong>Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac1 Related Markets Visible</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/30728/recipe-runs/inherited-87648c6f-fd4a-4423-bd46-b2e4525528a1/after-ac1-related-markets-visible.png?sha=f2edd72b106ea5a3" alt="Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac1 Related Markets Visible" width="400" /></td></tr>
<tr><td align="center" width="50%"><strong>Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac3 Recursive Related Markets</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/30728/recipe-runs/inherited-87648c6f-fd4a-4423-bd46-b2e4525528a1/after-ac3-recursive-related-markets.png?sha=f400321b8cae385b" alt="Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac3 Recursive Related Markets" width="400" /></td><td align="center" width="50%"><strong>Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac4 Primary List Related Markets</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/30728/recipe-runs/inherited-87648c6f-fd4a-4423-bd46-b2e4525528a1/after-ac4-primary-list-related-markets.png?sha=03cf906007d5eecf" alt="Recipe Runs/inherited 87648c6f Fd4a 4423 Bd46 B2e4525528a1/after Ac4 Primary List Related Markets" width="400" /></td></tr>
</table>


**Video**
- After: [recipe-runs/inherited-87648c6f-fd4a-4423-bd46-b2e4525528a1/after.mp4](https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/30728/recipe-runs/inherited-87648c6f-fd4a-4423-bd46-b2e4525528a1/after.mp4?sha=d234e140fbccb022)

## **Validation Recipe**
<details><summary>recipe.json (22 steps - related markets rail visibility, navigation, primary list, and absence checks)</summary>

See `.task/feat/tat-3169-0528-090046/artifacts/recipe.json` for the executable recipe. The latest human-review rerun scrolls the related rail horizontally before AC1 and AC3 screenshots so the evidence shows loaded homepage-style sparkline cards.
</details>

## **Validation Logs**
Command:
```bash
bash scripts/perps/agentic/validate-recipe.sh .task/feat/tat-3169-0528-090046/artifacts/ --skip-manual
```

Latest rerun after human review: `validate-recipe-human-review.log` with 22/22 recipe nodes passing. The refreshed screenshots are:

- `after-ac1-related-markets-visible.png` - FET detail page with homepage-style Related markets sparkline cards.
- `after-ac1-fet-chart-loaded.png` - FET chart area loaded correctly.
- `after-ac3-recursive-related-markets.png` - TAO destination page with homepage-style Related markets sparkline cards.
- `after-ac4-primary-list-related-markets.png` - ONDO primary RWA rail with homepage-style Related markets sparkline cards.

Visual check: AC1, AC3, and AC4 rail screenshots show loaded sparklines and visible symbols/prices without collapsed text. The FET chart screenshot confirms the replacement market's chart renders correctly.

## **Pre-merge author checklist**

- [x] I've followed [MetaMask Contributor Docs](https://github.com/MetaMask/contributor-docs) and [MetaMask Mobile Coding Standards](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/CODING_GUIDELINES.md).
- [x] I've completed the PR template to the best of my ability
- [x] I've included tests if applicable
- [x] I've documented my code using [JSDoc](https://jsdoc.app/) format if applicable
- [x] I've applied the right labels on the PR (see [labeling guidelines](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/LABELING_GUIDELINES.md)). Not required for external contributors.

#### Performance checks (if applicable)

- [x] I've tested on Android
  - Ideally on a mid-range device; emulator is acceptable
- [x] I've tested with a power user scenario
  - Use these [power-user SRPs](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/edit-v2/401401446401?draftShareId=9d77e1e1-4bdc-4be1-9ebb-ccd916988d93) to import wallets with many accounts and tokens
- [x] I've instrumented key operations with Sentry traces for production performance metrics
  - See [`trace()`](/app/util/trace.ts) for usage and [`addToken`](/app/components/Views/AddAsset/components/AddCustomToken/AddCustomToken.tsx#L274) for an example

For performance guidelines and tooling, see the [Performance Guide](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/400085549067/Performance+Guide+for+Engineers).

## **Pre-merge reviewer checklist**

- [ ] I've manually tested the PR (e.g. pull and build branch, run the app, test code being changed).
- [ ] I confirm that this PR addresses all acceptance criteria described in the ticket it closes and includes the necessary testing evidence such as recordings and or screenshots.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Changes are behind a remote feature flag and limited to Perps UI, static collection config, and analytics; the dependency patch only extends event name constants in dist files.
> 
> **Overview**
> Adds a **Related markets** discovery rail on Perps **market details**, gated by remote flag `perpsRelatedMarketsMobile` (defaults off). When enabled, the screen loads the markets list if needed, maps the current symbol to a static thematic/sector collection via `getRelatedMarketsForMarket`, and renders a horizontal `PerpsRelatedMarkets` rail (other symbols in the collection, excluding the current market).
> 
> Tapping a tile navigates to that asset’s details with `source: related_markets` and emits `PERPS_UI_INTERACTION` for `related_market_clicked` (source/destination market, category, position) and a one-time `slide` on the rail. **Asset screen viewed** tracking now accepts a `resetKey` on `market.symbol` so views fire again when switching markets.
> 
> Analytics constants are added through a **yarn patch** on `@metamask/perps-controller` 6.3.0; docs and Mixpanel dictionary entries document the new properties. Includes selectors, locale string, and unit/integration tests for the flag, utilities, rail, and details view.
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit 7652c52637f45f3f7be9193ea1b16b9cac7c25b5. Bugbot is set up for automated code reviews on this repo. Configure [here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

