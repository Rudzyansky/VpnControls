from localization import load_translations

modules = []  # create account, delete account, rename account, reset password

translations = load_translations(__name__)

__all__ = [
    'modules',
    'translations'
]
