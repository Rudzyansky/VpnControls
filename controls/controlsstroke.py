import re
import subprocess
from re import Pattern
from typing import AnyStr, IO, Optional

from controls import utils
from controls.controlsabstract import Controls
from controls.utils import from_hex, to_hex
from entities.account import Account


class StrokeControls(Controls):
    line_pattern: Pattern[AnyStr]
    filepath: str

    def __init__(self, filepath: str = '/etc/strongswan/users/ipsec.%s.secrets'):
        super().__init__()
        self.line_pattern = re.compile('"#(?P<username>[a-zA-Z0-9]+)" : EAP "0x(?P<password>[a-zA-Z0-9]+)"')
        self.filepath = filepath

    @classmethod
    def add_user(cls, user_id: int, username: str, password: str) -> Optional[int]:
        password = utils.gen_password()
        line = f'"#{to_hex(username)}" : EAP "0x{to_hex(password)}"\n'
        with open(cls.filepath % user_id, 'a') as f:
            position = f.tell()
            f.write(line)
        return position

    @classmethod
    def remove_user(cls, user_id: int, pos: int) -> int:
        with open(cls.filepath % user_id, 'r+', encoding='utf-8') as f:
            f.seek(pos)
            f.readline()  # skip current line
            start, end = pos, f.tell()
            tmp = f.read()
            f.seek(start)
            f.write(tmp)
            f.truncate()
        return end - start

    @classmethod
    def set_password(cls, user_id: int, pos: int, password: str) -> int:
        with open(cls.filepath % user_id, 'r+', encoding='utf-8') as f:
            start, end = get_password_pos(f, pos)
            replace_by_indexes(f, start, end, to_hex(password))
        return end - start

    @classmethod
    def set_username(cls, user_id: int, pos: int, username: str) -> int:
        with open(cls.filepath % user_id, 'r+', encoding='utf-8') as f:
            start, end = get_username_pos(f, pos)
            replace_by_indexes(f, start, end, to_hex(username))
        return end - start

    @classmethod
    def get_account(cls, user_id: int, pos: int) -> Optional[Account]:
        with open(cls.filepath % user_id, 'r+', encoding='utf-8') as f:
            f.seek(pos)
            matches = cls.line_pattern.match(f.readline())
        return Account(username=matches[0], password=matches[1], position=pos)

    @classmethod
    def get_accounts(cls, user_id: int, *positions: int) -> list[Account]:
        result: list[Account] = list()
        with open(cls.filepath % user_id, 'r+', encoding='utf-8') as f:
            for pos in positions:
                f.seek(pos)
                matches = cls.line_pattern.match(f.readline())
                result.append(Account(username=matches[0], password=matches[1], position=pos))
        return result

    @classmethod
    def change_hook(cls):
        subprocess.run(['strongswan', 'rereadsecrets'])


def find_quoted_str(line: str, start: int = None):
    q1 = line.find('"', start)
    q2 = line.find('"', q1 + 1)
    return q1 + 1, q2 - 1


def rfind_quoted_str(line: str, end: int = None):
    q2 = line.rfind('"', 0, end)
    q1 = line.rfind('"', 0, q2 - 1)
    return q1 + 1, q2 - 1


def get_username_pos(f: IO, pos: int):
    f.seek(pos)
    line = f.readline()
    q1 = line.find('"')
    q2 = line.find('"', q1 + 1)
    return pos + q1 + 2, pos + q2 - 1  # starts with '#'


def get_password_pos(f: IO, pos: int):
    f.seek(pos)
    line = f.readline()
    q2 = line.rfind('"')
    q1 = line.rfind('"', 0, q2 - 1)
    return pos + q1 + 3, pos + q2 - 1  # starts with '0x'


def replace_by_indexes(f: IO, start: int, end: int, data: AnyStr):
    f.seek(end)
    tmp = f.read()
    f.seek(start)
    f.write(data)
    f.write(tmp)
    f.truncate()


def find_by_username(f: IO, username: str):
    start = f.tell()
    for line in f:
        end = f.tell()
        q1, q2 = find_quoted_str(line)
        q3, q4 = find_quoted_str(line, q2 + 2)
        if from_hex(line[q1 + 1: q2]) == username:  # begin with '#'
            yield start, end, from_hex(line[q3 + 2: q4]), q3  # begin with '0x'
        start = end


controls: Controls = StrokeControls()
