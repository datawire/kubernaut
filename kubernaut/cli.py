import click
from kubernaut.create.cmd import entrypoint as create_entrypoint


@click.version_option(prog_name="kubernaut")
@click.group()
@click.option("--backend-url", type=str)
def cli(ctx, backend_url):
    click.echo("main!")


if __name__ == "__main__":
    cli.add_command(create_entrypoint)
    cli()
