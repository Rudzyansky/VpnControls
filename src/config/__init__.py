from .base import *
from .env import *
from .logcfg import apply_logging

DB_PATH = DATA_DIR.joinpath('clients.db')
LANG_DIR = PROJECT_DIR.joinpath('lang')

SECRETS_PATTERN = '/etc/strongswan/users/ipsec.%s.secrets'

DATA_DIR.mkdir(parents=True, exist_ok=True)
