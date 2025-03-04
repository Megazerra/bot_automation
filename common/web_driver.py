import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.browser import start_browser


async def init_browser():
    try:
        #profiles = load_profiles("../common/profiles.json")
        #profile = profiles[1]
        #print("Iniciando navegador con el perfil:", profile["name"])
        return await start_browser(None)
    except Exception as e:
        print(f"Error in init_headless: {e}")
        return None


def stop_driver(driver):
    if driver:
        driver.quit()
