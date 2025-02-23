import json
import os

# base_path = "C:/Users/juanp/PycharmProjects/automation_bot_nodriver/locales/src/"
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "/app/locales/src/"))

class Translation:
    def __init__(self):
        self.translations = None

    def set_lang(self, l):
        file_path = f"{base_path}/{l}.json"
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


lang = Translation()
lang.set_lang('en')
