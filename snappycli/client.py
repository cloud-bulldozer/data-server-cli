import sys
import os

from pathlib import Path
from typing import (AsyncGenerator, BinaryIO)

from toolz import pipe
import httpx
import aiofiles
import asyncio

from tqdm import tqdm


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


async def _tell_aiofile(file: BinaryIO) -> int:
    # with asyncio, file.tell() returns generator containing a
    # future
    done, pending = await asyncio.wait({next(file.tell())})
    return int(done.pop().result())


async def _get_file_size(file: BinaryIO) -> int:
    current_pointer = await _tell_aiofile(file)
    await file.seek(0, os.SEEK_END)
    size = await _tell_aiofile(file)
    await file.seek(current_pointer, os.SEEK_SET)

    return size


async def upload_bytes(
    file: BinaryIO, chunk_size: int = 262_144_000
) -> AsyncGenerator[bytes, None]:
    # 250 MiB == 250 * 1024 * 1024 == 262_144_000
    contents = "dummy"
    pointer = 0
    file_size = await _get_file_size(file)

    with tqdm(
        total=file_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        file=sys.stdout,
        desc=f'Posting {file.name}'
    ) as progress:
        while len(contents):
            await file.seek(pointer)
            pointer += chunk_size
            contents = await file.read(chunk_size)
            progress.update(float(chunk_size))
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
    url: str, tkn: str, filepath: Path, filedir: str = ''
) -> str:
    return pipe(
        await _async_post_file(url, tkn, filepath, filedir),
        response_handler,
        lambda r: r['loc']
    )
