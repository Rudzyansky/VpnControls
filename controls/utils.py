import base64
import subprocess


def gen_password():
    return subprocess.run(['pwgen', '-s', '-1', '16', '1'], stdout=subprocess.PIPE, text=True).stdout


def decode_hex(_str: str):
    return bytes.fromhex(_str).decode()


def encode_hex(_str: str):
    return bytes.hex(_str.encode()).upper()


def decode_base64(_str: str):
    return base64.b64decode(_str.encode()).decode()


def encode_base64(_str: str):
    return base64.b64encode(_str.encode()).decode()
