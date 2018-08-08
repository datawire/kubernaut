import click
import os.path

from kubernaut import __version__
from kubernaut import *
from kubernaut.config.cmd import config as config_cmd
from kubernaut.claims.cmd import claims as claims_cmd
from kubernaut.clustergroups.cmd import clustergroups
from kubernaut.config.model import Config
from pathlib import Path
from typing import Optional


@click.group()
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
@click.version_option(version=__version__, prog_name="kubernaut")
def cli(ctx: Context, kubernaut_backend: Optional[str], kubernaut_config: str):
    config = Config.load(Path(kubernaut_config))
    app_ctx = KubernautContext(config)

    if kubernaut_backend:
        config.current_backend = kubernaut_backend

    ctx.obj = app_ctx


cli.add_command(config_cmd)
cli.add_command(claims_cmd)
cli.add_command(clustergroups)


if __name__ == "__main__":
    cli()
