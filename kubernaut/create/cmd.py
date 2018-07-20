import click


@click.group(name="create")
def entrypoint():
    pass


def create_claim():
    click.echo("CREATE CLAIM!")

