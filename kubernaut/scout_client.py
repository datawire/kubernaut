class Scout:

    def __init__(self, application, version, scout_host="kubernaut.io/scout"):
        import os

        if not isinstance(application, str) or str(application).strip() == '':
            raise ValueError("Application name is not a string, blank, empty or null")

        if not isinstance(version, str) or str(application).strip() == '':
            raise ValueError("Application version is not a string, blank, empty or null")

        self.application = str(application)
        self.version = str(version)
        self.scout_host = str(scout_host)
        self.disabled = os.getenv("SCOUT_DISABLED", "0").lower() in {"1", "true", "yes"}

    def send(self, metadata):
        import requests

        if not self.disabled:
            payload = {
                'application': self.application,
                'version': self.version,
                'metadata': metadata or {}
            }

            try:
                requests.post("https://{0}".format(self.scout_host), json=payload, timeout=1)
                return {'latest_version': '1.0.0'}
            except:
                return {'latest_version': '1.0.0'}
        else:
            return {}
