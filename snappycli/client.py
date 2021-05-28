from pathlib import Path
from typing import (AsyncGenerator, BinaryIO)

from toolz import pipe
import httpx
import aiofiles


def response_handler(r: httpx.Response) -> dict:
    r.raise_for_status()
    return r.json()


def _login_req(
    url: str, username: str, password: str
) -> httpx.Response:
    return httpx.post(
        url,
        data={
            'username': username,
            'password': password
        })


def token(url: str, username: str, password: str) -> str:
    return pipe(
        _login_req(url, username, password),
        response_handler,
        lambda r: r['access_token']
    )


async def upload_bytes(
    file: BinaryIO,
    chunk_size: int = 1_000_000
) -> AsyncGenerator[bytes, None]:
    contents = 'dummy'
    pointer = 0
    while len(contents):
        await file.seek(pointer)
        pointer += chunk_size
        contents = await file.read(chunk_size)
        yield contents


async def _async_post_file(
    url: str, tkn: str, filepath: Path, filedir: str = ''
) -> httpx.Response:
    async with aiofiles.open(filepath, 'rb') as file, \
            httpx.AsyncClient(timeout=httpx.Timeout(
                write=None, read=None, connect=None, pool=None)) as client:
        r = await client.post(
            url,
            params={
                'filename': filepath.name,
                'filedir' : filedir
            },
            data=upload_bytes(file),
            headers={
                'Authorization': f'Bearer {tkn}'
            }
        )
    return r


async def async_post_file(
    url: str, tkn: str, filepath: Path, filedir: str
) -> str:
    return pipe(
        await _async_post_file(url, tkn, filepath, filedir),
        response_handler,
        lambda r: r['loc']
    )
