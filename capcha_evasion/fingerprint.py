import json
import nodriver as nd


def load_profiles(file_path):
    """Carga los perfiles desde un archivo JSON."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def start_browser(profile):
    return await nd.start(browser_args=['--headless=new', '--no-sandbox'])