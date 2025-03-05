async def print_ip(browser):
    # -------- PROXY -------- #
    ip_page = await browser.get("https://ip.oxylabs.io/")
    await browser.sleep(2)
    ip = await ip_page.evaluate("document.body.textContent.trim()")
    print(f">= IP Address: {ip}")
    # -------- PROXY -------- #