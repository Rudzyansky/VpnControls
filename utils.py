def cool_message(title: str, data: dict) -> str:
    return f'**{title}**\n' + '\n'.join([f'__{k}__ `{v}`' for k, v in data.items()])


def debug_payload(**kwargs):
    return cool_message('Debug info', kwargs)


def gen_creds_message_text(username: str, password: str) -> str:
    return cool_message('IKEv2', {'Address': 'vpn.false.team', 'Username': username, 'Password': password})
