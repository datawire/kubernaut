from kubernaut.backend import Backend
from kubernaut.util import *
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml import StringIO
from typing import List

_yaml = YAML(typ="safe")


class Config:

    def __init__(self, load_path: Path, current_backend: Optional[Backend], backends: List[Backend]) -> None:
        self.load_path = require(load_path)
        self.current_backend = current_backend
        self.backends = backends or []

    def check(self):
        pass

    def add_backend(self, new_backend: Backend) -> None:
        for existing in self.backends:
            if new_backend.name == existing.name:
                raise ValueError("Backend already exists: {}".format(existing.name))

        self.backends.append(new_backend)

    def remove_backend(self, name_or_url: str) -> None:
        for existing in self.backends:
            if existing.name == name_or_url:
                self.backends.remove(existing)
                if self.current_backend.name == name_or_url:
                    self.current_backend = None

    def set_current_backend(self, new_backend: str):
        for be in self.backends:
            if be.name == new_backend:
                self.current_backend = be
                break
        else:
            raise ValueError("Backend not found: {}", new_backend)

    def save(self):
        current_be_name = None
        if self.current_backend:
            current_be_name = self.current_backend.name

        data = {
            "currentBackend": current_be_name,
            "backends": [{"name": be.name, "url": be.url, "key": be.key} for be in self.backends]
        }

        string_stream = StringIO()
        _yaml.dump(data, stream=string_stream)
        self.load_path.write_text(string_stream.getvalue(), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> 'Config':
        try:
            data = _yaml.load(path.read_text(encoding="utf-8"))
            all_backends = [Backend(be["url"], be["key"], be["name"]) for be in data.get("backends", [])]

            current = data.get("currentBackend", None)
            for be in all_backends:
                if current == be.name:
                    current = be
                    break

            return Config(path, current, all_backends)
        except FileNotFoundError as fnf:
            return Config(path, None, [])
