"""PTY (Pseudo-Terminal) 资源。"""

from typing import Any, Dict, List, Optional

from ..http_client import HttpClient
from .base import BaseResource


class PtyResource(BaseResource):
    """PTY (Pseudo-Terminal) 会话管理资源。"""

    def list(self) -> List[Dict[str, Any]]:
        """
        列出所有活动的 PTY 会话。

        Returns:
            PTY 会话列表

        示例:
            >>> sessions = client.pty.list()
            >>> for pty in sessions:
            ...     print(f"{pty['id']}: {pty['title']}")
        """
        return self._http_client.get("/pty")

    def create(
        self,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        cwd: Optional[str] = None,
        title: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        创建新的 PTY 会话。

        Args:
            command: 要执行的命令（可选）
            args: 命令参数列表（可选）
            cwd: 工作目录（可选）
            title: PTY 会话标题（可选）
            env: 环境变量字典（可选）

        Returns:
            创建的 PTY 会话信息

        示例:
            >>> # 创建默认 shell 会话
            >>> pty = client.pty.create()
            
            >>> # 创建自定义命令会话
            >>> pty = client.pty.create(
            ...     command="python",
            ...     args=["-m", "http.server"],
            ...     cwd="/path/to/project",
            ...     title="HTTP Server",
            ...     env={"PORT": "8000"}
            ... )
        """
        data = {}
        if command is not None:
            data["command"] = command
        if args is not None:
            data["args"] = args
        if cwd is not None:
            data["cwd"] = cwd
        if title is not None:
            data["title"] = title
        if env is not None:
            data["env"] = env

        return self._http_client.post("/pty", json_data=data if data else None)

    def get(self, pty_id: str) -> Dict[str, Any]:
        """
        获取指定 PTY 会话的详细信息。

        Args:
            pty_id: PTY 会话 ID

        Returns:
            PTY 会话信息

        示例:
            >>> pty = client.pty.get("pty_123")
            >>> print(pty["title"])
        """
        return self._http_client.get(f"/pty/{pty_id}")

    def update(
        self,
        pty_id: str,
        title: Optional[str] = None,
        size: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        更新 PTY 会话属性。

        Args:
            pty_id: PTY 会话 ID
            title: 新标题（可选）
            size: 终端大小 {"rows": 24, "cols": 80}（可选）

        Returns:
            更新后的 PTY 会话信息

        示例:
            >>> # 更新标题
            >>> pty = client.pty.update("pty_123", title="新标题")
            
            >>> # 更新终端大小
            >>> pty = client.pty.update(
            ...     "pty_123",
            ...     size={"rows": 30, "cols": 120}
            ... )
        """
        data = {}
        if title is not None:
            data["title"] = title
        if size is not None:
            data["size"] = size

        return self._http_client.put(f"/pty/{pty_id}", json_data=data)

    def remove(self, pty_id: str) -> bool:
        """
        移除并终止 PTY 会话。

        Args:
            pty_id: PTY 会话 ID

        Returns:
            是否成功移除

        示例:
            >>> success = client.pty.remove("pty_123")
        """
        return self._http_client.delete(f"/pty/{pty_id}")

    def connect(self, pty_id: str) -> bool:
        """
        建立 WebSocket 连接以与 PTY 会话实时交互。

        注意: 此方法返回连接状态，实际的 WebSocket 连接需要使用 WebSocket 客户端。

        Args:
            pty_id: PTY 会话 ID

        Returns:
            是否可以连接

        示例:
            >>> can_connect = client.pty.connect("pty_123")
            >>> if can_connect:
            ...     # 使用 WebSocket 客户端连接到 ws://host/pty/pty_123/connect
            ...     pass
        """
        return self._http_client.get(f"/pty/{pty_id}/connect")
