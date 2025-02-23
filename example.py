import asyncio
import random
import string
import logging
import nodriver as uc

logging.basicConfig(level=30)

months = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]

async def find_element(tab, texts, best_match=True):
    """Busca un elemento en la página con múltiples opciones de texto."""
    for text in texts:
        element = await tab.find(text, best_match=best_match)
        if element:
            return element
    return None  # Si no encuentra ninguno, retorna None


async def main():
    driver = await uc.start()

    tab = await driver.get("https://twitter.com")

    print('Finding the "create account" button')
    texts = ["create account", "crear cuenta"]
    create_account = await find_element(tab, texts)

    print('"Create account" => click')
    await create_account.click()

    print('Finding the "create account" button')
    texts = ["use email instead", "usar correo"]
    element = await find_element(tab, texts)
    await element.click()

    print("Finding the email input field")
    email = await tab.select("input[type=email]")

    if not email:
        use_mail_instead = await tab.find("use email instead")
        await use_mail_instead.click()
        email = await tab.select("input[type=email]")

    randstr = lambda k: "".join(random.choices(string.ascii_letters, k=k))

    print('Filling in the "email" input field')
    await email.send_keys("".join([randstr(8), "@", randstr(8), ".com"]))

    print("Finding the name input field")
    name = await tab.select("input[type=text]")

    print('Filling in the "name" input field')
    await name.send_keys(randstr(8))

    print('Finding the "month", "day" and "year" fields')
    sel_month, sel_day, sel_year = await tab.select_all("select")

    print('Filling in the "month" field')
    await sel_month.send_keys(months[random.randint(0, 11)].title())

    print('Filling in the "day" field')
    await sel_day.send_keys(str(random.randint(1, 28)))

    print('Filling in the "year" field')
    await sel_year.send_keys(str(random.randint(1980, 2005)))

    await tab.sleep(1)

    cookie_bar_accept = await tab.find("accept all", best_match=True)
    if cookie_bar_accept:
        await cookie_bar_accept.click()

    print("Clicking 'Next' button")
    next_btn = await tab.find(text="next", best_match=True)
    await next_btn.mouse_click()

    await tab.sleep(2)

    print('Finding "Next" button again')
    next_btn = await tab.find(text="next", best_match=True)
    await next_btn.mouse_click()

    await tab.select("[role=button]")

    print('Finding "Sign up" button')
    sign_up_btn = await tab.find("Sign up", best_match=True)
    await sign_up_btn.click()

    print('Waiting for verification step...')
    await tab.sleep(10)
    driver.stop()

if __name__ == '__main__':
    asyncio.run(main())
