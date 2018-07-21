import click

from kubernaut import Context
from kubernaut.backend import Backend
from kubernaut.config.model import Config

from typing import Optional


@click.group(
    help="Configure the kubernaut CLI"
)
def config(): pass


@config.command(name="add-backend")
@click.argument("key")
@click.option(
    "--url",
    type=str,
    default="https://kubernaut.io"
)
@click.option(
    "--current",
    default=False,
    type=bool,
)
@click.option(
    "--name",
    type=str
)
@click.pass_obj
def add_backend(obj: Context, key: str, url: str, current: bool, name: Optional[str]) -> None:
    conf: Config = obj.config
    backend = Backend(url, key, name)
    conf.add_backend(backend)

    if current or conf.current_backend is None:
        conf.set_current_backend(backend.name)

    conf.save()


@config.command(name="remove-backend")
@click.argument("name_url", type=str)
@click.pass_obj
def remove_backend(obj, name_url: str) -> None:
    conf: Config = obj.config
    conf.remove_backend(name_url)
    conf.save()


@config.command(name="view-backend")
@click.pass_obj
def get_backend(obj):
    backend = obj.config.current_backend

    result = "Backend: "
    if backend:
        result += backend.url
        if backend.url != backend.name:
            result += (' "' + backend.name + '"')
    else:
        result += "None configured"

    click.echo(result)
