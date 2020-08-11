#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import typer
from toolz import pipe

import snappycli.auth as auth
import snappycli.client as client


app = typer.Typer()


def exception_handler(func):
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            typer.echo(e)
            raise typer.Abort()
    return inner_func


@exception_handler
def _post_file(url: str, token: str, filepath: Path):
    return client.post_file(
        url, token, filepath
    )


@exception_handler
def _login(url: str, username: str, password: str):
    pipe(
        auth.add(client.token(f'{url}/auth/jwt/login', username, password)),
        auth.save
    )


@app.command()
def script_login(
    data_server_username: str = typer.Argument(
        ...,
        envvar = 'DATA_SERVER_USERNAME'
    ),
    data_server_password: str = typer.Argument(
        ...,
        envvar = 'DATA_SERVER_PASSWORD'
    ),
    data_server_url: str = typer.Option(
        'http://localhost:7070',
        envvar = 'DATA_SERVER_URL'
    )
):  
    """
    Login to a snappy data server with a shell script
    using environment variables.
    """
    _login(
        data_server_url, 
        data_server_username, 
        data_server_password)


@app.command()
def login(
    username: str = typer.Option(
        ...,
        prompt=True,
        envvar = 'DATA_SERVER_USERNAME'
    ),
    password: str = typer.Option(
        ...,
        prompt=True, hide_input=True, hidden=True,
    ),
    url: str = typer.Option(
        'http://localhost:7070',
        envvar = 'DATA_SERVER_URL'
    )
):  
    """
    Login to a snappy data server with a prompt.
    """
    _login(url, username, password)
    typer.echo('login succeeded')


@app.command()
def post_file(
    filepath: Path = 
        typer.Argument(...),
    url: str = 
        typer.Option(
        'http://localhost:7070',
        envvar = 'DATA_SERVER_URL'
    )
):
    typer.echo(f"""you're file is at {
        _post_file(
            f'{url}/api', 
            token = auth.token(auth.load()),
            filepath = filepath)
    }""")


@app.command()
def logout():
    auth.save(auth.rm())
    typer.echo('logged out of snappy')


@app.command()
def install():
    """Automatically add required system resource for snappy cli"""
    Path(Path.home(), '.snappy').mkdir(exist_ok=True)
    auth.save(auth.rm())
    typer.echo('snappy ready to go!')


if __name__ == '__main__':
    app()
