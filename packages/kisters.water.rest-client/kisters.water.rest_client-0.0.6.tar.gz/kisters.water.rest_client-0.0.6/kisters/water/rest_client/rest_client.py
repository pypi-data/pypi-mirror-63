from typing import Iterable, List, Optional, Union

import requests
import msgpack

from .auth import Authentication


class RESTClient:
    def __init__(self, url: str, *, authentication: Authentication = None):
        super().__init__()
        self._url = url.rstrip("/")
        self._auth = authentication
        self._session = requests.Session()

    @property
    def url(self):
        return self._url

    @property
    def session(self):
        return self._session

    def _construct_url(self, resource: Union[str, Iterable[str]]) -> str:
        if isinstance(resource, str):
            return "/".join((self.url, resource))
        return "/".join((self.url, *resource))

    @staticmethod
    def _verify_response(response):
        if response.status_code == 422:
            raise ValueError(response.json())
        response.raise_for_status()

    def get(
        self,
        resource: Union[str, Iterable[str]],
        *,
        parameters: Optional[dict] = None,
        data: Optional[Union[dict, List[dict]]] = None,
        headers: Optional[dict] = None,
        msgpack_data: Optional[bool] = None,
    ) -> Union[dict, List[dict]]:
        """Get data located at a resource"""
        return self.request(
            "get",
            resource,
            parameters=parameters,
            data=data,
            headers=headers,
            msgpack_data=msgpack_data,
        )

    def put(
        self,
        resource: Union[str, Iterable[str]],
        *,
        parameters: Optional[dict] = None,
        data: Optional[Union[dict, List[dict]]] = None,
        headers: Optional[dict] = None,
        msgpack_data: Optional[bool] = None,
    ):
        """Overwrite data located at a resource"""
        return self.request(
            "put",
            resource,
            parameters=parameters,
            data=data,
            headers=headers,
            msgpack_data=msgpack_data,
        )

    def post(
        self,
        resource: Union[str, Iterable[str]],
        *,
        parameters: Optional[dict] = None,
        data: Optional[Union[dict, List[dict]]] = None,
        headers: Optional[dict] = None,
        msgpack_data: Optional[bool] = None,
    ):
        """Send data to a resource"""
        return self.request(
            "post",
            resource,
            parameters=parameters,
            data=data,
            headers=headers,
            msgpack_data=msgpack_data,
        )

    def delete(
        self,
        resource: Union[str, Iterable[str]],
        *,
        parameters: Optional[dict] = None,
        data: Optional[Union[dict, List[dict]]] = None,
        headers: Optional[dict] = None,
        msgpack_data: Optional[bool] = None,
    ):
        """Delete data located at a resource"""
        return self.request(
            "delete",
            resource,
            parameters=parameters,
            data=data,
            headers=headers,
            msgpack_data=msgpack_data,
        )

    def request(
        self,
        method: str,
        resource: Union[str, Iterable[str]],
        *,
        parameters: Optional[dict] = None,
        data: Optional[Union[dict, List[dict]]] = None,
        headers: Optional[dict] = None,
        msgpack_data: Optional[bool] = None,
    ):
        headers = headers or {}
        if self._auth:
            headers["Authorization"] = f"Bearer {self._auth.get_access_token()}"
        if msgpack_data:
            headers["accept"] = "application/x-msgpack"
        json = None
        if data is not None:
            if msgpack_data:
                data = msgpack.packb(data)
                headers["content-type"] = "application/x-msgpack"
            else:
                json = data
                data = None
        resp = self._session.request(
            method,
            self._construct_url(resource),
            params=parameters,
            json=json,
            data=data,
            headers=headers,
        )
        self._verify_response(resp)
        if resp.headers.get("Content-Type") == "application/x-msgpack":
            return msgpack.unpackb(resp.content, raw=False)
        if resp.headers.get("Content-Type") == "application/json":
            return resp.json()
        return resp
