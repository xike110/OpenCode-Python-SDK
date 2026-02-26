"""App 资源。"""

from typing import Any, Dict, List, Literal, Optional

from ..http_client import HttpClient
from .base import BaseResource


class AppResource(BaseResource):
    """应用管理资源。"""

    def log(
        self,
        service: str,
        level: Literal["debug", "info", "warn", "error"],
        message: str,
        extra: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        写入日志到服务器。

        Args:
            service: 服务名称
            level: 日志级别（debug/info/warn/error）
            message: 日志消息
            extra: 额外的元数据（可选）

        Returns:
            是否成功写入

        示例:
            >>> # 写入信息日志
            >>> client.app.log("my-service", "info", "操作成功")
            
            >>> # 写入错误日志并附加元数据
            >>> client.app.log(
            ...     "my-service",
            ...     "error",
            ...     "操作失败",
            ...     extra={"user_id": "123", "action": "delete"}
            ... )
        """
        data = {
            "service": service,
            "level": level,
            "message": message
        }
        if extra is not None:
            data["extra"] = extra

        return self._http_client.post("/log", json_data=data)

    def agents(self) -> List[Dict[str, Any]]:
        """
        列出所有可用的 AI 代理。

        Returns:
            代理列表

        示例:
            >>> agents = client.app.agents()
            >>> for agent in agents:
            ...     print(f"{agent['name']}: {agent['description']}")
        """
        return self._http_client.get("/agent")

    def skills(self) -> List[Dict[str, Any]]:
        """
        列出所有可用的技能。

        Returns:
            技能列表

        示例:
            >>> skills = client.app.skills()
            >>> for skill in skills:
            ...     print(f"{skill['name']}: {skill['description']}")
        """
        return self._http_client.get("/skill")
