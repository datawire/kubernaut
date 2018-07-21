import click


@click.group(
    help="Create Kubernaut resources such as claims"
)
def create():
    pass


@create.command("claim")
@click.pass_context
def create_claim(ctx):
    config = ctx.obj

    click.echo("CREATE CLAIM!")

