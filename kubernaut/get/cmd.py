import click


@click.group(
    help="Retrieve Kubernaut information or state"
)
def get(): pass


def get_cluster_group(obj, name):
    pass


def get_claim(obj, name):
    pass


def get_kubeconfig(obj, claim):
    pass

