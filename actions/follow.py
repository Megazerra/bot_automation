async def follow_user(driver, target_user):
    tab = await driver.get(f"https://www.instagram.com/{target_user}")

    follow_button = await tab.find("Seguir")
    if follow_button:
        await follow_button.click()
        print(f"Following: {target_user}")
    else:
        print(f"Button Follow not found for: {target_user}")
    await tab.close()
