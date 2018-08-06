from kubernaut.backend import Backend
from kubernaut.util import *
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml import StringIO
from typing import List

_yaml = YAML(typ="safe")


class Config:

    def __init__(self, load_path: Path, current_backend: Optional[Backend], backends: List[Backend]) -> None:
        self._load_path = require(load_path)
        self.active_backend_name = current_backend.name if current_backend else None
        self.backends = backends or []

    def check(self):
        pass

    @property
    def current_backend(self) -> Optional[Backend]:
        return self.get_backend(self.active_backend_name)

    @current_backend.setter
    def current_backend(self, name: str):
        backend = self.get_backend(name)
        if backend is None:
            raise ValueError("Backend not found: {}".format(name))

        self.active_backend_name = backend.name

    def get_backend(self, name) -> Optional[Backend]:
        result = None
        for be in self.backends:
            if be.name == name:
                result = be

        return result

    def add_backend(self, new_backend: Backend) -> None:
        for existing in self.backends:
            if new_backend.name == existing.name:
                raise ValueError("Backend already exists: {}".format(existing.name))

        self.backends.append(new_backend)

    def remove_backend(self, name_or_url: str) -> None:
        for existing in self.backends:
            if existing.name == name_or_url:
                if self.active_backend_name == name_or_url:
                    self.active_backend_name = None
                self.backends.remove(existing)

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
        self._load_path.write_text(string_stream.getvalue(), encoding="utf-8")

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
