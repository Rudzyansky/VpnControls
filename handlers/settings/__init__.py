from localization import load_translations

modules = []  # language

translations = load_translations(__name__)

__all__ = [
    'modules',
    'translations'
]
