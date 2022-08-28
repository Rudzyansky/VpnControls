import asyncio
from io import SEEK_END
from typing import AnyStr, IO, Optional

_loop = asyncio.new_event_loop()


class FileManipulator:

    def __init__(self, file_pattern: str) -> None:
        self.file_pattern = file_pattern

    def open(self, *modifiers, mode='r+b'):
        return open(self.file_pattern % modifiers, mode)

    @staticmethod
    def append(f: IO, data: AnyStr) -> int:
        """
        :return: insertion position
        """
        if isinstance(data, str):
            data = data.encode()

        position = f.tell()
        f.write(data)
        return position

    @staticmethod
    def remove_line(f: IO, position: int) -> Optional[int]:
        """
        :return: count of removed bytes
        """
        if f.seek(0, SEEK_END) < position:
            return None

        f.seek(position)
        count = len(f.readline())  # skip current line
        tmp = f.read()
        f.seek(position)
        f.write(tmp)
        f.truncate()
        return count

    @staticmethod
    def replace_by_position(f: IO, position: int, count: int, data: AnyStr) -> Optional[int]:
        """
        :return: file size difference (new size - prev size)
        """
        if count < 0 or f.seek(0, SEEK_END) < position + count:
            return None

        if isinstance(data, str):
            data = data.encode()

        if len(data) == count:
            f.seek(position)
            f.write(data)
            return 0

        f.seek(position + count)
        tmp = f.read()
        f.truncate(position + len(data) + len(tmp))
        f.seek(position)
        f.write(data)
        f.write(tmp)
        return len(data) - count
