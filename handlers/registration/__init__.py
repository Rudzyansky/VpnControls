from gettext import translation, NullTranslations

from localization import languages, localedir
from . import register_msg, invite_iq, accept_cq, decline_cq, revoke_cq, start_msg

modules = [register_msg,
           invite_iq,
           accept_cq,
           decline_cq,
           revoke_cq,
           start_msg]

translations: list[NullTranslations] = []

for language in languages:
    translations[language] = translation(__name__, localedir, [language], fallback=True)

__all__ = [
    'modules',
    'translations'
]
