import json
import requests

from typing import Dict, Optional


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__, ', '.join('%s=%s' % item for item in vars(self).items()))
    cls.__str__ = __str__
    return cls


@auto_str
class RawBackendResponse:

    def __init__(self, status_code: int, headers: Dict[str, str], content: str = None) -> None:
        self.status_code = status_code
        self.headers = headers or {}
        self.content = content

        self.headers = {k.lower(): v for k, v in self.headers.items()}

        if "application/json" in headers.get("content-type", ""):
            self.json = json.loads(self.content, encoding="utf-8")

    def is_success(self):
        return self.status_code // 100 == 2


class Backend:

    def __init__(self, url, key, name: Optional[str]) -> None:
        self.url = url
        self.key = key
        self.name = name or self.url

    def __str__(self) -> str:
        return "Backend(url={}, name={})".format(self.url, self.name)

    # ==========================================================================
    # Low-level HTTP cluster-groups API
    # ==========================================================================

    def get_many_cluster_groups(self) -> RawBackendResponse:
        headers = self.__init_headers()
        headers["content-type"] = "application/json"

        resp = requests.get(url=self.__fmt_url("/cluster-groups"),
                            headers=headers)

        return RawBackendResponse(resp.status_code, dict(resp.headers), resp.text)

    def describe_cluster_group(self, name: str) -> RawBackendResponse:
        headers = self.__init_headers()
        headers["content-type"] = "application/json"

        resp = requests.get(url=self.__fmt_url("/cluster-groups/{0}".format(name)),
                            headers=headers)

        return RawBackendResponse(resp.status_code, dict(resp.headers), resp.text)

    # ==========================================================================
    # Low-level HTTP claims API
    # ==========================================================================

    def create_claim(self, json_payload) -> RawBackendResponse:
        headers = self.__init_headers()
        headers["content-type"] = "application/json"

        resp = requests.post(url=self.__fmt_url("/claims"),
                             headers=headers,
                             data=json_payload)

        return RawBackendResponse(resp.status_code, dict(resp.headers), resp.text)

    def get_claim(self, name) -> RawBackendResponse:
        headers = self.__init_headers()
        resp = requests.get(url=self.__fmt_url("/claims/{}".format(name)),
                            headers=headers)

        return RawBackendResponse(resp.status_code, dict(resp.headers), resp.text)

    def delete_claim(self, name: str, all_claims: bool = False) -> RawBackendResponse:
        headers = self.__init_headers()
        path = "/claims" if all_claims else "/claims/{}".format(name)
        resp = requests.delete(url=self.__fmt_url(path), headers=headers)

        return RawBackendResponse(resp.status_code, dict(resp.headers), resp.text)

    def get_many_claims(self):
        headers = self.__init_headers()
        headers["content-type"] = "application/json"
        resp = requests.get(url=self.__fmt_url("/claims"),
                            headers=headers)

        return RawBackendResponse(resp.status_code, dict(resp.headers), resp.text)

    # ==========================================================================
    # Internals
    # ==========================================================================

    def __fmt_url(self, resource: Optional[str]) -> str:
        return "{0}{1}".format(self.url.rstrip("/"), resource or "")

    def __init_headers(self) -> Dict[str, str]:
        return {
            "authorization": "Bearer {0}".format(self.key),
            "user-agent": "kubernaut/{0}".format("v1alpha2")
        }
