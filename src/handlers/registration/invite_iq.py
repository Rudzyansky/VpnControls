import re

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import InlineQueryHandler

import domain
from entities.token import Token
from handlers.filters import can_invite
from localization import LocalizedContext, Languages

pattern_handler = re.compile(r'^invite$')
pattern_handler_space = re.compile(r'^invite/$')
pattern_handler_lang = re.compile(r'^invite/([a-z]{2})$')
pattern_handler_token = re.compile(r'^invite/([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})$')
pattern_handler_token_space = re.compile(r'^invite/([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})/$')
pattern_handler_token_lang = re.compile(r'^invite/([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})/([a-z]{2})$')


async def handler(update: Update, context: LocalizedContext):
    if not can_invite.filter(update):
        return
    current_tokens = domain.registration.get_current_tokens(update.effective_user.id)
    articles = []
    lang = domain.common.language(update.effective_user.id)
    articles += [await invite_article(context, token, lang) for token in current_tokens]
    await update.inline_query.answer(articles)


async def handler_space(update: Update, context: LocalizedContext):
    if not can_invite.filter(update):
        return
    current_tokens = domain.registration.get_current_tokens(update.effective_user.id)
    articles = []
    for lang in Languages:
        articles += [await invite_article(context, token, lang) for token in current_tokens]
    await update.inline_query.answer(articles)


async def handler_lang(update: Update, context: LocalizedContext):
    if not can_invite.filter(update):
        return
    lang = context.match.group(1)
    if lang not in Languages:
        await update.inline_query.answer([])
        return
    current_tokens = domain.registration.get_current_tokens(update.effective_user.id)
    articles = [await invite_article(context, token, lang) for token in current_tokens]
    await update.inline_query.answer(articles)


async def handler_token(update: Update, context: LocalizedContext):
    if not can_invite.filter(update):
        return
    token_id = context.match.group(1)
    token = domain.registration.fetch_token(Token(token_id, owner_id=update.effective_user.id))
    if token is None:
        await update.inline_query.answer([])
    else:
        lang = domain.common.language(update.effective_user.id)
        await update.inline_query.answer([await invite_article(context, token, lang)])


async def handler_token_space(update: Update, context: LocalizedContext):
    if not can_invite.filter(update):
        return
    token_id = context.match.group(1)
    token = domain.registration.fetch_token(Token(token_id, owner_id=update.effective_user.id))
    if token is None:
        await update.inline_query.answer([])
    else:
        await update.inline_query.answer([
            await invite_article(context, token, lang)
            for lang in Languages
        ])


async def handler_token_lang(update: Update, context: LocalizedContext):
    if not can_invite.filter(update):
        return
    token_id, lang = context.match.group(1), context.match.group(2)
    token = domain.registration.fetch_token(Token(token_id, owner_id=update.effective_user.id))
    if token is None:
        await update.inline_query.answer([])
    else:
        if lang in Languages:
            await update.inline_query.answer([await invite_article(context, token, lang)])
        else:
            await update.inline_query.answer([])


async def invite_article(context: LocalizedContext, token: Token, lang: str):
    if token.used_by is None:
        description = ''
    else:
        user = await context.bot.get_chat(token.used_by)
        display_name = user.first_name
        if user.last_name:
            display_name += f" {user.last_name}"
        description = (context.localize('registration.bound_to', lang) % display_name) + ', '
    description += (context.localize('registration.expires_in', lang) % token.expire) + '\n' + token.string

    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton(context.localize('registration.accept_invite', lang),
                             callback_data=f'accept {token.string} {lang}'),
        InlineKeyboardButton(context.localize('registration.decline_invite', lang),
                             callback_data=f'decline {token.string} {lang}')
    ]])

    return InlineQueryResultArticle(
        id=token.string,
        title=context.localize('registration.invite', lang),
        description=description,
        thumbnail_url='https://false.team/invite128.png',
        input_message_content=InputTextMessageContent(
            message_text=context.localize('registration.invite_message', lang),
        ),
        reply_markup=buttons,
    )


def get_handlers():
    return [
        InlineQueryHandler(handler, pattern_handler),
        InlineQueryHandler(handler_space, pattern_handler_space),
        InlineQueryHandler(handler_lang, pattern_handler_lang),
        InlineQueryHandler(handler_token, pattern_handler_token),
        InlineQueryHandler(handler_token_space, pattern_handler_token_space),
        InlineQueryHandler(handler_token_lang, pattern_handler_token_lang),
    ]
