import datetime

from localization.context import ContextProto


def contact_with_developer(context: ContextProto, **kwargs):
    if 'timestamp' not in kwargs.keys():
        kwargs['timestamp'] = datetime.datetime.now(datetime.timezone.utc)
    if 'chat_id' not in kwargs.keys():
        kwargs['chat_id'] = context.chat_id
    if 'user_id' not in kwargs.keys():
        kwargs['user_id'] = context.user_id

    data = {
        ' '.join('ID' if kk.lower() == 'id' else kk.capitalize() for kk in k.replace('_', ' ').split()): v
        for k, v in kwargs.items()
    }
    payload = '<b>Debug info</b>\n' + '\n'.join([f'<i>{k}</i> <code>{v}</code>' for k, v in data.items()])
    return context.localize('errors.contact_developer') + '\n\n' + payload
