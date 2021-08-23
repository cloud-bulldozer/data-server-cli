import sys
from pathlib import Path
from typing import AsyncGenerator

import aiofiles
import httpx
from aiofiles import os as aios
from toolz import pipe
from tqdm import tqdm


def response_handler(r: httpx.Response) -> dict:
    try:
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        detail = r.json().get("detail", None)
        cause = "\n".join((detail, str(e))) if detail else str(e)
        raise Exception(cause).with_traceback(e.__traceback__)
    return r.json()


def _login_req(url: str, username: str, password: str) -> httpx.Response:
    return httpx.post(url, data={"username": username, "password": password})


def token(url: str, username: str, password: str) -> str:
    return pipe(_login_req(url, username, password), response_handler, lambda r: r["access_token"])


async def upload_bytes(filepath: Path, chunk_size: int = 524_288_000) -> AsyncGenerator[bytes, None]:
    # 500 MiB == 500 * 1024 * 1024 == 524,288,000
    contents = "dummy"
    pointer = 0
    async with aiofiles.open(filepath, "rb") as file:
        while contents:
            await file.seek(pointer)
            pointer += chunk_size
            contents = await file.read(chunk_size)
            yield contents


async def show_progress_bar(filepath: Path) -> AsyncGenerator[bytes, None]:
    file_stat = await aios.stat(filepath)
    with tqdm(
        total=file_stat.st_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        file=sys.stdout,
        desc=f"Posting {filepath.name}",
    ) as progress:
        async for contents in upload_bytes(filepath):
            progress.update(float(len(contents)))
            yield contents


async def _async_post_file(
    url: str, tkn: str, filepath: Path, filedir: str = "", silent: bool = False
) -> httpx.Response:

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(write=None, read=None, connect=None, pool=None)
    ) as client:
        r = await client.post(
            url,
            params={"filename": filepath.name, "filedir": filedir},
            data=upload_bytes(filepath) if silent else show_progress_bar(filepath),
            headers={"Authorization": f"Bearer {tkn}"},
        )
    return r


async def async_post_file(url: str, tkn: str, filepath: Path, filedir: str = "", silent: bool = False) -> str:
    return pipe(
        await _async_post_file(url, tkn, filepath, filedir, silent), response_handler, lambda r: r["loc"]
    )
