import click

from kubernaut import KubernautContext
from kubernaut.util import strip_margin


@click.group(
    help=strip_margin("""
    | Manage Kubernaut cluster groups
    |
    | A "cluster group" is an abstraction to group available Kubernetes clusters so that Kubernaut admins can create 
    | groups of clusters that implement common functionality. For example, consider a team that wants to maintain
    | three types of Kubernetes clusters for development and testing: "dev", "kubernetes-v1.9.7" and "OpenShift".
    |
    | Using a cluster group the admin can configure new clusters to register with the appropriate group. Afterwards it
    | is possible for a user to ask for a cluster from a specific group, for example, if Ophelia in Development needs
    | an OpenShift cluster she could run the below command (which is just an example) and Kubernaut would return access
    | to an OpenShift cluster in her claim.
    |
    |   `kubernaut claims create --group=OpenShift`
    |""")
)
def clustergroups():
    pass


@clustergroups.command(
    "list",
    help="List all available clustergroups"
)
@click.pass_obj
def list_claims(obj: KubernautContext):
    backend = obj.get_backend()
    api_res = backend.get_many_cluster_groups()

    if api_res.is_success():
        payload = api_res.json
        for cg in payload.get("groups", []):
            click.echo("{} - {}".format(cg["name"], cg["description"]))
    else:
        click.echo("Error retrieving cluster groups!")
