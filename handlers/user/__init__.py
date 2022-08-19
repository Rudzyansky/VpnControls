from . import acquirecredentials, resetpassword, changeusername


def register(client):
    client.add_event_handler(acquirecredentials.handler)

    client.add_event_handler(resetpassword.handler)
    client.add_event_handler(changeusername.handler)


__all__ = [
    'register'
]
