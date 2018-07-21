import click
import os.path

from kubernaut import *
from kubernaut.create.cmd import create
from kubernaut.delete.cmd import delete
from kubernaut.config.cmd import config as config_cmd
from kubernaut.get.cmd import get
from kubernaut.config.model import Config
from pathlib import Path
from typing import Optional


@click.group()
@click.version_option()
@click.option(
    "--kubernaut-backend",
    help="Set an alternate API backend",
    default=None,
    envvar="KUBERNAUT_BACKEND",
    type=str
)
@click.option(
    "--kubernaut-config",
    help="Set an alternate config file",
    default=os.path.join(click.get_app_dir("kubernaut", roaming=True), "config"),
    envvar="KUBERNAUT_CONFIG",
    type=click.Path()
)
@click.pass_context
def cli(ctx, kubernaut_backend: Optional[str], kubernaut_config: str):
    config = Config.load(Path(kubernaut_config))
    app_ctx = Context(config)

    if kubernaut_backend:
        config.set_current_backend(kubernaut_backend)

    ctx.obj = app_ctx


cli.add_command(config_cmd)
cli.add_command(create)
cli.add_command(delete)
cli.add_command(get)

if __name__ == "__main__":
    cli()
