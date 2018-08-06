import click

from kubernaut.util import *
from kubernaut.model import *
from kubernaut.backend import Backend
from pathlib import Path


@click.group(
    help="Create Kubernaut resources such as claims"
)
def create():
    pass


@create.command(
    "claim",
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


def create_final_spec(spec: Optional[ClaimSpec], overrides: Dict[str, Any]) -> ClaimSpec:
    spec = spec if spec else ClaimSpec("", "")

    if overrides.get("name", None):
        spec.name = overrides["name"]
    elif not spec.name:
        spec.name = generate_claim_name()

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











































