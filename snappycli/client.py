from pathlib import Path
import asyncio

from toolz import pipe
import requests
import httpx


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


def _post_file_req(url: str, token: str, filepath: Path, filedir: str):
    return requests.post(
        url = url,
        files = {
            'file': (str(filepath), filepath.open('rb'))
        },
        headers = {
            'Authorization': f'Bearer {token}'
        },
        params = {"filedir": filedir}
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
        response_handler,
        lambda r: r['loc']
    )


async def async_post_file_req(
    url: str, token: str, filepath: Path, filedir: str = ''):    
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(write=None, read=None, 
            connect=None, pool=None)) as client:
        r = await client.post(
            url, 
            params={
                'filename': filepath.name,
                'filedir': filedir
            },
            files={
                'file': (filepath.name, filepath.open('rb'), 'application/octet-stream')
            },
            headers = {
                'Authorization': f'Bearer {token}'
            }
        )
