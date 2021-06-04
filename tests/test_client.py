import asyncio
import os
from pathlib import Path

from snappycli.client import token, async_post_file


async def main():
    # url = os.getenv('FILE_SERVER_URL')
    # tkn = token(f'{url}/auth/jwt/login',
    #             os.getenv('FILE_SERVER_UNAME'),
    #             os.getenv('FILE_SERVER_PASS'))
    # await async_post_file(
    #     f'{url}/stream', tkn,
    #     Path('/home/mleader/5M.txt')
    # )
    url = os.getenv('DATA_SERVER_URL')
    tkn = token(f'{url}/auth/jwt/login',
                os.getenv('DATA_SERVER_USERNAME'),
                os.getenv('DATA_SERVER_PASSWORD'))
    await async_post_file(
        f'{url}/stream', tkn,
        Path('/home/mleader/5M.txt')
    )


if __name__ == '__main__':
    asyncio.run(
        main()
    )