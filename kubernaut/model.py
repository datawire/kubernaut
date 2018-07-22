import json
from ruamel.yaml import StringIO, YAML


class ClaimSpec:

    def __init__(self, name: str, cluster_group: str) -> None:
        self.name = name
        self.cluster_group = cluster_group

    def validate(self):
        pass

    def to_json(self):
        data = {"name": self.name}
        if self.cluster_group:
            data["clusterGroup"] = self.cluster_group

        return json.dumps(data, indent=4)

    @classmethod
    def from_json(cls, json_string: str) -> 'ClaimSpec':
        data = json.loads(json_string)
        return ClaimSpec(data["name"], data["clusterGroup"])

    @classmethod
    def from_yaml(cls, yaml_string: str) -> 'ClaimSpec':
        yaml = YAML(typ="safe")
        data = yaml.load(yaml_string)

        return ClaimSpec(
            name=data.get("name", None),
            cluster_group=data.get("clusterGroup", None)
        )


class Claim:

    def __init__(self, name: str, kubeconfig: str) -> None:
        self.name = name
        self.kubeconfig = kubeconfig
