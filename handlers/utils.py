from typing import Union


def extract(match, group: Union[int, str], default=None):
    try:
        return match[group]
    except IndexError:
        return default
