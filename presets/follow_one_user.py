import sys
import os
import nodriver as uc
from capcha_evasion import profiles as evasion
from common.browser import launch_browser_with_profile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import traceback
from actions.login import login_threads
from actions.follow import follow_user


async def main(username, password, target_user):
    browser = None
    try:
        print("Empezando", flush=True)

        perfil = evasion.profiles.get("perfil_windows_EEUU")
        browser = await launch_browser_with_profile("perfil_windows_EEUU", perfil)
        print("Perfil seleccionado", flush=True)

        # Iniciar sesión en Threads
        await login_threads(browser, username, password)

        # Seguir al usuario objetivo
        await browser.tabs[0].save_screenshot("6.png")
        await browser.sleep(5)
        await follow_user(browser, target_user)

        print("Proceso completado con éxito", flush=True)

    except Exception as e:
        print("Error:", e, flush=True)
        traceback.print_exc()

    finally:
        sys.exit(0)


if __name__ == "__main__":
    loop = uc.loop()
    try:
        if len(sys.argv) != 4:
            print(f"Uso: python {sys.argv[0]} <username> <password> <target_user>")
            sys.exit(1)

        user = sys.argv[1]
        passwd = sys.argv[2]
        target = sys.argv[3]

        loop.run_until_complete(main(user, passwd, target))
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Cerrando el programa.")
    finally:
        loop.close()