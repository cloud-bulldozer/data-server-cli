import subprocess as sbp
from pathlib import Path

import requests
import typer
from toolz import pipe


app = typer.Typer()


def exception_handler(func):
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            typer.echo(e)
            raise typer.Abort()
    return inner_func


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


def _post_file_req(url: str, token: str, filepath: Path):
    return requests.post(
        url,
        files = {
            'file': (str(filepath), filepath.open('rb'))
        },
        headers = {
            'Authorization': f'Bearer {token}'
        }
    )


@exception_handler
def _login(url: str, username: str, password: str):
    return pipe(
        _login_req(url, username, password),
        response_handler,
        lambda r: r['access_token']
    )


@exception_handler
def _post_file(url: str, token: str, filepath: Path):
    return pipe(
        _post_file_req(url, token,filepath),
        response_handler
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
    typer.echo(_login(f'{url}/auth/jwt/login', username, password))


@app.command()
def post_file(
    token: str,
    filepath: Path,
    url: str = typer.Argument(
        'http://localhost:8000',
        envvar = 'DATA_SERVER_URL'
    )
):
    typer.echo(_post_file(f'{url}/api', token, filepath))


if __name__ == '__main__':
    app()
