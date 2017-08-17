from . import __version__


class Scout:

    def __init__(self, application, version, install_id, user_agent, scout_host="kubernaut.io/scout"):
        import os

        if not isinstance(application, str) or str(application).strip() == '':
            raise ValueError("Application name is not a string, blank, empty or null")

        if not isinstance(version, str) or str(application).strip() == '':
            raise ValueError("Application version is not a string, blank, empty or null")

        self.application = str(application)
        self.version = str(version)
        self.install_id = str(install_id)
        self.user_agent = str(user_agent)
        self.scout_host = str(scout_host)
        self.disabled = os.getenv("SCOUT_DISABLE", "0").lower() in {"1", "true", "yes"}

    def send(self, metadata):
        import requests

        result = {'latest_version': __version__}  # default to current version

        if not self.disabled:
            payload = {
                'application': self.application,
                'install_id': self.install_id,
                'version': self.version,
                'metadata': metadata or {}
            }

            headers = {'User-Agent': self.user_agent}

            try:
                resp = requests.post("https://{0}".format(self.scout_host), headers=headers, json=payload, timeout=1)
                success = resp.status_code / 100 == 2
                if success:
                    result = resp.json()
            except:
                pass

        return result
