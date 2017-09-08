#!/usr/bin/env python

import click
import json
import functools
import platform
import requests
from uuid import uuid4
from . import __version__
from scout import Scout

from pathlib2 import Path
from os import getenv
from sys import exit

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

PROGRAM_NAME = "kubernaut"

KUBERNAUT_HTTPS = getenv("KUBERNAUT_HTTPS", "1").lower() in {"1", "true", "yes"}
KUBERNAUT_HOST = getenv("KUBERNAUT_HOST", "kubernaut.io")
KUBERNAUT_ADDR = ("https://{0}" if KUBERNAUT_HTTPS else "http://{0}").format(KUBERNAUT_HOST)

# Formatting Notes
# ----------------
#
# %(prog)s is interpreted by the click library.
# {0}      is interpreted by kubernaut itself to inject version information.
#
VERSION_OUTDATED_MSG = "Your version of %(prog)s is out of date! The latest version is {0}." + \
                       " Please go to " + click.style("https://github.com/datawire/kubernaut", underline=True) + \
                       " for update instructions."

LOGIN_MSG = click.style("Kubernaut is a free service! Please get an access token to use Kubernaut => ") + \
            click.style("https://kubernaut.io/token", bold=True, underline=True) + "\n\n" + \
            click.style("Once you have your token please run `kubernaut set-token <TOKEN>`")

USER_AGENT = "{0}/{1} ({2}; {3})".format(PROGRAM_NAME, __version__, platform.system(), platform.release())

CLAIM_LIMITATION_MSGS = [
    click.style("Warning: ", fg="yellow", bold=True) + click.style("Kubernaut does not currently support LoadBalancer services!")
]

# ----------------------------------------------------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------------------------------------------------

config_root = Path.home() / ".config" / PROGRAM_NAME
config_root.mkdir(parents=True, exist_ok=True)
config_file = config_root / 'config.json'

with config_file.open('a+') as f:
    f.seek(0)
    data = f.read() or '{}'
    config = json.loads(data)

kubeconfig_root = Path.home() / ".kube"
kubeconfig_root.mkdir(exist_ok=True)

scout = Scout(PROGRAM_NAME, __version__)
scout_resp = scout.report()

# ----------------------------------------------------------------------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------------------------------------------------------------------


def save_config(config_data):
    with config_file.open('w+') as cf:
        json.dump(config_data, cf, indent=2)


def get_jwt(server):
    s = server.split("://")[1]
    if s not in config:
        click.echo("Token not found for Kubernaut. Please get a token first with `kubernaut get-token`.".format(server))
        exit(1)

    return config.get(s).get('token')


def create_headers(server):
    return {
        "Authorization": "Bearer {0}".format(get_jwt(server)),
        "User-Agent": USER_AGENT
    }


def handle_response(resp):
    failed = False
    if resp.status_code == 400:
        click.echo(resp.json()["description"])
    elif resp.status_code == 401:
        click.echo("Unable to authenticate with Kubernaut. Do you have an account?\n\n" + LOGIN_MSG)
    elif resp.status_code == 404:
        click.echo("Kubernetes cluster not found... have you claimed one? Please run `kubernaut claim`")
    elif resp.status_code == 500:
        click.echo("The kubernaut.io service is experiencing a temporary issue. Please try again later.")

    if failed:
        exit(1)


def common_options(func):
    @click.option("-s", "--server", help="Set the kubernaut server", default=KUBERNAUT_ADDR)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def create_version_message():
    msg = "%(prog)s v%(version)s"

    latest_version = scout_resp.get('latest_version', __version__)
    if latest_version != __version__:
        msg += "\n\n" + VERSION_OUTDATED_MSG.format(latest_version)

    return msg

# ----------------------------------------------------------------------------------------------------------------------
# CLI implementation
# ----------------------------------------------------------------------------------------------------------------------


@click.group()
@click.version_option(version=__version__, prog_name=PROGRAM_NAME, message=create_version_message())
def cli():
    """kubernaut: easy kubernetes clusters for painless development and testing"""


@cli.command("claim", help="Claim a Kubernetes cluster")
@common_options
def cli_claim(server):
    url = '{}/cluster'.format(server)
    resp = requests.post(url, headers=create_headers(server))

    handle_response(resp)
    if resp.status_code == 200:
        for m in CLAIM_LIMITATION_MSGS:
            click.echo(m)
            click.echo()

        with (kubeconfig_root / PROGRAM_NAME).open("w+") as f:
            f.write(resp.text)
            click.echo(
                "Wrote kubernetes config to {}".format((kubeconfig_root / "kubernaut")))


@cli.command("kubeconfig", help="Get a clusters kubeconfig")
@click.option(
    '-p', '--path-only',
    help='Only print the path after the command exits',
    is_flag=True
)
@common_options
def cli_get_kubeconfig(server, path_only):
    url = '{}/cluster'.format(server)
    resp = requests.get(url, headers=create_headers(server))

    handle_response(resp)
    if resp.status_code == 200:
        path = kubeconfig_root / PROGRAM_NAME
        with path.open("w+") as kf:
            kf.write(resp.text)
            if path_only:
                click.echo(path)
            else:
                click.echo("Wrote kubernetes config to {}".format((kubeconfig_root / PROGRAM_NAME)))


@cli.command("discard", help="Discard a previously claimed Kubernetes cluster")
@common_options
def cli_discard(server):
    url = '{}/cluster'.format(server)
    resp = requests.delete(url, headers=create_headers(server))
    handle_response(resp)


@cli.command("get-token", help="Retrieve a token to use the Kubernaut service")
def cli_get_token():
    click.echo(LOGIN_MSG)


@cli.command("set-token", help="Set a token to use the Kubernaut service")
@click.argument("token")
@common_options
def cli_set_token(server, token):
    config[server.split("://")[1]] = {"token": token}
    save_config(config)
