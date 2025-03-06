from nodriver import cdp
from locales.translation import lang
async def follow_user(browser, target_user):
    tab = browser.tabs[0]
    await tab.send(cdp.page.navigate(url=f"https://www.threads.net/@{target_user}"))
    await tab.sleep(1)

    follow_button = await tab.find(lang.t('common.actions.follow'))
    if follow_button:
        await follow_button.click()
    else:
        source = await tab.evaluate("document.documentElement.outerHTML")
        with open('follow_error.html', 'w', encoding='utf-8') as file:
            file.write(source)
        print(f"Follow button not found for: {target_user}")

    following_button = await tab.find(lang.t('common.buttons.following'))
    if following_button:
        print(f"Following: {target_user}")
    else:
        print(f"Following button not found for: {target_user}")

    await tab.close()
