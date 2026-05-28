# TAT-3169 Recipe Coverage

## Acceptance Criteria Coverage

| AC | Proof mode | Recipe nodes | Evidence |
| --- | --- | --- | --- |
| AC1: Related markets rail appears on an AI market detail page | mixed | `ac1-open-ai-market`, `ac1-wait-related-rail`, `ac1-screenshot-related-rail` | `after-ac1-related-markets-visible.png` |
| AC2: Related-market tap opens the destination with `source=related_markets` | state | `ac2-press-related-market`, `ac2-assert-route-source` | Route-state assertion in recipe log |
| AC3: Destination market page also shows related markets | mixed | `ac3-wait-recursive-rail`, `ac3-screenshot-recursive-rail` | `after-ac3-recursive-related-markets.png` |
| AC4: Markets in multiple lists use one primary list | mixed | `ac4-open-multi-list-market`, `ac4-assert-single-primary-list`, `ac4-screenshot-primary-list` | `after-ac4-primary-list-related-markets.png` |
| AC5: Unlisted BTC does not render the rail | state | `ac5-open-unlisted-market`, `ac5-assert-no-rail` | Absence assertion in recipe log |

## Visual Evidence Policy

AC1, AC3, and AC4 use screenshots because they assert visible rail content. AC2 and AC5 use state assertions because navigation source and absence are more reliably proven from route/fiber state than from a static screenshot.
