from telegram import BotCommand

from localization import Localization
from .categories import Categories

_commands: dict[str:dict[Categories:list[BotCommand]]] = dict()


# noinspection PyShadowingNames
def get(language: str, categories: set[Categories]) -> list[BotCommand]:
    commands = _commands[language]
    result = list()
    for c in Categories:
        if c in categories:
            result.extend(commands[c])
    return result


# Initialize commands for each language
for language in Localization._translations:
    __commands: dict[Categories:BotCommand] = dict()

    #
    # Accounts commands
    #

    __commands[Categories.CAN_CREATE_ACCOUNT] = [
        BotCommand('acquire', Localization.get_translation(language, 'commands.new_account')),
    ]

    __commands[Categories.HAS_ACCOUNTS] = [
        BotCommand('accounts', Localization.get_translation(language, 'commands.accounts_management')),
    ]

    #
    # Tokens commands
    #

    __commands[Categories.HAS_ACTUAL_TOKENS] = [
        BotCommand('invite', Localization.get_translation(language, 'commands.show_invitation_token')),
    ]

    __commands[Categories.CAN_ISSUE_TOKEN] = [
        BotCommand('issue', Localization.get_translation(language, 'commands.issue_token')),
    ]

    __commands[Categories.HAS_TOKENS] = [
        BotCommand('tokens', Localization.get_translation(language, 'commands.show_tokens')),
    ]

    #
    # Privileged commands
    #

    __commands[Categories.HAS_USERS] = [
        BotCommand('users', Localization.get_translation(language, 'commands.users_management')),
    ]

    #
    # Common commands
    #

    __commands[Categories.REGISTERED] = [
        BotCommand('language', Localization.get_translation(language, 'commands.change_language')),
        BotCommand('refresh', Localization.get_translation(language, 'commands.refresh_menu')),
    ]

    _commands[language] = __commands

__all__ = [
    'get'
]
