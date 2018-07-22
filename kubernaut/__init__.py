import inspect
import sys

from kubernaut.config.model import Config
from kubernaut.model import *
from ruamel.yaml import YAML

model_classes = inspect.getmembers(sys.modules["kubernaut.model"], inspect.isclass)

yaml = YAML(typ='safe')
yaml.register_class(ClaimSpec)


class Context:
    def __init__(self, config: Config):
        self.config = config
