"""TUI (Terminal User Interface) 资源。"""

from typing import Any, Dict, Literal, Optional

from ..http_client import HttpClient
from .base import BaseResource


class TuiResource(BaseResource):
    """TUI (Terminal User Interface) 交互资源。"""

    def append_prompt(self, text: str) -> bool:
        """
        追加文本到 TUI 提示框。

        Args:
            text: 要追加的文本

        Returns:
            是否成功追加

        示例:
            >>> success = client.tui.append_prompt("你好，")
            >>> success = client.tui.append_prompt("世界！")
        """
        return self._http_client.post(
            "/tui/append-prompt",
            json_data={"text": text}
        )

    def submit_prompt(self) -> bool:
        """
        提交 TUI 提示框中的内容。

        Returns:
            是否成功提交

        示例:
            >>> client.tui.append_prompt("帮我写一个函数")
            >>> client.tui.submit_prompt()
        """
        return self._http_client.post("/tui/submit-prompt")

    def clear_prompt(self) -> bool:
        """
        清空 TUI 提示框。

        Returns:
            是否成功清空

        示例:
            >>> success = client.tui.clear_prompt()
        """
        return self._http_client.post("/tui/clear-prompt")

    def execute_command(self, command: str) -> bool:
        """
        执行 TUI 命令。

        Args:
            command: 要执行的命令（例如 "agent_cycle"）

        Returns:
            是否成功执行

        示例:
            >>> success = client.tui.execute_command("agent_cycle")
        """
        return self._http_client.post(
            "/tui/execute-command",
            json_data={"command": command}
        )

    def show_toast(
        self,
        message: str,
        variant: Literal["info", "success", "warning", "error"],
        title: Optional[str] = None,
        duration: int = 5000
    ) -> bool:
        """
        在 TUI 中显示提示消息。

        Args:
            message: 提示消息内容
            variant: 消息类型（info/success/warning/error）
            title: 消息标题（可选）
            duration: 显示时长（毫秒），默认 5000

        Returns:
            是否成功显示

        示例:
            >>> # 显示成功消息
            >>> client.tui.show_toast("操作成功", "success")
            
            >>> # 显示错误消息
            >>> client.tui.show_toast(
            ...     "操作失败",
            ...     "error",
            ...     title="错误",
            ...     duration=10000
            ... )
        """
        data = {
            "message": message,
            "variant": variant,
            "duration": duration
        }
        if title is not None:
            data["title"] = title

        return self._http_client.post("/tui/show-toast", json_data=data)

    def open_help(self) -> bool:
        """
        打开 TUI 帮助对话框。

        Returns:
            是否成功打开

        示例:
            >>> success = client.tui.open_help()
        """
        return self._http_client.post("/tui/open-help")

    def open_sessions(self) -> bool:
        """
        打开 TUI 会话列表对话框。

        Returns:
            是否成功打开

        示例:
            >>> success = client.tui.open_sessions()
        """
        return self._http_client.post("/tui/open-sessions")

    def open_themes(self) -> bool:
        """
        打开 TUI 主题选择对话框。

        Returns:
            是否成功打开

        示例:
            >>> success = client.tui.open_themes()
        """
        return self._http_client.post("/tui/open-themes")

    def open_models(self) -> bool:
        """
        打开 TUI 模型选择对话框。

        Returns:
            是否成功打开

        示例:
            >>> success = client.tui.open_models()
        """
        return self._http_client.post("/tui/open-models")

    def select_session(self, session_id: str) -> bool:
        """
        选择指定的会话。

        Args:
            session_id: 会话 ID

        Returns:
            是否成功选择

        示例:
            >>> success = client.tui.select_session("ses_123")
        """
        return self._http_client.post(
            "/tui/select-session",
            json_data={"sessionID": session_id}
        )

    def publish(self, event: Dict[str, Any]) -> bool:
        """
        发布 TUI 事件。

        Args:
            event: 事件数据

        Returns:
            是否成功发布

        示例:
            >>> event = {
            ...     "type": "tui.prompt.append",
            ...     "text": "Hello"
            ... }
            >>> success = client.tui.publish(event)
        """
        return self._http_client.post("/tui/publish", json_data=event)
