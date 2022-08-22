from telethon.tl.types import BotCommand

from localization import get_translations

translations = get_translations(__package__)

commands_user: dict[str:list[BotCommand]] = {}
commands_admin: dict[str:list[BotCommand]] = {}

for language, translation in translations.items():
    _ = translation.gettext

    _commands_user = [
        BotCommand('accounts', _('Accounts management')),
        BotCommand('acquire', _('New account')),
        # BotCommand('change', _('Change username')),
        # BotCommand('reset', _('Reset password')),
        BotCommand('lang', _('Change language')),
        BotCommand('refresh', _('Refresh menu')),  # todo установка команд происходит на устройства в онлайне!!!
    ]

    _commands_admin = _commands_user + [
        BotCommand('invite', _('Show token, issue if not exist')),
        BotCommand('register', _('Issue new invitation token')),
        BotCommand('tokens', _('Show all invitation tokens')),
        BotCommand('remove', _('Remove user (all invited users assign with admin top level)')),
        BotCommand('grant', _('Grant admin privileges')),
        BotCommand('revoke', _('Revoke admin and remove all invited users')),
    ]

    commands_user[language] = _commands_user
    commands_admin[language] = _commands_admin
