import json
from pathlib import Path


def load(filepath: Path = Path(Path.home(), '.snappy', 'auth.json')):
    with open(filepath, 'r') as auths_json:
        return json.load(auths_json)


def save(
    auths: dict, 
    filepath: Path = Path(Path.home(), '.snappy', 'auth.json'
)):
    with open(filepath, 'w') as auths_json:
        json.dump(auths, auths_json)


def token(auths: dict):
    return auths.get('auth', None)


def add(token: str):
    return {'auth': token}


def rm():
    return {'auth': ''}
