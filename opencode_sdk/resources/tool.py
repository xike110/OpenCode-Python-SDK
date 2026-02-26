"""Tool 资源。"""

from typing import Any, Dict, List

from ..http_client import HttpClient
from .base import BaseResource


class ToolResource(BaseResource):
    """工具管理资源。"""

    def ids(self) -> List[str]:
        """
        获取所有可用的工具 ID 列表。

        包括内置工具和动态注册的工具。

        Returns:
            工具 ID 列表

        示例:
            >>> tool_ids = client.tools.ids()
            >>> print(tool_ids)
            ['read', 'write', 'edit', 'bash', 'grep', ...]
        """
        return self._http_client.get("/experimental/tool/ids")

    def list(self, provider_id: str, model_id: str) -> List[Dict[str, Any]]:
        """
        获取指定提供商和模型的可用工具列表。

        Args:
            provider_id: 提供商 ID
            model_id: 模型 ID

        Returns:
            工具列表，每个工具包含：
            - id: 工具 ID
            - description: 工具描述
            - parameters: JSON Schema 参数定义

        示例:
            >>> tools = client.tools.list("anthropic", "claude-3-5-sonnet-20241022")
            >>> for tool in tools:
            ...     print(f"{tool['id']}: {tool['description']}")
            ...     print(f"参数: {tool['parameters']}")
        """
        return self._http_client.get(
            "/experimental/tool",
            params={"provider": provider_id, "model": model_id}
        )
