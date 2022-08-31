def cool_message(title: str, data: dict) -> str:
    return f'**{title}**\n' + '\n'.join([f'__{k}__ `{v}`' for k, v in data.items()])


def debug_payload(**kwargs):
    return cool_message('Debug info', kwargs)


def contact_with_developer(_, **kwargs):
    return _('Something wrong. Contact with developer') + '\n\n' + debug_payload(**kwargs)


def contact_with_administrator(_, **kwargs):
    return _('An error has occurred. Please contact your administrator') + '\n\n' + debug_payload(**kwargs)


def gen_creds_message_text(username: str, password: str) -> str:
    return cool_message('IKEv2', {'Address': 'vpn.false.team', 'Username': username, 'Password': password})
