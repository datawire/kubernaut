import requests

from kubernaut.util import require
from typing import Dict


class RawBackendResponse:

    def __init__(self, status_code: int, headers: Dict[str, str] = None, content: str = None):
        self.status_code = require(status_code)
        self.headers = headers or {}
        self.content = content


class Backend:

    def __init__(self, backend_url, backend_key, **kwargs):
        self.backend_url = require(backend_url)
        self.backend_key = require(backend_key)

    # ==========================================================================
    # Low-level HTTP cluster-groups API
    # ==========================================================================

    def list_cluster_groups(self) -> RawBackendResponse:
        headers = self.__init_headers()
        headers["content-type"] = "application/json"

        resp = requests.get(url=self.__fmt_url("/cluster-groups"),
                            headers=headers)

        return RawBackendResponse(resp.status_code, resp.headers, resp.text)

    def describe_cluster_group(self, name: str) -> RawBackendResponse:
        headers = self.__init_headers()
        headers["content-type"] = "application/json"

        resp = requests.get(url=self.__fmt_url("/cluster-groups/{}".format(name)),
                            headers=headers)

        return RawBackendResponse(resp.status_code, resp.headers, resp.text)

    # ==========================================================================
    # Low-level HTTP claims API
    # ==========================================================================

    def create_claim(self, json_payload) -> RawBackendResponse:
        headers = self.__init_headers()
        headers["content-type"] = "application/json"

        resp = requests.post(url=self.__fmt_url("/claims"),
                             headers=headers,
                             json=json_payload)

        return RawBackendResponse(resp.status_code, resp.headers, resp.text)

    def describe_claim(self, name) -> RawBackendResponse:
        headers = self.__init_headers()
        resp = requests.get(url=self.__fmt_url("/claims/{}".format(name)),
                            headers=headers)

        return RawBackendResponse(resp.status_code, resp.headers, resp.text)

    def delete_claim(self, name: str) -> RawBackendResponse:
        headers = self.__init_headers()
        resp = requests.delete(url=self.__fmt_url("/claims/{}".format(name)),
                               headers=headers)

        return RawBackendResponse(resp.status_code, resp.headers, resp.text)

    def list_claims(self):
        headers = self.__init_headers()
        headers["content-type"] = "application/json"

        resp = requests.get(url=self.__fmt_url("/claims"),
                            headers=headers)

        return RawBackendResponse(resp.status_code, resp.headers, resp.text)

    # ==========================================================================
    # Internals
    # ==========================================================================

    def __fmt_url(self, resource):
        return "{0}/{1}".format(self.backend_url, resource)

    def __init_headers(self) -> Dict[str, str]:
        return {
            "authorization": "Bearer {0}".format(self.backend_key),
            "user-agent": "kubernaut/{0}".format("v1alpha2")
        }
