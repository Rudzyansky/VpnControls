from typing import Union, Match


def extract(match: Match, group: Union[int, str], default=None):
    result = match[group]
    return default if result is None else result
