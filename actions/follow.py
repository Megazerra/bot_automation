from locales.translation import lang
async def follow_user(driver, target_user):
    tab = await driver.get(f"https://www.instagram.com/{target_user}")
    tab.save_screenshot("banner.png")
    await tab.sleep(1)

    follow_button = await tab.find(lang.t('ig.actions.follow'))
    if follow_button:
        await follow_button.click()
        print(f"Following: {target_user}")
    else:
        source = await tab.evaluate("document.documentElement.outerHTML")
        with open('follow_error.html', 'w', encoding='utf-8') as file:
            file.write(source)
        print(f"Button Follow not found for: {target_user}")
    await tab.close()
