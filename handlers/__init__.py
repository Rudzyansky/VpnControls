from . import administration, user


def register(client):
    administration.register(client)
    user.register(client)


__all__ = [
    'register'
]
