import os
import pickle
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
    await driver.get("https://www.instagram.com")
    if os.path.exists(cookies_path):
        load_cookies(driver, cookies_path)
        await driver.get("https://www.instagram.com")  # Reload the page with cookies
    else:
        # Fill in the Facebook login form
        print("Finding the email and password input field")
        email = await driver.select("input[type=email]")
        passsword = await driver.select("input[type=pass]")
        email.send_keys(username)
        passsword.send_keys(password)
        login_ig = await driver.find(text="Iniciar sesión", best_match=True)
        if login_ig:
            email.send_keys(username)
            passsword.send_keys(password)
            await login_ig.mouse_click()

            await driver.sleep(2)
            print("Login form submitted")
        else:
            print("Facebook login fields not found")
        save_cookies(driver, cookies_path)


async def login_facebook(driver, username, password, cookies_path="cookies.pkl"):
    """Log in to Instagram using Facebook credentials."""
    tab = await driver.get("https://www.facebook.com/login.php?next=https%3A%2F%2Fwww.facebook.com%2Foidc%2F%3Fapp_id%3D124024574287414%26redirect_uri%3Dhttps%3A%2F%2Fwww.instagram.com%2Faccounts%2Fsignupviafb%2F%26response_type%3Dcode%26scope%3Dopenid%2Bemail%2Bprofile%2Blinking%26state%3DATBXRSuShMyQrdYrzpeTUEQCCkjoCUfK4n4DXNyEXUFqjR1vjW70TMCYNb8qMnyrbMlA5PyzYmismCuITOXsL6bRipLXQ8pa5RtV8_0aOcPiuQh4UYyH0VLbXb2_RuEluEmOkZzcVB6CsFxVE6Xx_fpWA_p5hBXAgEh_QmU71q2HdsQ-Ec4fCljsoFa_diIDjVFi7vS529B98f0Zp8-RRkI21hFO-Xv6JyCcmq4yxeDiSSboCCbkzVZdE244Z4Q1ZCGr")
    if os.path.exists(cookies_path):
        load_cookies(driver, cookies_path)
        tab = await driver.get("https://www.instagram.com")  # Reload the page with cookies
    else:
        # Accept Facebook cookies (if appears)
        decline_fb_cookies = await tab.find(lang.t('fb.cookies') , True)
        if decline_fb_cookies:
            await decline_fb_cookies.click()
        else:
            source = await tab.evaluate("document.documentElement.outerHTML")
            with open('fb_cookies.html', 'w', encoding='utf-8') as file:
                file.write(source)
            print("Facebook cookies accepts button not found")

        await tab.sleep(2)
        # Fill in the Facebook login form
        email = await tab.select(f"input[name={lang.t('fb.login.email')}]")
        passsword = await tab.select(f"input[name={lang.t('fb.login.password')}]")

        # Log in with Facebook
        login_fb = await tab.find(text=lang.t('fb.login.button'))
        if login_fb:
            await email.send_keys(username)
            await passsword.send_keys(password)
            await tab.sleep(12)
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
        tab.save_screenshot("from_login.png")

        # Save cookies after logging in
        # save_cookies(driver, cookies_path)


def logout(driver, cookies_path):
    """Log out from Instagram."""
    driver.get("https://www.instagram.com/accounts/logout/")
    if os.path.exists(cookies_path):
        os.remove(cookies_path)
    print("Logged out and cookies removed")
