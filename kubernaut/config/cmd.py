import click


@click.group()
def config():
    pass


@config.command(name="set-token")
def config_set_token():
    click.echo("set-token")


@config.command(name="view-token")
def config_view_token():
    click.echo("view-token")
