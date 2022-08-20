from localization import load_translations

modules = [
    'register_msg',
    'invite_iq',
    'accept_cq',
    'decline_cq',
    'revoke_cq',
    'start_msg'
]

translations = load_translations(__name__)

__all__ = [
    'modules',
    'translations'
]
