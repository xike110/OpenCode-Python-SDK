"""OpenCode 主客户端。"""

from typing import Any, Dict, Optional

from .http_client import HttpClient
from .resources.base import BaseResource


class OpencodeClient:
    """
    OpenCode API 客户端。

    这是与 OpenCode API 交互的主要入口点。
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        directory: Optional[str] = None,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        初始化 OpenCode 客户端。

        Args:
            base_url: OpenCode 服务器的基础 URL（默认: http://localhost:8000）
            directory: 项目目录路径（添加到 x-opencode-directory header）
            timeout: 请求超时时间（秒），None 表示无超时
            headers: 要包含在请求中的额外 headers

        示例:
            >>> client = OpencodeClient(
            ...     base_url="http://localhost:8000",
            ...     directory="/path/to/project"
            ... )
        """
        self._http_client = HttpClient(
            base_url=base_url,
            directory=directory,
            timeout=timeout,
            headers=headers,
        )

        # 初始化资源
        from .resources import (
            SessionResource,
            EventResource,
            ProjectResource,
            ConfigResource,
            ProviderResource,
            FileResource,
            FindResource,
            McpResource,
            LspResource,
            PtyResource,
            ToolResource,
            TuiResource,
            AppResource,
            CommandResource,
            GlobalResource,
            InstanceResource,
            PathResource,
            VcsResource,
            FormatterResource,
            AuthResource,
        )
        
        # ==================== 核心资源 ====================
        # 会话管理：创建、列表、更新、删除 AI 编码会话，发送消息
        self.sessions = SessionResource(self._http_client)
        
        # 事件订阅：订阅实时事件流（SSE），接收流式响应
        self.events = EventResource(self._http_client)
        
        # 项目管理：列出和管理项目
        self.projects = ProjectResource(self._http_client)
        
        # 配置管理：获取和更新系统配置（模型、提供商等）
        self.config = ConfigResource(self._http_client)
        
        # 提供商管理：管理 AI 提供商（如 OpenAI、Anthropic 等）
        self.providers = ProviderResource(self._http_client)
        
        # 文件操作：读取、列表文件
        self.files = FileResource(self._http_client)
        
        # 搜索功能：搜索文件、文本内容
        self.find = FindResource(self._http_client)
        
        # ==================== 高级功能资源 ====================
        # MCP 集成：模型上下文协议（Model Context Protocol）服务器管理
        self.mcp = McpResource(self._http_client)
        
        # LSP 集成：语言服务器协议（Language Server Protocol）
        self.lsp = LspResource(self._http_client)
        
        # PTY 管理：伪终端（Pseudo-Terminal）会话管理
        self.pty = PtyResource(self._http_client)
        
        # 工具管理：列出可用的工具（bash、read、write 等）
        self.tools = ToolResource(self._http_client)
        
        # TUI 交互：终端用户界面（Terminal UI）交互
        self.tui = TuiResource(self._http_client)
        
        # 应用管理：应用程序管理和日志
        self.app = AppResource(self._http_client)
        
        # 命令管理：命令管理
        self.commands = CommandResource(self._http_client)
        
        # ==================== 全局和系统资源 ====================
        # 全局资源：全局事件和系统级操作
        self.global_resource = GlobalResource(self._http_client)
        
        # 实例管理：OpenCode 实例管理
        self.instance = InstanceResource(self._http_client)
        
        # 路径管理：路径相关操作
        self.path = PathResource(self._http_client)
        
        # 版本控制：Git 等版本控制系统集成
        self.vcs = VcsResource(self._http_client)
        
        # 格式化工具：代码格式化工具管理
        self.formatter = FormatterResource(self._http_client)
        
        # 认证管理：用户认证和授权
        self.auth = AuthResource(self._http_client)

    def close(self) -> None:
        """关闭客户端并释放资源。"""
        self._http_client.close()

    def __enter__(self) -> "OpencodeClient":
        """上下文管理器入口。"""
        return self

    def __exit__(self, *args: Any) -> None:
        """上下文管理器退出。"""
        self.close()


def create_opencode_client(
    base_url: str = "http://localhost:8000",
    directory: Optional[str] = None,
    timeout: Optional[float] = None,
    headers: Optional[Dict[str, str]] = None,
) -> OpencodeClient:
    """
    创建 OpenCode 客户端实例。

    这是创建客户端的便捷函数。

    Args:
        base_url: OpenCode 服务器的基础 URL
        directory: 项目目录路径
        timeout: 请求超时时间（秒）
        headers: 额外的 headers

    Returns:
        OpencodeClient 实例

    示例:
        >>> client = create_opencode_client(
        ...     base_url="http://localhost:8000",
        ...     directory="/path/to/project"
        ... )
    """
    return OpencodeClient(
        base_url=base_url,
        directory=directory,
        timeout=timeout,
        headers=headers,
    )
