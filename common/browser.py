import asyncio
import json
import platform
import nodriver as uc
from nodriver.cdp import fetch
from capcha_evasion.profiles import stealth_script
from common.oxylabs import Oxylabs, start_gost_proxy


def load_profiles(file_path):
    """Carga los perfiles desde un archivo JSON."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def start_browser():
    #return await nd.start(browser_args=['--headless=new', '--no-sandbox', '--disable-features=Translate', '--lang=en-US'])
    return await uc.start(browser_args=['--disable-features=Translate', '--lang=en-US'])



# --- 4. Función para iniciar navegador con un perfil dado ---
async def launch_browser_with_profile(profile_name, profile_data):
    """Lanza Chrome con el perfil especificado y realiza una navegación de prueba."""
    ua = profile_data["user_agent"]
    tz = profile_data["timezone"]
    geo = profile_data["geolocation"]
    accept_lang = profile_data.get("languages", "en-US,en")  # idioma por defecto si no especificado
    proxy = profile_data.get("proxy")

    # Configurar argumentos de Chrome (user-agent, idiomas, proxy, deshabilitar WebRTC local IP, etc.)
    args = [
        f"--user-agent={ua}",
        f"--lang={accept_lang}",
        "--disable-blink-features=AutomationControlled",  # Oculta indicios de automatización
        "--disable-gpu",  # (Opcional) evita usar GPU para estampar Canvas/WebGL, usa renderizado por software
        "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
        # WebRTC solo usará interfaz de red pública (no filtra IP local)
        "--disable-features=WebRtcHideLocalIpsWithMdns",  # Deshabilita mDNS (para que IP local no se filtre via WebRTC)
        "--disable-features=Translate",
        "--headless=new"
    ]
    if proxy:
        rport: int = 2000
        oxy = Oxylabs()
        cc = profile_data["languages"].split("-")[1].split(",")[0]
        city = profile_data["timezone"].split("/")[1]
        _proxy: dict = oxy.get_proxy(cc, city)
        start_gost_proxy(_proxy['proxy'].get('https'), rport)
        args.append(f"--proxy-server=socks5://localhost:{rport}")

    # Incluir path al ejecutable de Chrome si es necesario (según SO)
    chrome_path = None
    if platform.system().startswith("Windows"):
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    else:
        chrome_path = "/usr/bin/google-chrome"  # Suponer Chrome en PATH en Linux
    chrome_path = None

    # Iniciar navegador con nodriver usando la configuración dada
    browser = await uc.start(
        browser_executable_path=chrome_path if chrome_path else None,
        browser_args=args
    )

    # Abrir una nueva pestaña en blanco antes de navegar, para aplicar ajustes CDP
    tab = await browser.get("about:blank")

    # Configurar zona horaria y geolocalización usando DevTools (CDP) antes de cargar el sitio real
    from nodriver import cdp  # importar herramientas CDP de nodriver
    # Establecer timezone override
    await tab.send(cdp.emulation.set_timezone_override(timezone_id=tz))
    # Establecer geolocalización (lat, lon en grados, accuracy en metros)
    await tab.send(cdp.emulation.set_geolocation_override(
        latitude=geo["lat"], longitude=geo["lon"], accuracy=100
    ))
    # *Nota:* Por defecto Chrome no permite geolocalización sin permiso. Para tests,
    # se podría otorgar permiso automáticamente:
    # await browser._connection.send(cdp.browser.grant_permissions(permissions=["geolocation"], origin="https://sitio.com"))
    # (Esto asume acceso interno a conexión CDP; nodriver puede exponerlo de otra forma)

    # Inyectar el script stealth de fingerprint en todas las páginas nuevas
    await tab.send(cdp.page.add_script_to_evaluate_on_new_document(source=stealth_script))

    # Navegar a un sitio de prueba para verificar la huella (por ejemplo, whoer.net o amiunique.org)
    test_url = "https://httpbin.org/headers"  # httpbin devolverá cabeceras, incluyendo User-Agent, para ver cambios
    test_url = "https://deviceandbrowserinfo.com/info_device"
    await tab.send(cdp.page.navigate(url=test_url))

    # Esperar unos segundos para que la página cargue (en headless podría no ser necesario explícitamente)
    await tab.sleep(5)

    # Imprimir título de la página y URL final como verificación básica
    target = tab.target
    print(f"[{profile_name}] Título de la página: {target.title}")
    print(f"[{profile_name}] URL visitada: {target.url}")

    '''
    # Cerrar el navegador al terminar la sesión
    browser.stop()
    print(f"[{profile_name}] Sesión finalizada.\n")
    '''
    return browser


async def setup_proxy(username, password, tab):
    async def auth_challenge_handler(event: fetch.AuthRequired):
        # Respond to the authentication challenge
        await tab.send(
            fetch.continue_with_auth(
                request_id=event.request_id,
                auth_challenge_response=fetch.AuthChallengeResponse(
                    response="ProvideCredentials",
                    username=username,
                    password=password,
                ),
            )
        )

    async def req_paused(event: fetch.RequestPaused):
        # Continue with the request
        await tab.send(fetch.continue_request(request_id=event.request_id))

    # Add handlers for fetch events
    tab.add_handler(
        fetch.RequestPaused, lambda event: asyncio.create_task(req_paused(event))
    )
    tab.add_handler(
        fetch.AuthRequired,
        lambda event: asyncio.create_task(auth_challenge_handler(event)),
    )

    # Enable fetch domain with auth requests handling
    await tab.send(fetch.enable(handle_auth_requests=True))

