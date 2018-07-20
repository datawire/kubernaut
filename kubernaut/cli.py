import click


from kubernaut.create.cmd import create
from kubernaut.delete.cmd import delete
from kubernaut.config.cmd import config


@click.group()
@click.version_option()
@click.option("--backend-url", type=str)
def cli(backend_url: str):
    pass


cli.add_command(config)
cli.add_command(create)
cli.add_command(delete)

if __name__ == "__main__":
    cli()
