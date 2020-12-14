# Data Server (Snappy) CLI

Command line interface to a local client for a [snappy data server](https://github.com/openshift-scale/).

## Requirements

Python 3.6+  
pipx  
Running snappy data server

## Install

### pipx

```shell
python -m pip install --user pipx
```

### Snappy CLI

To facilitate your use of `snappy`, define an environment variable, `DATA_SERVER_URL`, to point to your snappy data server.


```shell
pipx install git+https://github.com/openshift-scale/data-server-cli.git
snappy install
```

## Upgrade

```shell
pipx install --force git+https://openshift-scale/data-server-cli.git
```


## Example

Usage is automatically documented by [Typer](https://typer.tiangolo.com/). 

### Help

Available commands can be listed with or without the help option.

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
  install       Automatically add required system resource for snappy cli
  login         Login to a snappy data server with a prompt.
  logout
  post-file
  script-login  Login to a snappy data server with a shell script using...
```

Snappy stores the file in the data_server directory, in case you want to create a new
directory in data_server and store file in that, set the SNAPPY_FILE_DIR env var to directory name.

Help with a command.

```shell
  snappy <cmd> --help
$ snappy script-login --help
```

```shell
Usage: snappy script-login [OPTIONS] DATA_SERVER_USERNAME
                            DATA_SERVER_PASSWORD

  Login to a snappy data server with a shell script using environment
  variables.

Arguments:
  DATA_SERVER_USERNAME  [env var: DATA_SERVER_USERNAME;required]
  DATA_SERVER_PASSWORD  [env var: DATA_SERVER_PASSWORD;required]
  SNAPPY_FILE_DIR       [env var: SNAPPY_FILE_DIR; optional]

Options:
  --data-server-url TEXT  [env var: DATA_SERVER_URL; default:
                          http://localhost:7070]

  --help                  Show this message and exit.
```

### Authentication and post

```shell
$ snappy login
```

Enter credentials.

```shell
Username:
Password:
```

```shell
$ snappy post-file ./hat.jpg
```

### When you're done

```shell
snappy logout
```
