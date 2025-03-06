import asyncio

from nodriver.cdp import fetch


class Oxylabs:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Oxylabs, cls).__new__(cls)
            cls._instance.USERNAME = "admin_QTwPt"
            cls._instance.PASSWORD = "9T6MkAVfKGknN_Y"
            cls._instance.ENDPOINT = "pr.oxylabs.io:7777"
            cls._instance.PROXY = f"https://{cls._instance.ENDPOINT}"
            cls._instance.SENTENCE = f"customer-{cls._instance.USERNAME}"
        return cls._instance  # Siempre retorna la misma instancia

    def set_location(self, country="", city=""):
        if country:
            self.SENTENCE += f"-cc-{country.upper()}"
            if city:
                self.SENTENCE += f"-city-{city.lower()}"

    async def setup_proxy(self, tab):
        async def auth_challenge_handler(event: fetch.AuthRequired):
            # Respond to the authentication challenge
            await tab.send(
                fetch.continue_with_auth(
                    request_id=event.request_id,
                    auth_challenge_response=fetch.AuthChallengeResponse(
                        response="ProvideCredentials",
                        username=self.SENTENCE,
                        password=self.PASSWORD,
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

        return tab

