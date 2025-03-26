import logging.config
from typing import Dict, Any

from .env import LOG_LEVEL


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


class ErrorFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL)


# Logging
default_logger_config = {"handlers": ["stdout", "stderr"], "level": "INFO", "propagate": False}
console_logger_config = {"handlers": ["stdout", "stderr"], "level": "DEBUG", "propagate": False}
warnings_logger_config = {"handlers": ["stderr"], "level": "WARNING", "propagate": False}
errors_logger_config = {"handlers": ["stderr"], "level": "ERROR", "propagate": False}
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] %(name)s: %(message)s [%(threadName)s]",
        },
    },
    "filters": {
        "info": {
            "()": InfoFilter,
        },
        "error": {
            "()": ErrorFilter,
        },
    },
    "handlers": {
        "stdout": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
            "filters": ["info"],
        },
        "stderr": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": "ext://sys.stderr",
            "filters": ["error"],
        },
    },
    "loggers": {
        "root": default_logger_config.copy(),
        "telegram": default_logger_config.copy(),
        "urllib3": default_logger_config.copy(),
        "asyncio": warnings_logger_config.copy(),
        "httpx": errors_logger_config.copy(),
        "httpcore": errors_logger_config.copy(),
    },
}

LOGGING_LEVELS_TO_DEBUG = {
    1: ['root'],
    3: ['asyncio', 'httpx', 'httpcore', 'telegram', 'urllib3']
}

for level, logger_names in LOGGING_LEVELS_TO_DEBUG.items():
    if LOG_LEVEL >= level:
        for name in logger_names:
            LOGGING_CONFIG['loggers'][name]['level'] = 'DEBUG'


def apply_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
