from pathlib import Path
from typing import Dict

import yaml

from config import LANG_DIR


class LocalizationManager:
    """Manages translations for the application"""

    def __init__(self, lang_dir: str | Path = LANG_DIR):
        self.lang_dir = Path(lang_dir)
        self._translations: Dict[str, Dict[str, str]] = {}
        self._load_translations()

    def _load_translations(self) -> None:
        """Load all translation files from the translations directory"""
        for lang_dir in self.lang_dir.iterdir():
            if not lang_dir.is_dir():
                continue

            lang = lang_dir.name
            self._translations[lang] = {}
            for yaml_file in lang_dir.rglob('*.yaml'):
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                prefix = f"{yaml_file.with_suffix('').relative_to(lang_dir)}.".replace('\\', '.').replace('/', '.')
                self._translations[lang].update({prefix + key: value for key, value in data.items()})

    def get_translation(self, language: str, key: str) -> str:
        """Get a translation for a specific language and key"""
        if language not in self._translations:
            language = 'en'  # Fallback to English
        return self._translations[language].get(key, key)

    def get_all_translations(self, key: str) -> Dict[str, str]:
        """Get translations for a key in all languages"""
        return {
            lang: self.get_translation(lang, key)
            for lang in self._translations
        }

    @property
    def available_languages(self):
        return list(self._translations.keys())


Localization = LocalizationManager()
Languages = Localization.available_languages
