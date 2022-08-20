from localization import load_translations

modules = []  # grant admin, revoke admin

translations = load_translations(__name__)

__all__ = [
    'modules',
    'translations'
]
