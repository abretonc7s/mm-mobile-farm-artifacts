### Scale warning fires mid-keystroke

**Low Severity**

<!-- DESCRIPTION START -->
The scale far-from-market gate treats a successful ladder as a finished price, but `hasScaleValidationInteraction` turns on in `onStartPriceChange` and `onEndPriceChange`. A partial start such as `8` still succeeds when end and order count are already filled, so the banner and `far_from_market_warning_shown` telemetry can fire while the user is still typing. The limit path avoids this with `hasBlurredLimitPrice`.
<!-- DESCRIPTION END -->

<!-- BUGBOT_BUG_ID: 5760633a-321c-4621-b21b-a8b2ccffbd3d -->

<!-- LOCATIONS START
app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.ts#L2957-L2967
LOCATIONS END -->
<div><a href="https://cursor.com/open?link=eyJ2ZXJzaW9uIjoxLCJ0eXBlIjoiQlVHQk9UX0ZJWF9JTl9DVVJTT1IiLCJkYXRhIjp7InJlZGlzS2V5IjoiYnVnYm90OmMxOWU4MzY2LTQzYTItNDUzYy1hY2ZhLWI3Y2IyMDAxZDc4MyIsImVuY3J5cHRpb25LZXkiOiJRVTFUWi1QQm1EOG9XWVh6TEpSbVdVelVlTkN4OTRTZnZpNFI0X1dQUlo4IiwiYnJhbmNoIjoiVEFULTM4OTctZmVhdC1hZGQtc2NhbGUtb3JkZXItcHJpY2Utd2FybmluZyIsInJlcG9Pd25lciI6Ik1ldGFNYXNrIiwicmVwb05hbWUiOiJtZXRhbWFzay1tb2JpbGUiLCJwcm92aWRlciI6ImdpdGh1YiJ9fQ" target="_blank" rel="noopener noreferrer"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/fix-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/fix-in-cursor-light.png"><img alt="Fix in Cursor" width="115" height="28" src="https://cursor.com/assets/images/fix-in-cursor-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/agents?link=eyJ2ZXJzaW9uIjoxLCJ0eXBlIjoiQlVHQk9UX0ZJWF9JTl9XRUIiLCJkYXRhIjp7InJlZGlzS2V5IjoiYnVnYm90OmMxOWU4MzY2LTQzYTItNDUzYy1hY2ZhLWI3Y2IyMDAxZDc4MyIsImVuY3J5cHRpb25LZXkiOiJRVTFUWi1QQm1EOG9XWVh6TEpSbVdVelVlTkN4OTRTZnZpNFI0X1dQUlo4IiwiYnJhbmNoIjoiVEFULTM4OTctZmVhdC1hZGQtc2NhbGUtb3JkZXItcHJpY2Utd2FybmluZyIsInJlcG9Pd25lciI6Ik1ldGFNYXNrIiwicmVwb05hbWUiOiJtZXRhbWFzay1tb2JpbGUiLCJwck51bWJlciI6MzU2NjYsImNvbW1pdFNoYSI6IjQ2YmQwODVkZWYwNDhjM2RkMDY3NjA2YjgzZWRhOTVmMWQwMjc1N2YiLCJwcm92aWRlciI6ImdpdGh1YiJ9fQ" target="_blank" rel="noopener noreferrer"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/fix-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/fix-in-web-light.png"><img alt="Fix in Web" width="99" height="28" src="https://cursor.com/assets/images/fix-in-web-dark.png"></picture></a></div>


<sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit 46bd085def048c3dd067606b83eda95f1d02757f. Configure [here](https://www.cursor.com/dashboard/bugbot).</sup>

