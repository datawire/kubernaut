import click

from kubernaut.util import *
from kubernaut import KubernautContext
from kubernaut.backend import Backend

from typing import Optional


@click.group(help="Configure your Kubernaut CLI")
def config(): pass


@config.group(help="Configure the kubernaut backend")
def backend(): pass


@backend.command(
    name="create",
    help="Create a new backend configuration",
)
@click.argument("key")
@click.option(
    "--url",
    type=str,
    default="https://kubernaut.io",
    help="The URL of the backend service"
)
@click.option(
    "--activate",
    default=False,
    type=bool,
    is_flag=True,
    help="Set the new backend as the current active backend"
)
@click.option(
    "--name",
    type=str,
    help="Assign a friendly name to the backend"
)
@click.pass_obj
def create_backend(obj: KubernautContext, key: str, url: str, activate: bool, name: Optional[str]) -> None:
    be = Backend(url, key, name)
    obj.config.add_backend(be)

    if activate or obj.config.current_backend is None:
        obj.config.current_backend = be.name

    obj.config.save()


@backend.command(
    name="delete",
    help="Delete an existing backend configuration"
)
@click.argument("name_url", type=str)
@click.pass_obj
def remove_backend(obj, name_url: str) -> None:
    obj.config.remove_backend(name_url)
    obj.config.save()


@backend.command(
    name="list",
    help="List all known backends"
)
@click.pass_obj
def list_backends(obj: KubernautContext):
    for be in obj.config.backends:
        click.echo(_fmt_backend(be))


@backend.command(name="describe", help="Show information about a single backend configuration")
@click.option(
    "--name",
    type=str,
    help="Describe a specific backend"
)
@click.pass_obj
def describe_backend(obj: KubernautContext, name: Optional[str] = None):
    _backend = obj.get_backend(name=name, fail_if_missing=False)

    if _backend:
        result = _fmt_backend(_backend)
    else:
        result = strip_margin("""
        | No backend is configured.
        """)

    click.echo(result)


def _fmt_backend(be: Backend) -> str:
    result = "Backend: " + be.url
    if be.url != be.name:
        result += (' "' + be.name + '"')

    return result
