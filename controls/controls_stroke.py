import re
import subprocess
from re import Pattern
from typing import AnyStr, IO, Optional

import env
from controls.controls_abstract import Controls
from controls.file_manipulator import FileManipulator
from controls.utils import to_hex, from_hex


class ControlsStroke(Controls, FileManipulator):
    line_pattern: Pattern[AnyStr]

    def __init__(self, file_pattern: str = env.SECRETS_PATTERN):
        super().__init__(file_pattern)
        self.line_pattern = re.compile(r'^"#([A-Z0-9]+)" : EAP "0x([A-Z0-9]+)"\n$', re.IGNORECASE)

    def add_user(self, user_id: int, username: str, password: str) -> Optional[int]:
        line = '"#%s" : EAP "0x%s"\n' % (to_hex(username), to_hex(password))
        with self.open(user_id, mode='ab') as f:
            return self.append(f, line)

    def remove_user(self, user_id: int, position: int) -> Optional[int]:
        with self.open(user_id) as f:
            return self.remove_line(f, position)

    def set_password(self, user_id: int, position: int, password: str) -> Optional[int]:
        with self.open(user_id) as f:
            _position, _count = self.get_password_pos(f, position)
            return self.replace_by_position(f, _position, _count, to_hex(password))

    def set_username(self, user_id: int, position: int, username: str) -> Optional[int]:
        with self.open(user_id) as f:
            _position, _count = self.get_username_pos(f, position)
            return self.replace_by_position(f, _position, _count, to_hex(username))

    def get_account(self, user_id: int, position: int) -> Optional[tuple[str, str]]:
        with self.open(user_id, mode='r') as f:
            f.seek(position)
            matches = self.line_pattern.match(f.readline())
            if matches:
                return from_hex(matches[1]), from_hex(matches[2])
            return None

    def get_accounts(self, user_id: int, *positions: int) -> list[tuple[str, str]]:
        result: list[tuple[str, str]] = list()
        with self.open(user_id, mode='r') as f:
            for position in positions:
                f.seek(position)
                matches = self.line_pattern.match(f.readline())
                result.append((from_hex(matches[1]), from_hex(matches[2])))
        return result

    @staticmethod
    def get_username_pos(f: IO, position: int):
        f.seek(position)
        line = f.readline().decode()
        start = line.find('"') + 2
        end = line.find('"', start)
        return position + start, end - start  # starts with '#'

    @staticmethod
    def get_password_pos(f: IO, position: int):
        f.seek(position)
        line = f.readline().decode()
        end = line.rfind('"')
        start = line.rfind('"', 0, end) + 3
        return position + start, end - start  # starts with '0x'

    @classmethod
    def change_hook(cls):
        subprocess.run(['strongswan', 'rereadsecrets'])


controls: Controls = ControlsStroke()
