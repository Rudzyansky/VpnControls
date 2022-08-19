from . import grantadmin, revokeadmin, registeruser, unregisteruser


def register(client):
    client.add_event_handler(grantadmin.handler)
    client.add_event_handler(revokeadmin.handler)

    [client.add_event_handler(handler) for handler in registeruser.handlers]
    client.add_event_handler(unregisteruser.handler)


__all__ = [
    'register'
]
