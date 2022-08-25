from telethon.tl.types import BotCommand

from localization import get_translations
from .categories import Categories

_translations = get_translations(__package__)

_commands: dict[str:dict[Categories:list[BotCommand]]] = dict()


# noinspection PyShadowingNames
def get(language: str, *categories: Categories):
    commands = _commands[language]
    result = list()
    for c in Categories:
        if c in categories:
            result += commands[c]
    return result


for _language, _translation in _translations.items():
    _ = _translation.gettext

    __commands: dict[Categories:BotCommand] = dict()

    #
    # User commands
    #

    __commands[Categories.NO_ACCOUNTS] = [
        BotCommand('acquire', _('New account')),
    ]

    __commands[Categories.ONE_ACCOUNT] = [
        BotCommand('change', _('Change username')),
        BotCommand('reset', _('Reset password')),
    ]

    __commands[Categories.MANY_ACCOUNTS] = [
        BotCommand('accounts', _('Accounts management')),
    ]

    #
    # Administration commands
    #

    __commands[Categories.NO_TOKENS] = [
        BotCommand('invite', _('Issue token')),
    ]

    __commands[Categories.HAS_ACTUAL_TOKENS] = [
        BotCommand('invite', _('Show actual token')),
    ]

    __commands[Categories.CAN_ISSUE_TOKEN] = [
        BotCommand('register', _('Issue new invitation token')),
    ]

    __commands[Categories.HAS_TOKENS] = [
        BotCommand('tokens', _('Show all invitation tokens')),
    ]

    __commands[Categories.HAS_SLAVES] = [
        BotCommand('remove', _('Remove user (all invited users assign with admin top level)')),
    ]

    __commands[Categories.GRANT] = [
        BotCommand('grant', _('Grant admin privileges')),
    ]

    __commands[Categories.HAS_INVITED] = [
        BotCommand('revoke', _('Revoke admin and remove all invited users')),
    ]

    #
    # Common commands
    #

    __commands[Categories.COMMON] = [
        BotCommand('language', _('Change language')),
        BotCommand('refresh', _('Refresh menu')),
    ]

    _commands[_language] = __commands

__all__ = [
    'get'
]
