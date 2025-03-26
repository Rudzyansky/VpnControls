from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from localization.context import ContextProto


def generate_text(context: ContextProto):
    return context.localize('settings.select_language')


def generate_buttons(context: ContextProto):
    languages = context.localize('settings.language')
    full = [InlineKeyboardButton(_name, callback_data=f'language {_code}') for _code, _name in languages.items()]
    buttons_matrix = [full[i:i + 2] for i in range(0, len(full), 2)]  # split by 2
    return InlineKeyboardMarkup(buttons_matrix)
