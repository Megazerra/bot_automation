import sys
import os

import nodriver as nd

from common.browser import start_browser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import traceback
from actions.login import login_threads
from actions.follow import follow_user


async def main(username, password, target_user):
    try:
        browser = await start_browser()
        tab = await browser.get("https://deviceandbrowserinfo.com/info_device")
        # Iniciar sesión en Threads con Facebook
        # await login_threads(driver, username, password)
        # Seguir al usuario objetivo
        # await follow_user(driver, target_user)
        await tab.sleep(3000)
        # stop_driver(driver)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()


if __name__ == "__main__":
    # Validar que se pasen los argumentos correctos
    if len(sys.argv) != 4:
        print(f"Uso: python {sys.argv[0]} <login_method> <username> <password> <target_user>")
        sys.exit(1)

    user = sys.argv[1]
    passwd = sys.argv[2]
    target = sys.argv[3]

    nd.loop().run_until_complete(main(user, passwd, target))
