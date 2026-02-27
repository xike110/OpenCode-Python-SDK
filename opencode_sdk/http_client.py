"""OpenCode API 的 HTTP 客户端。"""

import json
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import httpx

from .exceptions import (
    APIError,
    BadRequestError,
    ConnectionError,
    NotFoundError,
    OpencodeException,
    TimeoutError,
)


class HttpClient:
    """用于向 OpenCode API 发送请求的 HTTP 客户端。"""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        directory: Optional[str] = None,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        初始化 HTTP 客户端。

        Args:
            base_url: OpenCode 服务器的基础 URL
            directory: 项目目录路径（添加到 x-opencode-directory header）
            timeout: 请求超时时间（秒），None 表示无超时
            headers: 要包含在请求中的额外 headers
        """
        self.base_url = base_url.rstrip("/")
        self.directory = directory
        self.timeout = timeout
        self.default_headers = headers or {}

        # 如果提供了目录，添加目录 header
        if directory:
            self.default_headers["x-opencode-directory"] = directory

        # 创建 httpx 客户端
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=self.default_headers,
        )

    def _build_url(self, path: str) -> str:
        """从路径构建完整 URL。"""
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def _handle_response(self, response: httpx.Response) -> Any:
        """处理 HTTP 响应并抛出适当的异常。"""
        try:
            # 检查 HTTP 错误
            if response.status_code == 404:
                raise NotFoundError("资源未找到")
            elif response.status_code == 400:
                try:
                    data = response.json()
                    raise BadRequestError(
                        data.get("message", "错误的请求"),
                        errors=data.get("errors", []),
                    )
                except json.JSONDecodeError:
                    raise BadRequestError("错误的请求")
            elif response.status_code >= 400:
                raise APIError(
                    message=f"HTTP {response.status_code}: {response.text}",
                    status_code=response.status_code,
                    is_retryable=response.status_code >= 500,
                    response_headers=dict(response.headers),
                    response_body=response.text,
                )

            # 解析 JSON 响应
            content_type = response.headers.get("content-type", "")
            if content_type.startswith("application/json"):
                return response.json()
            else:
                text = response.text
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return text

        except httpx.TimeoutException as e:
            raise TimeoutError(f"请求超时: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"连接失败: {str(e)}")
        except httpx.HTTPError as e:
            raise OpencodeException(f"HTTP 错误: {str(e)}")

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        发送 GET 请求。

        Args:
            path: API 端点路径
            params: 查询参数
            headers: 额外的 headers

        Returns:
            响应数据
        """
        try:
            response = self.client.get(
                path,
                params=params,
                headers=headers,
            )
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"请求超时: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"连接失败: {str(e)}")

    def post(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        发送 POST 请求。

        Args:
            path: API 端点路径
            json_data: JSON 请求体数据
            data: 表单数据
            params: 查询参数
            headers: 额外的 headers

        Returns:
            响应数据
        """
        try:
            response = self.client.post(
                path,
                json=json_data,
                data=data,
                params=params,
                headers=headers,
            )
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"请求超时: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"连接失败: {str(e)}")

    def put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        发送 PUT 请求。

        Args:
            path: API 端点路径
            json_data: JSON 请求体数据
            headers: 额外的 headers

        Returns:
            响应数据
        """
        try:
            response = self.client.put(
                path,
                json=json_data,
                headers=headers,
            )
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"请求超时: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"连接失败: {str(e)}")

    def patch(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        发送 PATCH 请求。

        Args:
            path: API 端点路径
            json_data: JSON 请求体数据
            headers: 额外的 headers

        Returns:
            响应数据
        """
        try:
            response = self.client.patch(
                path,
                json=json_data,
                headers=headers,
            )
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"请求超时: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"连接失败: {str(e)}")

    def delete(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        发送 DELETE 请求。

        Args:
            path: API 端点路径
            headers: 额外的 headers

        Returns:
            响应数据
        """
        try:
            response = self.client.delete(
                path,
                headers=headers,
            )
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"请求超时: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"连接失败: {str(e)}")

    def close(self) -> None:
        """关闭 HTTP 客户端。"""
        self.client.close()

    def __enter__(self) -> "HttpClient":
        """上下文管理器入口。"""
        return self

    def __exit__(self, *args: Any) -> None:
        """上下文管理器退出。"""
        self.close()
