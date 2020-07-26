# Snappy CLI

## Requirements

Python 3.6+  
pipx  
Running [snappy data server](https://github.com/openshift-scale/snappy-data-server)

## Install

### pipx

```shell
python -m pip install --user pipx
```

### Snappy CLI

Define `DATA_SERVER_URL` to point to your [snappy data server](https://github.com/openshift-scale/snappy-data-server).


```shell
pipx install git+https://github.com/mfleader/snappyCLI.git
snappy install
```

## Example

Usage is automatically documented by [Typer](https://typer.tiangolo.com/). Available commands can be listed with or without the help option.

```shell
$ snappy
```

```shell
Usage: snappy [OPTIONS] COMMAND [ARGS]...

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
$ snappy <cmd> --help
$ snappy login --help
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

