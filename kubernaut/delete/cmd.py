import click

from kubernaut.config.model import Config
from typing import Tuple


@click.group(
    help="Delete Kubernaut resources such as claims"
)
def delete(): pass


@delete.command(
    "claim",
    help="Delete one or more claims"
)
@click.argument("names", nargs=-1)
@click.option(
    "--all", 'all_claims',
    default=False,
    help="Delete ALL of your claims",
    is_flag=True
)
@click.pass_obj
def delete_claim(obj, names: Tuple[str], all_claims: bool):
    backend = obj.config.current_backend

    results = {}

    if all_claims:
        result = backend.delete_claim(name=None, all_claims=True)
    else:
        for name in set(names):
            result = backend.delete_claim(name)
            results[name] = result
