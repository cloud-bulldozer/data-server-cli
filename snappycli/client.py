from pathlib import Path
from typing import (AsyncGenerator, Generator, BinaryIO)

from toolz import pipe
import httpx
import aiofiles
from requests_toolbelt import MultipartEncoderMonitor, StreamingIterator
import rich.progress
import requests

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


async def async_upload_bytes(
    file: BinaryIO,
    chunk_size: int = 262_144_000
) -> AsyncGenerator[bytes, None]:
    # 250 MiB == 250 * 1024 * 1024 == 262_144_000
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
            data=async_upload_bytes(file),
            headers={
                'Authorization': f'Bearer {tkn}'
            }
        )
    return r


def upload_bytes(
    file: BinaryIO,
    chunk_size: int = 262_144_000
) -> Generator[bytes, None, None]:
    # 250 MiB == 250 * 1024 * 1024 == 262_144_000
    contents = 'dummy'
    pointer = 0
    i = 0
    while len(contents):
        file.seek(pointer)
        pointer += chunk_size
        contents = file.read(chunk_size)
        yield contents


def show_progress(
    file_size: int,
    file: BinaryIO,
    chunk_size: int = 262_144_000
    # chunks: Generator[bytes, None, None]
) -> Generator[bytes, None, None]:
    with rich.progress.Progress(
            "[progress.percentage]{task.percentage:>3.0f}%",
            rich.progress.BarColumn(bar_width=None),
            rich.progress.DownloadColumn(),
            rich.progress.TransferSpeedColumn(),
    ) as progress:
            # 250 MiB == 250 * 1024 * 1024 == 262_144_000
        contents = 'dummy'
        pointer = 0
        upload_task = progress.add_task('upoad', total=file_size)
        while len(contents):
            file.seek(pointer)
            pointer += chunk_size
            contents = file.read(chunk_size)
            progress.update(upload_task, completed=len(contents))
            yield contents

        

def _post_file(
    url: str, tkn: str, filepath: Path, filedir: str = ''
) -> httpx.Response:
    file_size = filepath.stat().st_size
    print(file_size)
    with open(filepath, 'rb') as file, \
            httpx.Client(timeout=httpx.Timeout(
                write=None, read=None, connect=None, pool=None)) as client:
        r = client.post(
            url,
            params={
                'filename': filepath.name,
                'filedir' : filedir
            },
            data=upload_bytes(file),
            # data=show_progress(file_size, file),
            headers={
                'Authorization': f'Bearer {tkn}'
            }
        )
    return r


def _tool_post_file(
    url: str, tkn: str, filepath: Path, filedir: str = ''
) -> requests.Response:
    file_size = filepath.stat().st_size
    print(file_size)
    with open(filepath, 'rb') as file:
        return requests.post(
                    url,
            params={
                'filename': filepath.name,
                'filedir' : filedir
            },
            # data=upload_bytes(file),
            data=StreamingIterator(file_size, upload_bytes(file)),
            headers={
                'Authorization': f'Bearer {tkn}'
            }
        )


def post_file(
    url: str, tkn: str, filepath: Path, filedir: str = ''
) -> str:
    return pipe(
        _post_file(url, tkn, filepath, filedir),
        # _tool_post_file(url, tkn, filepath, filedir),
        response_handler,
        lambda r: r['loc']
    )    


async def async_post_file(
    url: str, tkn: str, filepath: Path, filedir: str = ''
) -> str:
    return pipe(
        await _async_post_file(url, tkn, filepath, filedir),
        response_handler,
        lambda r: r['loc']
    )
