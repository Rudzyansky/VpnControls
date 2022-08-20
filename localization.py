from gettext import translation, NullTranslations

localedir = 'lang'
languages = ['en', 'ru']


def load_translations(domain: str) -> dict[str:NullTranslations]:
    return {i: translation(domain, localedir, [i], fallback=True) for i in languages}
