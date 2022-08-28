from . import acquire_msg
from . import username_cq, password_cq, delete_cq

modules = [
    acquire_msg,
    username_cq, password_cq, delete_cq
]

__all__ = [
    'modules'
]
