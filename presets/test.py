import sys
import os
import nodriver as nd
import traceback
from capcha_evasion import profiles as evasion
from common.browser import launch_browser_with_profile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def main():
    try:
        # for name, data in evasion.profiles.items():
          #  await launch_browser_with_profile(name, data)

        perfil = evasion.profiles.get("perfil_windows_EEUU")
        browser = await launch_browser_with_profile("perfil_windows_EEUU", perfil)

        # -------- PROXY -------- #
        ip_page = await browser.get("https://ip.oxylabs.io/")
        await browser.sleep(2)
        ip = await ip_page.evaluate("document.body.textContent.trim()")
        print(f">= IP Address: {ip}")
        # -------- PROXY -------- #

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()


if __name__ == "__main__":
    loop = nd.loop()  # Obtiene el event loop de nodriver

    try:
        loop.run_until_complete(main())  # Ejecuta `main()` de forma asíncrona
        loop.run_forever()  # Mantiene el event loop activo
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Cerrando el programa.")
    finally:
        loop.close()

