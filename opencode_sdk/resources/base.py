"""OpenCode SDK 的基础资源类。"""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..http_client import HttpClient


class BaseResource:
    """所有 API 资源的基类。"""

    def __init__(self, client: "HttpClient") -> None:
        """
        初始化资源。

        Args:
            client: HTTP 客户端实例
        """
        self._http_client = client

    def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """发送 GET 请求。"""
        return self._http_client.get(path, params=params, headers=headers)

    def _post(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """发送 POST 请求。"""
        return self._http_client.post(path, json_data=json_data, data=data, headers=headers)

    def _put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """发送 PUT 请求。"""
        return self._http_client.put(path, json_data=json_data, headers=headers)

    def _patch(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """发送 PATCH 请求。"""
        return self._http_client.patch(path, json_data=json_data, headers=headers)

    def _delete(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """发送 DELETE 请求。"""
        return self._http_client.delete(path, headers=headers)
