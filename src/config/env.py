from os import getenv
from pathlib import Path

from .base import PROJECT_DIR

DOMAIN = getenv('DOMAIN')
DATA_DIR = Path(getenv("DATA_DIR", PROJECT_DIR.joinpath('data'))).resolve()
TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
LOG_LEVEL = int(getenv('LOG_LEVEL', 0))
