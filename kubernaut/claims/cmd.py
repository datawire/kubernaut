import click
import operator
import sys

from kubernaut import KubernautContext
from kubernaut.kubeconfig import *
from kubernaut.util import *
from kubernaut.model import *
from kubernaut.backend import Backend
from pathlib import Path
from typing import List


@click.group(
    help="Manage Kubernetes cluster claims"
)
def claims():
    pass


@claims.command(
    "create",
    help=strip_margin("""
    | Create a claim
    |
    | Use a spec file:
    |
    |     kubernaut claims create -f spec.yaml
    |
    | Use a spec file but override some properties:
    |
    |     kubernaut claims create -f spec.yaml --name=IAmTheWalrus
    |
    | Use CLI arguments only:
    |
    |     kubernaut claims create --name=prickly-pear-abc123 --cluster-group=main
    |""")
)
@click.option(
    "--filename", "-f",
    help="Create a claim from a claim spec file",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--name",
    help="Set the name of a claim. If not set a random value is provided",
    type=str,
)
@click.option(
    "--cluster-group",
    help="Set the cluster-group to claim from",
    type=str,
)
@click.option(
    "--length",
    help="Set the length of the claim in minutes",
    type=int,
    default=1440
)
@click.pass_obj
def create_claim(obj, filename, name: Optional[str], cluster_group: Optional[str], length: int):
    backend = obj.config.current_backend

    if length < 1:
        length = 1440

    spec = None
    if filename:
        spec = ClaimSpec.from_yaml(Path(filename).read_text(encoding="utf-8"))

    spec = create_final_spec(spec, {"name": name, "cluster_group": cluster_group, "length": length})

    pattern = '^[a-z][a-z0-9-_]*[a-z0-9]$'
    if not re.search(pattern, spec.name, re.IGNORECASE | re.ASCII):
        raise click.ClickException("Claim name does not match allowed pattern: '{}'".format(pattern))

    claim = _create_claim(backend, spec)
    if claim:
        kubeconfig_path = Path.home() / ".kube" / "{}.yaml".format(spec.name)
        write_kubeconfig(claim.kubeconfig, kubeconfig_path)
        click.echo(kubeconfig_message(kubeconfig_path))
    else:
        raise click.ClickException("Unable to create claim!")


@claims.command(
    "list",
    help="List all your current claims"
)
@click.pass_obj
def list_claims(obj: KubernautContext):
    backend = obj.get_backend()
    api_res = backend.get_many_claims()

    if api_res.is_success():
        claims_list = api_res.json.get("claims", [])
        claims_list.sort(key=operator.itemgetter('name'))

        if len(claims_list) == 0:
            click.echo("No active claims found")

        for claim in claims_list:
            click.echo(claim["name"])
    else:
        click.echo("Error retrieving claims!")


@claims.command(
    "delete",
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
def delete_claim(obj, names: List[str], all_claims: bool):
    backend = obj.get_backend()

    results = {}

    if all_claims:
        result = backend.delete_claim(name=None, all_claims=True)
    else:
        for name in set(names):
            result = backend.delete_claim(name)
            results[name] = result


@claims.command(
    "get-kubeconfig",
    help="Describe one or more claims"
)
@click.argument("name", nargs=1)
@click.pass_obj
def get_kubeconfig(obj, name: str) -> None:
    backend = obj.config.current_backend
    api_res = backend.get_claim(name)

    if api_res.is_success():
        print(api_res.json["claim"]["kubeconfig"])
    else:
        print("No active claim found: {}".format(name))
        sys.exit(1)

@claims.command(
    "describe",
    help="Describe one or more claims"
)
@click.argument("name", nargs=1)
@click.pass_obj
def describe_claim(obj, name: str) -> None:
    backend = obj.config.current_backend
    api_res = backend.get_claim(name)

    if api_res.is_success():
        print(api_res.json["claim"]["name"])
    else:
        print("No active claim found: {}".format(name))


def create_final_spec(spec: Optional[ClaimSpec], overrides: Dict[str, Any]) -> ClaimSpec:
    spec = spec if spec else ClaimSpec("", "", 0)

    if overrides.get("name", None):
        spec.name = overrides["name"]
    elif not spec.name:
        spec.name = random_name()

    if overrides.get("cluster_group", None):
        spec.cluster_group = overrides["cluster_group"]
    elif not spec.cluster_group:
        spec.cluster_group = "default"

    if overrides.get("length", None):
        spec.length = overrides["length"]
    elif not spec.length:
        spec.length = 1440

    return spec


def _create_claim(backend: Backend, spec: ClaimSpec) -> Optional[Claim]:
    api_result = backend.create_claim(spec.to_json())
    if api_result.is_success():
        return Claim(api_result.json["claim"]["name"], api_result.json["claim"]["kubeconfig"])
    else:
        print(api_result)
        return None
