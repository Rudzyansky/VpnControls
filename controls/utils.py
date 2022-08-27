import subprocess


def gen_password():
    return subprocess.run(['pwgen', '-s', '-1', '16', '1'], stdout=subprocess.PIPE, text=True).stdout


def from_hex(_str: str):
    return bytes.fromhex(_str).decode()


def to_hex(_str: str):
    return bytes.hex(_str.encode())
