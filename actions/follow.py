import sys

from nodriver import cdp
from locales.translation import lang
async def follow_user(browser, target_user):
    tab = browser.tabs[0]
    await tab.save_screenshot("6.5.png")
    await tab.send(cdp.page.navigate(url=f"https://www.threads.net/@{target_user}"))
    await tab.sleep(1)
    await tab.save_screenshot("7.png")

    follow_button = await tab.find(lang.t('common.actions.follow'))
    if follow_button:
        await follow_button.click()
    else:
        print(f"Follow button not found for: {target_user}", flush=True)

    following_button = await tab.find(lang.t('common.buttons.following'))
    if following_button:
        print(f"Following: {target_user}", flush=True)
    else:
        print(f"Following button not found for: {target_user}", flush=True)

    await tab.save_screenshot("8.png")
