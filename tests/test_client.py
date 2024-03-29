import asyncio
import os
from pathlib import Path

from snappycli.client import async_post_file, token


async def main():
    url = os.getenv("FILE_SERVER_URL")
    tkn = token(f"{url}/auth/jwt/login", os.getenv("FILE_SERVER_UNAME"), os.getenv("FILE_SERVER_PASS"))

    await async_post_file(f"{url}/api", tkn, Path("/home/mleader/1G.txt"), "", True)


if __name__ == "__main__":
    asyncio.run(main())
