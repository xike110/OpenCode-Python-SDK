"""Command 资源。"""

from typing import Any, Dict, List

from ..http_client import HttpClient
from .base import BaseResource


class CommandResource(BaseResource):
    """命令管理资源。"""

    def list(self) -> List[Dict[str, Any]]:
        """
        列出所有可用的命令。

        Returns:
            命令列表

        示例:
            >>> commands = client.commands.list()
            >>> for cmd in commands:
            ...     print(f"{cmd['name']}: {cmd['description']}")
        """
        return self._http_client.get("/command")
