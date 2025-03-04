import os
import pickle
from common.totp_2fa import get_totp
from locales.translation import lang

def save_cookies(driver, path):
    pass
    """Save cookies to a file."""
    #with open(path, 'wb') as file:
     #   pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, path):
    """Load cookies from a file."""
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


async def login(driver, username, password, cookies_path="cookies.pkl"):
    """Log in to Instagram or load cookies if a session already exists."""
    tab = await driver.get("https://www.instagram.com")
    if os.path.exists(cookies_path):
        load_cookies(driver, cookies_path)
        await driver.get("https://www.instagram.com")  # Reload the page with cookies
    else:
        await lang.set_lang(tab)

        # Decline Instagram cookies (if appears)
        decline_ig_cookies = await tab.find(lang.t('ig.cookies'), True)
        if decline_ig_cookies:
            await decline_ig_cookies.click()
        else:
            source = await tab.evaluate("document.documentElement.outerHTML")
            with open('fb_cookies.html', 'w', encoding='utf-8') as file:
                file.write(source)
            print("Facebook cookies accepts button not found")

        # Find Instagram login form
        print("Finding the email and password input field")
        email = await tab.select(f"input[name={lang.t('ig.login.email')}]")
        passwd = await tab.select(f"input[name={lang.t('ig.login.password')}]")

        # Log in with Facebook
        login_ig = await tab.find(text=lang.t('ig.login.button'))
        if login_ig:
            await email.send_keys(username)
            await passwd.send_keys(password)
            await tab.sleep(1)
            await login_ig.mouse_click()
            print("Login form submitted")
        else:
            print("Login form not found")


        totp_ig = await tab.find(text=lang.t('ig.2fa.button'))
        # totp_ig = await tab.select("button[contains(text(),'confirm')]")
        if totp_ig:
            code_totp = get_totp()
            ig_2fa = await tab.select(f"input[name={lang.t('ig.2fa.input')}]")
            await ig_2fa.send_keys(code_totp)
            await totp_ig.click()
'''
        banner = await tab.find_all(lang.t('th.login.banner'))
        if banner:
            print("Banner found")
        else:
            print("Banner not found")
'''
        #save_cookies(driver, cookies_path)


async def login_facebook(driver, username, password, cookies_path="cookies.pkl"):
    """Log in to Instagram using Facebook credentials."""
    tab = await driver.get("https://www.facebook.com/login.php?next=https%3A%2F%2Fwww.facebook.com%2Foidc%2F%3Fapp_id%3D124024574287414%26redirect_uri%3Dhttps%3A%2F%2Fwww.instagram.com%2Faccounts%2Fsignupviafb%2F%26response_type%3Dcode%26scope%3Dopenid%2Bemail%2Bprofile%2Blinking%26state%3DATBXRSuShMyQrdYrzpeTUEQCCkjoCUfK4n4DXNyEXUFqjR1vjW70TMCYNb8qMnyrbMlA5PyzYmismCuITOXsL6bRipLXQ8pa5RtV8_0aOcPiuQh4UYyH0VLbXb2_RuEluEmOkZzcVB6CsFxVE6Xx_fpWA_p5hBXAgEh_QmU71q2HdsQ-Ec4fCljsoFa_diIDjVFi7vS529B98f0Zp8-RRkI21hFO-Xv6JyCcmq4yxeDiSSboCCbkzVZdE244Z4Q1ZCGr")
    if os.path.exists(cookies_path):
        load_cookies(driver, cookies_path)
        tab = await driver.get("https://www.instagram.com")  # Reload the page with cookies
    else:
        await lang.set_lang(tab)

        # Accept Facebook cookies (if appears)
        decline_fb_cookies = await tab.find(lang.t('fb.cookies') , True)
        if decline_fb_cookies:
            await decline_fb_cookies.click()
        else:
            source = await tab.evaluate("document.documentElement.outerHTML")
            with open('fb_cookies.html', 'w', encoding='utf-8') as file:
                file.write(source)
            print("Facebook cookies accepts button not found")

        # Fill in the Facebook login form
        email = await tab.select(f"input[name={lang.t('fb.login.email')}]")
        passwd = await tab.select(f"input[name={lang.t('fb.login.password')}]")

        # Log in with Facebook
        login_fb = await tab.find(text=lang.t('fb.login.button'))
        if login_fb:
            await email.send_keys(username)
            await passwd.send_keys(password)
            await tab.sleep(10)
            await login_fb.mouse_click()
            print("Login form submitted")
        else:
            source = await tab.evaluate("document.documentElement.outerHTML")
            with open('fb_form.html', 'w', encoding='utf-8') as file:
                file.write(source)
            print("Login form not found")
        banner = await tab.find_all(lang.t('ig.home.banner'))
        if banner:
            print("Banner found")
        else:
            print("Banner not found")
        # await tab.save_screenshot("from_login.png")

        # Save cookies after logging in
        # save_cookies(driver, cookies_path)


async def login_threads(driver, username, password):
    tab = await driver.get("https://www.threads.net/login/?show_choice_screen=false")
    await lang.set_lang(tab)

    th_cookies = await tab.find(lang.t("th.cookies"), True)
    if th_cookies:
        await th_cookies.click()
        print("Threads cookies declined")
    else:
        print("Threads cookies not found")
    th_login = await tab.find(f"//div[contains(text(),'{lang.t('th.login.button')}')]")
    if th_login:
        user = await tab.select(f"input[placeholder='{lang.t('th.login.username')}']")
        passwd = await tab.select(f"input[placeholder='{lang.t('th.login.password')}']")
        await user.send_keys(username)
        await passwd.send_keys(password)
        await tab.sleep(5)
        await th_login.click()

    th_login = await tab.find(username, True)
    # th_login = await tab.select(f"div[role={lang.t('th.login.role')}]")
    if th_login:
        await th_login.click()
        print("Login successfully completed")
    else:
        Exception(f"Could not login Threads")

    title_2fa = await tab.find(f"//div[.//span[contains(text(),  '{lang.t('th.2fa.title')}')]]")
    if title_2fa:
        totp_th = await tab.find(f"//div[contains(text(), '{lang.t('th.2fa.button')}')]")
        code_totp = get_totp()
        th_2fa = await tab.find(f"//input[@placeholder='{lang.t('th.2fa.input')}']")
        await th_2fa.send_keys(code_totp)
        await tab.sleep(5)
        await totp_th.click()


    # totp_ig = await tab.select("button[contains(text(),'confirm')]")

    banner = await tab.find_all(lang.t('ig.home.banner'))
    if banner:
        print("Banner found")
    else:
        print("Banner not found")

def logout(driver, cookies_path):
    """Log out from Instagram."""
    driver.get("https://www.instagram.com/accounts/logout/")
    if os.path.exists(cookies_path):
        os.remove(cookies_path)
    print("Logged out and cookies removed")
