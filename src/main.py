#!/usr/bin/env python3
# encoding=utf-8
import logging

import config
import domain
import handlers
from db import Repository
from domain.common import application


def main():
    config.apply_logging()

    Repository.create_tables()
    domain.common.load_languages_cache()
    domain.commands.init()

    # Register handlers
    handlers.register(application)

    logging.info('Ready')

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
