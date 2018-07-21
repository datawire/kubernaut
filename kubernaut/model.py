class ClaimSpec:

    def __init__(self, name, cluster_group) -> None:
        self.name = name
        self.cluster_group = cluster_group


class Claim:

    def __init__(self, name, cluster_group) -> None:
        self.name = name


class ClusterGroup:

    def __init__(self, name: str, available_clusters: int) -> None:
        self.name = name
        self.available_clusters = available_clusters

