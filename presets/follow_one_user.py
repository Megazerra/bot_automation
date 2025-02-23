import asyncio
import traceback
from common.instagram_utils import login_facebook
from actions.follow import follow_user
from common.web_driver import stop_driver, init_browser


async def main():
    try:
        driver = await init_browser()

        # Credenciales y usuario objetivo
        login_method = "facebook"
        username = "638306436"
        password = "ervadoHDTp@260601Jp*"  # **NUNCA compartas credenciales en código público**
        target_user = "rin_hayashi_"

        # Iniciar sesión en Threads con Facebook
        await login_facebook(driver, username, password)
        # Seguir al usuario objetivo
        await follow_user(driver, target_user)
        await driver.sleep(2)

        # stop_driver(driver)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

