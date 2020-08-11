from pathlib import Path

import requests
from toolz import pipe


def response_handler(r = requests.Response):
    r.raise_for_status()
    return r.json()


def _login_req(url: str, username: str, password: str):
    return requests.post(
        url,
        data = {
            'username': username,
            'password': password
        })


def _post_file_req(url: str, token: str, filepath: Path):
    return requests.post(
        url,
        files = {
            'file': (str(filepath), filepath.open('rb'))
        },
        headers = {
            'Authorization': f'Bearer {token}'
        }
    )


def token(url: str, username: str, password: str):
    return pipe(
        _login_req(url, username, password),
        response_handler,
        lambda r: r['access_token']
    )


def post_file(url: str, token: str, filepath: Path):
    return pipe(
        _post_file_req(url, token,filepath),
        response_handler
    )
