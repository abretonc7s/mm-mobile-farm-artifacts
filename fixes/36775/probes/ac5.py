import json,copy
T='temp/tasks/fix/36775-0924-221931'
DRAIN=f'bash {T}/artifacts/scripts/drain-btc-margin.sh'
SHEET='perps-adjust-margin-bottom-sheet'
def nav(p,what):
    return [
 (f'{p}-home',{"action":"ui.navigate","page":"home","intent":"Reset navigation so the market screen is the only margin entry point"}),
 (f'{p}-nav',{"action":"ui.navigate","page":"perps-market","market":"BTC","intent":"Open the BTC market holding the isolated position"}),
 (f'{p}-wait-margin-card',{"action":"ui.wait_for","test_id":"position-card-margin","expected":"present","timeout_ms":15000,"intent":"Make sure the position margin card is mounted before opening margin actions"}),
 (f'{p}-press-margin-card',{"action":"ui.press","test_id":"position-card-margin","intent":what})]
def ac4():
    c=nav('ac4-add','Open margin actions to give the position removable headroom')+[
 ('ac4-add-press-add',{"action":"ui.press","test_id":"perps-adjust-margin-add-btn","intent":"Choose Add Margin so the position has margin the form can offer"}),
 ('ac4-add-open-keypad',{"action":"ui.press","test_id":"perps-amount-display-touchable","intent":"Open the keypad to type the margin to add"}),
 ('ac4-add-key-2',{"action":"ui.press","test_id":"keypad-key-2","intent":"Type the tens digit of the $20 addition"}),
 ('ac4-add-key-0',{"action":"ui.press","test_id":"keypad-key-0","intent":"Type the units digit of the $20 addition"}),
 ('ac4-add-close-keypad',{"action":"ui.press","test_id":"perps-adjust-margin-done-button","intent":"Close the keypad to reach the confirm button"}),
 ('ac4-add-confirm',{"action":"ui.press","test_id":"perps-adjust-margin-confirm-button","intent":"Submit the $20 margin addition"}),
 ('ac4-add-assert-added',{"action":"ui.wait_for","text":"Added $20 margin","text_match":"contains","expected":"visible","timeout_ms":20000,"intent":"Confirm the exchange accepted the addition so removable headroom exists"}),
 ]+nav('ac4','Open the margin action choice on the full-screen variant')+[
 ('ac4-press-remove',{"action":"ui.press","test_id":"perps-adjust-margin-reduce-btn","intent":"Open the full-screen Remove Margin form"}),
 ('ac4-open-keypad',{"action":"ui.press","test_id":"perps-amount-display-touchable","intent":"Reveal the quick-amount buttons including Max"}),
 ('ac4-press-max',{"action":"ui.press","text":"Max","intent":"Keep a positive Max amount in the form before the limit drops"}),
 ('ac4-close-keypad',{"action":"ui.press","test_id":"perps-adjust-margin-done-button","intent":"Close the keypad so the retained amount is validated"}),
 ('ac4-assert-no-explanation',{"action":"ui.wait_for","test_id":"perps-adjust-margin-no-removable-margin","expected":"absent","timeout_ms":3000,"intent":"Confirm margin is still removable before the live limit drops"}),
 ('ac4-drain-live-limit',{"action":"command","cmd":DRAIN,"timeout_ms":60000,"intent":"Remove the position's spare margin outside the open form so its live limit falls to zero under the retained amount"}),
 ('ac4-assert-explanation',{"action":"ui.wait_for","test_id":"perps-adjust-margin-no-removable-margin","expected":"visible","timeout_ms":15000,"intent":"Require the zero-removable explanation once the live limit reaches zero"}),
 ('ac4-assert-no-stale-error',{"action":"ui.wait_for","text":"Amount exceeds maximum removable margin","text_match":"contains","expected":"absent","timeout_ms":3000,"intent":"Require no stale over-limit error on the retained amount next to the explanation"}),
 ('ac4-screenshot',{"action":"ui.screenshot","label":"AC4: full screen explains zero limit under retained amount","intent":"Show reviewers the full-screen form explains the zero limit instead of a stale error"})]
    return c
def ac5():
    return [
 ('ac5-pin-bottom-sheet',{"action":"metamask.feature_flags.set","flags":{"perpsTAT3938AbtestScreenVsBottomSheet":"treatment"},"intent":"Switch to the bottom-sheet margin flow the review finding is about"}),
 ]+nav('ac5-add','Open the margin bottom sheet to give the position removable headroom')+[
 ('ac5-add-open-keypad',{"action":"ui.press","test_id":"perps-amount-display-touchable","intent":"Open the keypad to type the margin to add"}),
 ('ac5-add-key-2',{"action":"ui.press","test_id":"keypad-key-2","intent":"Type the tens digit of the $20 addition"}),
 ('ac5-add-key-0',{"action":"ui.press","test_id":"keypad-key-0","intent":"Type the units digit of the $20 addition"}),
 ('ac5-add-close-keypad',{"action":"ui.press","test_id":f"{SHEET}-done-button","intent":"Close the keypad to reach the confirm button"}),
 ('ac5-add-confirm',{"action":"ui.press","test_id":f"{SHEET}-confirm-button","intent":"Submit the $20 margin addition from the bottom sheet"}),
 ('ac5-add-assert-added',{"action":"ui.wait_for","text":"Added $20 margin","text_match":"contains","expected":"visible","timeout_ms":20000,"intent":"Confirm the exchange accepted the addition so removable headroom exists"}),
 ]+nav('ac5','Open the margin bottom sheet on the position')+[
 ('ac5-press-remove-mode',{"action":"ui.press","test_id":f"{SHEET}-remove-mode","intent":"Switch the bottom sheet to Remove"}),
 ('ac5-open-keypad',{"action":"ui.press","test_id":"perps-amount-display-touchable","intent":"Reveal the quick-amount buttons including Max"}),
 ('ac5-press-max',{"action":"ui.press","text":"Max","intent":"Keep a positive Max amount in the sheet before the limit drops"}),
 ('ac5-close-keypad',{"action":"ui.press","test_id":f"{SHEET}-done-button","intent":"Close the keypad so the retained amount is validated"}),
 ('ac5-assert-no-explanation',{"action":"ui.wait_for","test_id":f"{SHEET}-no-removable-margin","expected":"absent","timeout_ms":3000,"intent":"Confirm margin is still removable before the live limit drops"}),
 ('ac5-drain-live-limit',{"action":"command","cmd":DRAIN,"timeout_ms":60000,"intent":"Remove the position's spare margin outside the open sheet so its live limit falls to zero under the retained amount"}),
 ('ac5-assert-explanation',{"action":"ui.wait_for","test_id":f"{SHEET}-no-removable-margin","expected":"visible","timeout_ms":15000,"intent":"Require the zero-removable explanation in the sheet once the live limit reaches zero"}),
 ('ac5-assert-no-stale-error',{"action":"ui.wait_for","test_id":f"{SHEET}-error","expected":"absent","timeout_ms":3000,"intent":"Require no stale error in the sheet in place of the explanation"}),
 ('ac5-screenshot',{"action":"ui.screenshot","label":"AC5: bottom sheet explains zero limit under retained amount","intent":"Show reviewers the bottom sheet explains the zero limit instead of a stale error"})]
def link(chain,last_next,nodes):
    for i,(k,v) in enumerate(chain):
        v['next']=chain[i+1][0] if i+1<len(chain) else last_next
        nodes[k]=v
