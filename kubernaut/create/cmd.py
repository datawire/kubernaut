import click


@click.group()
def create():
    pass


@create.command("claim")
def create_claim():
    click.echo("CREATE CLAIM!")

