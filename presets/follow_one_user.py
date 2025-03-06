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
    try:
        perfil = evasion.profiles.get("perfil_windows_EEUU")
        browser = await launch_browser_with_profile("perfil_windows_EEUU", perfil)
        # Iniciar sesión en Threads
        await login_threads(browser, username, password)
        # Seguir al usuario objetivo
        #await follow_user(browser, target_user)

        # stop_driver(driver)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()

'''
if __name__ == "__main__":
    # Validar que se pasen los argumentos correctos
    if len(sys.argv) != 4:
        print(f"Uso: python {sys.argv[0]} <login_method> <username> <password> <target_user>")
        sys.exit(1)

    user = sys.argv[1]
    passwd = sys.argv[2]
    target = sys.argv[3]

    nd.loop().run_until_complete(main(user, passwd, target))
'''
if __name__ == "__main__":
    loop = uc.loop()  # Obtiene el event loop de nodriver

    try:
        if len(sys.argv) != 4:
            print(f"Uso: python {sys.argv[0]} <login_method> <username> <password> <target_user>")
            sys.exit(1)

        user = sys.argv[1]
        passwd = sys.argv[2]
        target = sys.argv[3]

        loop.run_until_complete(main(user, passwd, target))
        loop.run_forever()
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Cerrando el programa.")
    finally:
        loop.close()
