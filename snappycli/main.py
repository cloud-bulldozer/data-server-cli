# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from functools import wraps
from pathlib import Path
from typing import Callable

import typer
from toolz import pipe

import snappycli.auth as auth
import snappycli.client as client

app = typer.Typer()


def exception_handler(fn: Callable) -> Callable:
    if asyncio.iscoroutinefunction(fn):

        @wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                typer.echo(e)
                raise typer.Abort()

        return wrapper
    else:

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                typer.echo(e)
                raise typer.Abort()

        return wrapper


@exception_handler
async def _async_post_file(url: str, token: str, filepath: Path, filedir: str, silent: bool) -> str:
    r = await client.async_post_file(url=url, tkn=token, filepath=filepath, filedir=filedir, silent=silent)
    return r


@exception_handler
def _login(url: str, username: str, password: str) -> str:
    pipe(auth.add(client.token(f"{url}/auth/jwt/login", username, password)), auth.save)


@app.command()
def script_login(
    data_server_username: str = typer.Argument(..., envvar="DATA_SERVER_USERNAME"),
    data_server_password: str = typer.Argument(..., envvar="DATA_SERVER_PASSWORD"),
    data_server_url: str = typer.Option("http://localhost:7070", envvar="DATA_SERVER_URL"),
) -> None:
    """
    Login to a snappy data server with a shell script
    using environment variables.
    """
    _login(data_server_url, data_server_username, data_server_password)


@app.command()
def login(
    username: str = typer.Option(..., prompt=True, envvar="DATA_SERVER_USERNAME"),
    password: str = typer.Option(
        ...,
        prompt=True,
        hide_input=True,
        hidden=True,
    ),
    url: str = typer.Option("http://localhost:7070", envvar="DATA_SERVER_URL"),
) -> None:
    """
    Login to a snappy data server with a prompt.
    """
    _login(url, username, password)
    typer.echo("login succeeded")


@app.command()
def post_file(
    filepath: Path = typer.Argument(...),
    url: str = typer.Option("http://localhost:7070", envvar="DATA_SERVER_URL"),
    filedir: str = typer.Option("", envvar="SNAPPY_FILE_DIR"),
    silent: bool = typer.Option(False, "-s", "--silent"),
) -> None:
    typer.echo(
        f"""your file is at {
    asyncio.run(_async_post_file(
        url=f'{url}/api',
        token=auth.token(auth.load()),
        filepath=filepath,
        filedir=filedir,
        silent=silent))
    }"""
    )


@app.command()
def logout() -> None:
    auth.save(auth.rm())
    typer.echo("logged out of snappy")


@app.command()
def install() -> None:
    """Automatically add required system resource for snappy cli"""
    Path(Path.home(), ".snappy").mkdir(exist_ok=True)
    auth.save(auth.rm())
    typer.echo("snappy ready to go!")


if __name__ == "__main__":
    app()
