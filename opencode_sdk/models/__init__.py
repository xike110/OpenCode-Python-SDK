"""OpenCode SDK 的数据模型。"""

from .common import FileDiff, Permission, Range, Todo
from .config import (
    AgentConfig,
    AgentPermission,
    Config,
    KeybindsConfig,
    McpConfig,
    McpLocalConfig,
    McpRemoteConfig,
    ProviderConfig,
)
from .events import Event, GlobalEvent
from .file import File, FileContent, FileNode, Symbol
from .message import (
    AgentPart,
    AssistantMessage,
    CompactionPart,
    FilePart,
    Message,
    Part,
    PatchPart,
    ReasoningPart,
    RetryPart,
    SnapshotPart,
    StepFinishPart,
    StepStartPart,
    SubtaskPart,
    TextPart,
    ToolPart,
    UserMessage,
)
from .other import (
    Agent,
    Auth,
    Command,
    FormatterStatus,
    LspStatus,
    McpStatus,
    Path,
    Project,
    Pty,
    ToolListItem,
    VcsInfo,
)
from .provider import Model, Provider, ProviderAuthAuthorization, ProviderAuthMethod
from .session import Session, SessionStatus

__all__ = [
    # 通用模型
    "Range",
    "FileDiff",
    "Permission",
    "Todo",
    # 会话模型
    "Session",
    "SessionStatus",
    # 消息模型
    "Message",
    "UserMessage",
    "AssistantMessage",
    "Part",
    "TextPart",
    "SubtaskPart",
    "ReasoningPart",
    "FilePart",
    "ToolPart",
    "StepStartPart",
    "StepFinishPart",
    "SnapshotPart",
    "PatchPart",
    "AgentPart",
    "RetryPart",
    "CompactionPart",
    # 事件模型
    "Event",
    "GlobalEvent",
    # 配置模型
    "Config",
    "AgentConfig",
    "AgentPermission",
    "ProviderConfig",
    "McpConfig",
    "McpLocalConfig",
    "McpRemoteConfig",
    "KeybindsConfig",
    # 提供商模型
    "Provider",
    "Model",
    "ProviderAuthMethod",
    "ProviderAuthAuthorization",
    # 文件模型
    "File",
    "FileNode",
    "FileContent",
    "Symbol",
    # 其他模型
    "Pty",
    "Agent",
    "Command",
    "ToolListItem",
    "Path",
    "VcsInfo",
    "Project",
    "McpStatus",
    "LspStatus",
    "FormatterStatus",
    "Auth",
]
