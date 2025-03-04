import json
import sys
import os

if sys.platform == 'win32':
    base_path = "C:/Users/juanp/PycharmProjects/automation_bot_nodriver/locales/src"
else:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "/app/locales/src/"))

class Translation:
    def __init__(self):
        self.translations = None

    def load_lang(self, l):
        file_path = f"{base_path}/{l}.json"
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            self.translations = json.load(file)

    def t(self, key_path):
        """Recorre el diccionario usando una clave separada por puntos."""
        keys = key_path.split('.')
        value = self.translations
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            return f"Traducción no encontrada para: {key_path}"

    async def set_lang(self, tab):
        # Chrome Language detection
        language = await tab.evaluate("navigator.language")
        print(f"Idioma detectado: {language}")
        tab_lang = language.split("-")[0]
        if tab_lang != 'es' and tab_lang != 'en':
            Exception(f"Language {language} is not supported")
        else:
            self.load_lang(tab_lang)


lang = Translation()
