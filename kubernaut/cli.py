#!/usr/bin/env python
import click

import click
import json
import functools
import requests

from pathlib import Path
from requests.auth import HTTPBasicAuth
from sys import exit

DEFAULT_SERVER = "kubernaut.io"

config_root = Path.home() / ".config" / "kubernaut"
config_root.mkdir(exist_ok=True)

kubeconfig_root = Path.home() / ".kube"
kubeconfig_root.mkdir(exist_ok=True)

config_file = config_root / 'config.json'


def load_config():
    with config_file.open('a+') as f:
        f.seek(0)
        data = f.read() or '{}'
        return json.loads(data)

config = load_config()


def create_basic_auth(server):
    credentials = config.get('credentials', {})
    if server not in credentials:
        click.echo("Credentials not found for {}. Please login first with `kubernaut login`.".format(server))
        exit(1)

    return HTTPBasicAuth(credentials[server]['username'], credentials[server]['password'])


def common_options(func):
    @click.option("-s", "--server", help="Set the kubernaut server", default=DEFAULT_SERVER)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """kubernaut: easy kubernetes clusters for painless development and testing"""


@cli.command("claim", help="claim your Kubernetes cluster")
@common_options
def cli_claim(server):
    url = 'http://{}/cluster'.format(server)
    auth = create_basic_auth(server)
    resp = requests.post(url, auth=auth)

    if resp.status_code == 401:
        click.echo("Authentication Failed!")
        exit(1)
    if resp.status_code == 400:
        click.echo("Error!")
    if resp.status_code == 200:
        with (kubeconfig_root / "kubernaut-{}".format(auth.username)).open("a+") as f:
            f.write(resp.text)
            click.echo(
                "Wrote kubernetes config to {}".format((kubeconfig_root / "kubernaut-{}".format(auth.username))))


@cli.command("kubeconfig", help="retrieve clusters kubeconfig")
@click.option(
    '-p', '--path-only',
    help='Only print the path after the command exits',
    is_flag=True
)
@common_options
def cli_get_kubeconfig(server, path_only):
    url = 'http://{}/cluster'.format(server)
    auth = create_basic_auth(server)
    resp = requests.get(url, auth=auth)

    if resp.status_code == 401:
        click.echo("Authentication Failed!")
        exit(1)
    if resp.status_code == 404:
        click.echo("Kubernetes cluster not found... have you claimed one? Please run `kubernaut claim`")
    if resp.status_code == 200:
        path = kubeconfig_root / "kubernaut-{}".format(auth.username)
        with path.open("a+") as f:
            f.write(resp.text)
            if path_only:
                click.echo(path)
            else:
                click.echo(
                    "Wrote kubernetes config to {}".format((kubeconfig_root / "kubernaut-{}".format(auth.username))))


@cli.command("release", help="release your Kubernetes cluster")
@common_options
def cli_release(server):
    url = 'http://{}/cluster'.format(server)
    auth = create_basic_auth(server)
    resp = requests.delete(url, auth=auth)

    if resp.status_code == 401:
        click.echo("Authentication Failed!")
        exit(1)


@cli.command("login", help="login to access the kubernaut.io service")
@common_options
@click.option("-u", "--username", prompt=True)
@click.option("-p", "--password", prompt=True, hide_input=True)
def cli_login(server, username, password):
    if 'credentials' not in config:
        config['credentials'] = {}

    credentials = config['credentials']
    credentials[server] = {'username': username, 'password': password}

    config['credentials'] = credentials
    print(config)

    save_config(config)


# TODO: Implement
#
# @cli.command("register", help="register with the kubernaut.io service")
# def cli_register():
#     pass


def save_config(data):
    with config_file.open('w+') as f:
        json.dump(data, f, indent=2)
