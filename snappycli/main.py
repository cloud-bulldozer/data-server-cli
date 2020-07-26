#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import typer
from toolz import pipe

import auth
import client


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
def _login(url: str, username: str, password: str):
    return pipe(
        client._login_req(url, username, password),
        client.response_handler,
        lambda r: r['access_token']
    )


@exception_handler
def _post_file(url: str, token: str, filepath: Path):
    return pipe(
        client._post_file_req(url, token,filepath),
        client.response_handler
    )


@app.command()
def login(
    username: str = typer.Option(
        ...,
        prompt=True, envvar = 'DATA_SERVER_USERNAME'
    ),
    password: str = typer.Option(
        ...,
        prompt=True, hide_input=True
    ),
    url: str = typer.Argument(
        'http://localhost:8000',
        envvar = 'DATA_SERVER_URL'
    )
):  
    pipe(
        auth.add(token = _login(f'{url}/auth/jwt/login', username, password)),
        auth.save
    )    
    typer.echo('login succeeded')


@app.command()
def post_file(
    filepath: Path,
    token = None,
    url: str = typer.Argument(
        'http://localhost:8000',
        envvar = 'DATA_SERVER_URL'
    )
):
    typer.echo(
        _post_file(
            f'{url}/api', 
            token = auth.token(auth.load()),
            filepath = filepath))


@app.command()
def logout():
    auth.save(auth.rm())
    typer.echo('logged out of snappy')


@app.command()
def install():
    Path(Path.home(), '.snappy').mkdir(exist_ok=True)
    auth.save(auth.rm())
    typer.echo('snappy ready to go!')


if __name__ == '__main__':
    app()
