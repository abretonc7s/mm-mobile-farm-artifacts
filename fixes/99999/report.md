## Fix Summary

Fixed the crash in `PerpsMarketDetails` component when market data is undefined.

### Root Cause
The component was accessing `market.price` without null-checking `market`, causing a TypeError on initial render.

### Changes
- Added null guard in `PerpsMarketDetails.tsx:42`
- Added fallback UI for loading state

### Testing
- Verified fix with CDP automation
- Confirmed no regression on existing markets
