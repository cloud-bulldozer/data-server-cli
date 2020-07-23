# Snappy Client

## Requirements

Python 3.6+

## Install

Define `DATA_SERVER_URL` to point to your snappy data server.

Feel free to install it into a virtual environment and add it to your system path, if needed.

```shell
git clone https://github.com/mfleader/snappy-client
cd snappy-client
pip install --requirement requirements.txt
```

## Example

Usage is automatically documented by [Typer](https://typer.tiangolo.com/). Available commands can be listed with the help option.

```shell
python snappy-cli.py --help
```

```shell
Usage: snappy-cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  login
  post-file

```

Get help with a command:

```shell
python snappy-cli.py <cmd> --help
python snappy-cli.py login --help
```

```shell
Usage: snappy-cli.py login [OPTIONS] [URL]

Arguments:
  [URL]  [env var: DATA_SERVER_URL;default: http://localhost:8000]

Options:
  --username TEXT  [env var: DATA_SERVER_USERNAME; required]
  --password TEXT  [required]
  --help           Show this message and exit.

```

