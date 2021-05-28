import json
from pathlib import Path


def load(filepath: Path = Path(Path.home(), '.snappy', 'auth.json')) -> dict:
    with open(filepath, 'r') as auths_json:
        return json.load(auths_json)


def save(
    auths: dict,
    filepath: Path = Path(Path.home(), '.snappy', 'auth.json')
) -> None:
    with open(filepath, 'w') as auths_json:
        json.dump(auths, auths_json)


def token(auths: dict) -> str:
    return auths.get('auth', None)


def add(tkn: str) -> dict:
    return {'auth': tkn}


def rm() -> dict:
    return {'auth': ''}
