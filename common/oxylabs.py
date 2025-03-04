import subprocess


def start_gost_proxy(proxy, rport):
    gost_proxy = f"socks5://{proxy.split('//')[1]}"
    gost_command = ["gost", "-L", f":{rport}", "-F", gost_proxy]
    subprocess.Popen(gost_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Started GOST proxy with {gost_proxy} on port {rport}")


class Oxylabs:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Oxylabs, cls).__new__(cls)
            cls._instance.USERNAME = "_csec_PSrd1"
            cls._instance.PASSWORD = "9T6MkAVfKGknN_Y"
            cls._instance.ENDPOINT = "pr.oxylabs.io:7777"
        return cls._instance  # Siempre retorna la misma instancia

    def get_proxy(self, country="", city="") -> dict:
        sentence = f"https://customer-{self.USERNAME}"
        if country:
            sentence += f"-cc-{country.lower()}"
            if city:
                sentence += f"-city-{city.lower()}"
        sentence += f":{self.PASSWORD}@{self.ENDPOINT}"

        wire_options = {
            "proxy": {
                "http": sentence.replace("https://", "http://"),
                "https": sentence,
                "ftp": sentence.replace("https://", "ftp://"),
            }
        }
        return wire_options

