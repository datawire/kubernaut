import click
import inspect
import sys

from kubernaut.util import *
from kubernaut.config.model import Config
from kubernaut.model import *
from kubernaut.backend import Backend
from ruamel.yaml import YAML
from typing import Optional

model_classes = inspect.getmembers(sys.modules["kubernaut.model"], inspect.isclass)

yaml = YAML(typ='safe')
yaml.register_class(ClaimSpec)


class KubernautContext:

    def __init__(self, config: Config):
        self.config = config

    def get_backend(self, name: Optional[str] = None, fail_if_missing: bool = True) -> Optional[Backend]:
        result = None
        if name is None:
            result = self.config.current_backend
        else:
            result = self.config.get_backend(name)

        if result is None and fail_if_missing:
            msg = strip_margin("""
            |
            | Kubernaut is not configured to communicate with a backend!
            |
            | Use `kubernaut config backend --help` to learn how to manage backends.
            |
            """)

            raise click.ClickException(msg)
        else:
            return result
