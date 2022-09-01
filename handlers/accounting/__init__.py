from . import acquire_msg, accounts_msg
from . import username_cq, password_cq, delete_cq

modules = [
    acquire_msg, accounts_msg,
    username_cq, password_cq, delete_cq
]

__all__ = [
    'modules'
]
