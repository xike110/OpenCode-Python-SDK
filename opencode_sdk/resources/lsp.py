"""LSP (Language Server Protocol) 资源。"""

from typing import Any, Dict, List

from ..http_client import HttpClient
from .base import BaseResource


class LspResource(BaseResource):
    """LSP (Language Server Protocol) 服务器状态资源。"""

    def status(self) -> List[Dict[str, Any]]:
        """
        获取所有 LSP 服务器的状态。

        Returns:
            LSP 服务器状态列表

        示例:
            >>> status_list = client.lsp.status()
            >>> for lsp in status_list:
            ...     print(f"{lsp['name']}: {lsp['status']}")
        """
        return self._http_client.get("/lsp")
