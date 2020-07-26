from pathlib import Path

import requests


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
