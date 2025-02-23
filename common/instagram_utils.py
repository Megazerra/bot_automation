import os
import pickle


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
    tab = await driver.get("https://www.instagram.com")
    if os.path.exists(cookies_path):
        load_cookies(driver, cookies_path)
        tab = await driver.get("https://www.instagram.com")  # Reload the page with cookies
    else:
        # Accept Instagram cookies
        cookie_bar_accept = await tab.find("Permitir todas las cookies", best_match=True)
        if cookie_bar_accept:
            await cookie_bar_accept.click()
        else:
            print("Instagram cookies accepts button not found")

        # Log in with Facebook
        login_with_facebook = await tab.find_all("iniciar sesión con facebook")
        await tab.sleep(2)

        if login_with_facebook:
            await login_with_facebook[2].click()
        else:
            print("Facebook login button not found")
            return
        await tab.sleep(2)
        # Accept Facebook cookies (if appears)
        accept_fb_cookies = await tab.find_all("Permitir todas las cookies")
        if accept_fb_cookies:
            await accept_fb_cookies[3].click()
        else:
            print("Facebook cookies accepts button not found")

        await tab.sleep(2)
        # Fill in the Facebook login form
        print("Finding the email and password input field")
        email = await tab.select("input[name=email]")
        passsword = await tab.select("input[name=pass]")

        print("Clicking 'Log In' button")
        login_fb = await tab.find(text="Iniciar sesión")
        if login_fb:
            await email.send_keys(username)
            await passsword.send_keys(password)
            await tab.sleep(6)
            await login_fb.mouse_click()
            print("Login form submitted")
        else:
            print("Facebook login fields not found")

        await tab.find_all("Para ti")
        # Save cookies after logging in
        # save_cookies(driver, cookies_path)


def logout(driver, cookies_path):
    """Log out from Instagram."""
    driver.get("https://www.instagram.com/accounts/logout/")
    if os.path.exists(cookies_path):
        os.remove(cookies_path)
    print("Logged out and cookies removed")
