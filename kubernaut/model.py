import json
from ruamel.yaml import StringIO, YAML
from typing import Optional


class ClaimSpec:

    def __init__(self, name: str, cluster_group: str, length: int) -> None:
        self.name = name
        self.cluster_group = cluster_group
        self.length = length

    def validate(self):
        pass

    def to_json(self):
        data = {"name": self.name, "length": self.length}
        if self.cluster_group:
            data["group"] = self.cluster_group

        return json.dumps(data, indent=4)

    @classmethod
    def from_json(cls, json_string: str) -> 'ClaimSpec':
        data = json.loads(json_string)
        return ClaimSpec(data["name"], data["clusterGroup"], data["length"])

    @classmethod
    def from_yaml(cls, yaml_string: str) -> 'ClaimSpec':
        yaml = YAML(typ="safe")
        data = yaml.load(yaml_string)

        return ClaimSpec(
            name=data.get("name", None),
            cluster_group=data.get("clusterGroup", None),
            length=data.get("length", None)
        )


class Claim:

    def __init__(self, name: str, kubeconfig: str) -> None:
        self.name = name
        self.kubeconfig = kubeconfig

    @classmethod
    def from_json(cls, json_string: str) -> 'Claim':
        data = json.loads(json_string)
        return Claim(data["name"], data["kubeconfig"])


class ClusterGroup:

    def __init__(self, name: str, description: Optional[str] = None) -> None:
        self.name = name
        self.description = description

    @classmethod
    def from_json(cls, json_string: str) -> 'ClusterGroup':
        data = json.loads(json_string)
        return ClusterGroup(data["name"], data.get("description"))
