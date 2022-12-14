import os
from os import getenv

API_ID: int = int(getenv('API_ID', 0))
API_HASH: str = getenv('API_HASH')
TOKEN: str = getenv('TOKEN')
ADDRESS: str = getenv('ADDRESS')
SECRETS_PATTERN: str = getenv('SECRETS_PATTERN', 'users/ipsec.%s.secrets')
DB_PATH: str = getenv('DB_PATH', 'clients.db')
ROOT: str = os.path.dirname(os.path.abspath(__file__))
