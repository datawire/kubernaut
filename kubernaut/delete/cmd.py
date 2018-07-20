import click


@click.group()
def delete():
    pass


@delete.command("claim")
def delete_claim():
    click.echo("DELETE CLAIM!")

