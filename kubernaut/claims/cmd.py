import click

from kubernaut import KubernautContext
from kubernaut.util import *
from kubernaut.model import *
from kubernaut.backend import Backend
from pathlib import Path
from typing import Tuple


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
    |     kubernaut create claim -f spec.yaml
    |
    | Use a spec file but override some properties:
    |
    |     kubernaut create claim -f spec.yaml --name=IAmTheWalrus
    |
    | Use CLI arguments only:
    |
    |     kubernaut create claim --name=prickly-pear-abc123 --cluster-group=main
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
@click.pass_obj
def create_claim(obj, filename, name: Optional[str], cluster_group: Optional[str]):
    backend = obj.config.current_backend

    spec = None
    if filename:
        spec = ClaimSpec.from_yaml(Path(filename).read_text(encoding="utf-8"))

    spec = create_final_spec(spec, {"name": name, "cluster_group": cluster_group})

    (claim, err) = _create_claim(backend, spec)


@claims.command(
    "list",
    help="List all your current claims"
)
@click.pass_obj
def list_claims(obj: KubernautContext):
    backend = obj.get_backend()
    api_res = backend.get_many_claims()
    print(api_res)

    if api_res.is_success():
        payload = api_res.json
        for claim in payload.get("claims", []):
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
def delete_claim(obj, names: Tuple[str], all_claims: bool):
    backend = obj.config.current_backend

    results = {}

    if all_claims:
        result = backend.delete_claim(name=None, all_claims=True)
    else:
        for name in set(names):
            result = backend.delete_claim(name)
            results[name] = result


def create_final_spec(spec: Optional[ClaimSpec], overrides: Dict[str, Any]) -> ClaimSpec:
    spec = spec if spec else ClaimSpec("", "")

    if overrides.get("name", None):
        spec.name = overrides["name"]
    elif not spec.name:
        spec.name = random_name()

    if overrides.get("cluster_group", None):
        spec.cluster_group = overrides["cluster_group"]
    elif not spec.cluster_group:
        spec.cluster_group = "default"

    return spec


def _create_claim(backend: Backend, spec: ClaimSpec) -> Optional[Claim]:
    api_result = backend.create_claim(spec.to_json())

    if api_result.is_success():
        return Claim(api_result.json["name"], api_result.json["kubeconfig"])
    else:
        return None
