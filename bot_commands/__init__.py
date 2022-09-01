from telethon.tl.types import BotCommand

from localization import get_translations
from .categories import Categories

_translations = get_translations(__package__)

_commands: dict[str:dict[Categories:list[BotCommand]]] = dict()


# noinspection PyShadowingNames
def get(language: str, categories: set[Categories]) -> list[BotCommand]:
    commands = _commands[language]
    result = list()
    for c in Categories:
        if c in categories:
            result.extend(commands[c])
    return result


for _language, _translation in _translations.items():
    _ = _translation.gettext

    __commands: dict[Categories:BotCommand] = dict()

    #
    # Accounts commands
    #

    __commands[Categories.CAN_CREATE_ACCOUNT] = [
        BotCommand('acquire', _('New account')),
    ]

    __commands[Categories.HAS_ACCOUNTS] = [
        BotCommand('accounts', _('Accounts management')),
    ]

    #
    # Tokens commands
    #

    __commands[Categories.HAS_ACTUAL_TOKENS] = [
        BotCommand('invite', _('Show actual invitation token')),
    ]

    __commands[Categories.CAN_ISSUE_TOKEN] = [
        BotCommand('issue', _('Issue new invitation token')),
    ]

    __commands[Categories.HAS_TOKENS] = [
        BotCommand('tokens', _('Show all invitation tokens')),
    ]

    #
    # Privileged commands
    #

    __commands[Categories.HAS_USERS] = [
        BotCommand('users', _('Users management')),
    ]

    #
    # Common commands
    #

    __commands[Categories.REGISTERED] = [
        BotCommand('language', _('Change language')),
        BotCommand('refresh', _('Refresh menu')),
    ]

    _commands[_language] = __commands

__all__ = [
    'get'
]
