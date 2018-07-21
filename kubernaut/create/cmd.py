import click


@click.group()
def create():
    pass


@create.command("claim")
@click.pass_context
def create_claim(ctx):
    config = ctx.obj

    click.echo("CREATE CLAIM!")

