import re
from re import Pattern
from typing import AnyStr, IO

from controls import utils
from controls.controlsabstract import Controls
from controls.utils import from_hex, to_hex


class StrokeControls(Controls):
    line_pattern: Pattern[AnyStr]
    filepath: str

    def __init__(self, filepath: str = '/etc/strongswan/ipsec.secrets'):
        super().__init__()
        self.line_pattern = re.compile('"#(?P<username>[a-zA-Z0-9]+)" : EAP "0x(?P<password>[a-zA-Z0-9]+)"')
        self.filepath = filepath

    @classmethod
    def add_user(cls, username: str):
        password = utils.gen_password()
        line = f'"#{to_hex(username)}" : EAP "0x{to_hex(password)}"\n'
        with open(cls.filepath, 'a') as f:
            start, = next(find_by_username(f, username), (None,))
            if start is not None:
                return False
            f.write(line)

    @classmethod
    def remove_user(cls, username: str):
        with open(cls.filepath, 'r+', encoding='utf-8') as f:
            start, end, = next(find_by_username(f, username), (None, None,))
            if start is not None and end is not None:
                f.seek(end)
                data = f.read()
                f.seek(start)
                f.write(data)
                f.truncate()

    @classmethod
    def reset_password(cls, username: str):
        password = to_hex(utils.gen_password())
        with open(cls.filepath, 'r+', encoding='utf-8') as f:
            start, end, _pw, index = next(find_by_username(f, username), (None, None, None, None))
            if start is not None and end is not None:
                f.seek(start + index + 2)
                f.write(password)

    @classmethod
    def change_username(cls, username: str, new_username: str):
        with open(cls.filepath, 'r+', encoding='utf-8') as f:
            start, = next(find_by_username(f, new_username), (None,))
            if start is not None:
                return False
            start, end, = next(find_by_username(f, username), (None, None))
            if start is None:
                return False


def find_quoted_str(line: str, start: int = 0):
    q1 = line.find('"', start)
    q2 = line.find('"', q1 + 1)
    return q1 + 1, q2 - 1


def find_by_username(f: IO, username: str):
    start = f.tell()
    for line in f:
        end = f.tell()
        q1, q2 = find_quoted_str(line)
        q3, q4 = find_quoted_str(line, q2 + 2)
        if from_hex(line[q1 + 1: q2]) == username:  # begin with '#'
            yield start, end, from_hex(line[q3 + 2: q4]), q3  # begin with '0x'
        start = end
