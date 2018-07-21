from kubernaut.config.model import Config


class Context:
    def __init__(self, config: Config):
        self.config = config
