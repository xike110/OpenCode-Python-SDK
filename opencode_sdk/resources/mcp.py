"""MCP (Model Context Protocol) 资源。"""

from typing import Any, Dict, Optional, Union

from ..http_client import HttpClient
from ..models.config import McpLocalConfig, McpRemoteConfig
from .base import BaseResource


class McpAuthResource(BaseResource):
    """MCP OAuth 认证资源。"""

    def __init__(self, http_client: HttpClient, name: str) -> None:
        """
        初始化 MCP OAuth 认证资源。

        Args:
            http_client: HTTP 客户端实例
            name: MCP 服务器名称
        """
        super().__init__(http_client)
        self.name = name

    def start(self) -> Dict[str, str]:
        """
        开始 OAuth 认证流程。

        Returns:
            包含 authorizationUrl 的字典

        示例:
            >>> result = client.mcp.auth("github").start()
            >>> print(result["authorizationUrl"])
        """
        return self._http_client.post(f"/mcp/{self.name}/auth")

    def callback(self, code: str) -> Dict[str, Any]:
        """
        完成 OAuth 认证（使用授权码）。

        Args:
            code: OAuth 回调返回的授权码

        Returns:
            MCP 服务器状态

        示例:
            >>> status = client.mcp.auth("github").callback("auth_code_123")
        """
        return self._http_client.post(
            f"/mcp/{self.name}/auth/callback",
            json_data={"code": code}
        )

    def authenticate(self) -> Dict[str, Any]:
        """
        启动 OAuth 流程并等待回调（会打开浏览器）。

        这是一个便捷方法，会自动打开浏览器并等待用户完成认证。

        Returns:
            MCP 服务器状态

        示例:
            >>> status = client.mcp.auth("github").authenticate()
        """
        return self._http_client.post(f"/mcp/{self.name}/auth/authenticate")

    def remove(self) -> Dict[str, bool]:
        """
        移除 OAuth 凭证。

        Returns:
            包含 success 字段的字典

        示例:
            >>> result = client.mcp.auth("github").remove()
            >>> print(result["success"])
        """
        return self._http_client.delete(f"/mcp/{self.name}/auth")


class McpResource(BaseResource):
    """MCP (Model Context Protocol) 服务器管理资源。"""

    def status(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有 MCP 服务器的状态。

        Returns:
            MCP 服务器状态字典，键为服务器名称

        示例:
            >>> status = client.mcp.status()
            >>> for name, info in status.items():
            ...     print(f"{name}: {info['status']}")
        """
        return self._http_client.get("/mcp")

    def add(
        self,
        name: str,
        config: Union[McpLocalConfig, McpRemoteConfig, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        动态添加新的 MCP 服务器。

        Args:
            name: MCP 服务器名称
            config: MCP 服务器配置（本地或远程）

        Returns:
            更新后的 MCP 服务器状态字典

        示例:
            >>> # 添加本地 MCP 服务器
            >>> config = {
            ...     "command": "node",
            ...     "args": ["server.js"],
            ...     "env": {"API_KEY": "xxx"}
            ... }
            >>> status = client.mcp.add("my-server", config)
            
            >>> # 添加远程 MCP 服务器
            >>> config = {
            ...     "url": "https://api.example.com/mcp",
            ...     "headers": {"Authorization": "Bearer token"}
            ... }
            >>> status = client.mcp.add("remote-server", config)
        """
        # 如果是 Pydantic 模型，转换为字典
        if hasattr(config, "model_dump"):
            config = config.model_dump(exclude_none=True)
        
        return self._http_client.post(
            "/mcp",
            json_data={"name": name, "config": config}
        )

    def connect(self, name: str) -> bool:
        """
        连接 MCP 服务器。

        Args:
            name: MCP 服务器名称

        Returns:
            是否成功连接

        示例:
            >>> success = client.mcp.connect("my-server")
        """
        return self._http_client.post(f"/mcp/{name}/connect")

    def disconnect(self, name: str) -> bool:
        """
        断开 MCP 服务器连接。

        Args:
            name: MCP 服务器名称

        Returns:
            是否成功断开

        示例:
            >>> success = client.mcp.disconnect("my-server")
        """
        return self._http_client.post(f"/mcp/{name}/disconnect")

    def auth(self, name: str) -> McpAuthResource:
        """
        获取 MCP OAuth 认证资源。

        Args:
            name: MCP 服务器名称

        Returns:
            MCP OAuth 认证资源实例

        示例:
            >>> # 开始 OAuth 认证
            >>> result = client.mcp.auth("github").start()
            >>> print(result["authorizationUrl"])
            
            >>> # 完成 OAuth 认证
            >>> status = client.mcp.auth("github").callback("auth_code")
            
            >>> # 一键认证（打开浏览器）
            >>> status = client.mcp.auth("github").authenticate()
            
            >>> # 移除认证
            >>> result = client.mcp.auth("github").remove()
        """
        return McpAuthResource(self._http_client, name)
