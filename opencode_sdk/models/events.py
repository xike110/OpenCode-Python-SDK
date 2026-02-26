"""事件数据模型。"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .common import FileDiff, Permission
from .message import Message, Part
from .session import SessionStatus


# ============================================================================
# 服务器事件
# ============================================================================


class EventServerInstanceDisposed(BaseModel):
    """服务器实例已释放事件。"""

    type: Literal["server.instance.disposed"] = "server.instance.disposed"
    properties: Dict[str, str] = Field(..., description="事件属性（目录）")


class EventServerConnected(BaseModel):
    """服务器已连接事件。"""

    type: Literal["server.connected"] = "server.connected"
    properties: Dict[str, Any] = Field(default_factory=dict, description="事件属性")


# ============================================================================
# 安装事件
# ============================================================================


class EventInstallationUpdated(BaseModel):
    """安装已更新事件。"""

    type: Literal["installation.updated"] = "installation.updated"
    properties: Dict[str, str] = Field(..., description="事件属性（版本）")


class EventInstallationUpdateAvailable(BaseModel):
    """安装更新可用事件。"""

    type: Literal["installation.update-available"] = "installation.update-available"
    properties: Dict[str, str] = Field(..., description="事件属性（版本）")


# ============================================================================
# LSP 事件
# ============================================================================


class EventLspClientDiagnostics(BaseModel):
    """LSP 客户端诊断事件。"""

    type: Literal["lsp.client.diagnostics"] = "lsp.client.diagnostics"
    properties: Dict[str, str] = Field(..., description="事件属性（服务器ID、路径）")


class EventLspUpdated(BaseModel):
    """LSP 已更新事件。"""

    type: Literal["lsp.updated"] = "lsp.updated"
    properties: Dict[str, Any] = Field(default_factory=dict, description="事件属性")


# ============================================================================
# 消息事件
# ============================================================================


class EventMessageUpdatedProperties(BaseModel):
    """消息已更新事件属性。"""

    info: Message = Field(..., description="消息信息")


class EventMessageUpdated(BaseModel):
    """消息已更新事件。"""

    type: Literal["message.updated"] = "message.updated"
    properties: EventMessageUpdatedProperties = Field(..., description="事件属性")


class EventMessageRemovedProperties(BaseModel):
    """消息已删除事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")

    class Config:
        populate_by_name = True


class EventMessageRemoved(BaseModel):
    """消息已删除事件。"""

    type: Literal["message.removed"] = "message.removed"
    properties: EventMessageRemovedProperties = Field(..., description="事件属性")


class EventMessagePartUpdatedProperties(BaseModel):
    """消息部分已更新事件属性。"""

    part: Part = Field(..., description="部分信息")
    delta: Optional[str] = Field(None, description="增量文本")


class EventMessagePartUpdated(BaseModel):
    """消息部分已更新事件。"""

    type: Literal["message.part.updated"] = "message.part.updated"
    properties: EventMessagePartUpdatedProperties = Field(..., description="事件属性")


class EventMessagePartRemovedProperties(BaseModel):
    """消息部分已删除事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    part_id: str = Field(..., alias="partID", description="部分 ID")

    class Config:
        populate_by_name = True


class EventMessagePartRemoved(BaseModel):
    """消息部分已删除事件。"""

    type: Literal["message.part.removed"] = "message.part.removed"
    properties: EventMessagePartRemovedProperties = Field(..., description="事件属性")


# ============================================================================
# 权限事件
# ============================================================================


class EventPermissionUpdated(BaseModel):
    """权限已更新事件。"""

    type: Literal["permission.updated"] = "permission.updated"
    properties: Permission = Field(..., description="权限信息")


class EventPermissionRepliedProperties(BaseModel):
    """权限已回复事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    permission_id: str = Field(..., alias="permissionID", description="权限 ID")
    response: str = Field(..., description="响应")

    class Config:
        populate_by_name = True


class EventPermissionReplied(BaseModel):
    """权限已回复事件。"""

    type: Literal["permission.replied"] = "permission.replied"
    properties: EventPermissionRepliedProperties = Field(..., description="事件属性")


# ============================================================================
# 会话事件
# ============================================================================


class EventSessionStatusProperties(BaseModel):
    """会话状态事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    status: SessionStatus = Field(..., description="会话状态")

    class Config:
        populate_by_name = True


class EventSessionStatus(BaseModel):
    """会话状态事件。"""

    type: Literal["session.status"] = "session.status"
    properties: EventSessionStatusProperties = Field(..., description="事件属性")


class EventSessionIdleProperties(BaseModel):
    """会话空闲事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")

    class Config:
        populate_by_name = True


class EventSessionIdle(BaseModel):
    """会话空闲事件。"""

    type: Literal["session.idle"] = "session.idle"
    properties: EventSessionIdleProperties = Field(..., description="事件属性")


class EventSessionCompactedProperties(BaseModel):
    """会话已压缩事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")

    class Config:
        populate_by_name = True


class EventSessionCompacted(BaseModel):
    """会话已压缩事件。"""

    type: Literal["session.compacted"] = "session.compacted"
    properties: EventSessionCompactedProperties = Field(..., description="事件属性")


class EventSessionCreatedProperties(BaseModel):
    """会话已创建事件属性。"""

    info: Any = Field(..., description="会话信息")  # 将是 Session 类型


class EventSessionCreated(BaseModel):
    """会话已创建事件。"""

    type: Literal["session.created"] = "session.created"
    properties: EventSessionCreatedProperties = Field(..., description="事件属性")


class EventSessionUpdatedProperties(BaseModel):
    """会话已更新事件属性。"""

    info: Any = Field(..., description="会话信息")  # 将是 Session 类型


class EventSessionUpdated(BaseModel):
    """会话已更新事件。"""

    type: Literal["session.updated"] = "session.updated"
    properties: EventSessionUpdatedProperties = Field(..., description="事件属性")


class EventSessionDeletedProperties(BaseModel):
    """会话已删除事件属性。"""

    info: Any = Field(..., description="会话信息")  # 将是 Session 类型


class EventSessionDeleted(BaseModel):
    """会话已删除事件。"""

    type: Literal["session.deleted"] = "session.deleted"
    properties: EventSessionDeletedProperties = Field(..., description="事件属性")


class EventSessionDiffProperties(BaseModel):
    """会话差异事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    diff: List[FileDiff] = Field(..., description="文件差异列表")

    class Config:
        populate_by_name = True


class EventSessionDiff(BaseModel):
    """会话差异事件。"""

    type: Literal["session.diff"] = "session.diff"
    properties: EventSessionDiffProperties = Field(..., description="事件属性")


class EventSessionErrorProperties(BaseModel):
    """会话错误事件属性。"""

    session_id: Optional[str] = Field(None, alias="sessionID", description="会话 ID")
    error: Optional[Dict[str, Any]] = Field(None, description="错误信息")

    class Config:
        populate_by_name = True


class EventSessionError(BaseModel):
    """会话错误事件。"""

    type: Literal["session.error"] = "session.error"
    properties: EventSessionErrorProperties = Field(..., description="事件属性")


# ============================================================================
# 文件事件
# ============================================================================


class EventFileEditedProperties(BaseModel):
    """文件已编辑事件属性。"""

    file: str = Field(..., description="文件路径")


class EventFileEdited(BaseModel):
    """文件已编辑事件。"""

    type: Literal["file.edited"] = "file.edited"
    properties: EventFileEditedProperties = Field(..., description="事件属性")


class EventFileWatcherUpdatedProperties(BaseModel):
    """文件监视器已更新事件属性。"""

    file: str = Field(..., description="文件路径")
    event: Literal["add", "change", "unlink"] = Field(..., description="事件类型")


class EventFileWatcherUpdated(BaseModel):
    """文件监视器已更新事件。"""

    type: Literal["file.watcher.updated"] = "file.watcher.updated"
    properties: EventFileWatcherUpdatedProperties = Field(..., description="事件属性")


# ============================================================================
# VCS 事件
# ============================================================================


class EventVcsBranchUpdatedProperties(BaseModel):
    """VCS 分支已更新事件属性。"""

    branch: Optional[str] = Field(None, description="分支名称")


class EventVcsBranchUpdated(BaseModel):
    """VCS 分支已更新事件。"""

    type: Literal["vcs.branch.updated"] = "vcs.branch.updated"
    properties: EventVcsBranchUpdatedProperties = Field(..., description="事件属性")


# ============================================================================
# 待办事项事件
# ============================================================================


class EventTodoUpdatedProperties(BaseModel):
    """待办事项已更新事件属性。"""

    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    todos: List[Any] = Field(..., description="待办事项列表")  # 将是 Todo 类型

    class Config:
        populate_by_name = True


class EventTodoUpdated(BaseModel):
    """待办事项已更新事件。"""

    type: Literal["todo.updated"] = "todo.updated"
    properties: EventTodoUpdatedProperties = Field(..., description="事件属性")


# ============================================================================
# 命令事件
# ============================================================================


class EventCommandExecutedProperties(BaseModel):
    """命令已执行事件属性。"""

    name: str = Field(..., description="命令名称")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    arguments: str = Field(..., description="命令参数")
    message_id: str = Field(..., alias="messageID", description="消息 ID")

    class Config:
        populate_by_name = True


class EventCommandExecuted(BaseModel):
    """命令已执行事件。"""

    type: Literal["command.executed"] = "command.executed"
    properties: EventCommandExecutedProperties = Field(..., description="事件属性")


# ============================================================================
# TUI 事件
# ============================================================================


class EventTuiPromptAppendProperties(BaseModel):
    """TUI 提示追加事件属性。"""

    text: str = Field(..., description="要追加的文本")


class EventTuiPromptAppend(BaseModel):
    """TUI 提示追加事件。"""

    type: Literal["tui.prompt.append"] = "tui.prompt.append"
    properties: EventTuiPromptAppendProperties = Field(..., description="事件属性")


class EventTuiCommandExecuteProperties(BaseModel):
    """TUI 命令执行事件属性。"""

    command: str = Field(..., description="要执行的命令")


class EventTuiCommandExecute(BaseModel):
    """TUI 命令执行事件。"""

    type: Literal["tui.command.execute"] = "tui.command.execute"
    properties: EventTuiCommandExecuteProperties = Field(..., description="事件属性")


class EventTuiToastShowProperties(BaseModel):
    """TUI 提示显示事件属性。"""

    title: Optional[str] = Field(None, description="提示标题")
    message: str = Field(..., description="提示消息")
    variant: Literal["info", "success", "warning", "error"] = Field(..., description="提示类型")
    duration: Optional[int] = Field(None, description="持续时间（毫秒）")


class EventTuiToastShow(BaseModel):
    """TUI 提示显示事件。"""

    type: Literal["tui.toast.show"] = "tui.toast.show"
    properties: EventTuiToastShowProperties = Field(..., description="事件属性")


# ============================================================================
# PTY 事件
# ============================================================================


class EventPtyCreatedProperties(BaseModel):
    """PTY 已创建事件属性。"""

    info: Any = Field(..., description="PTY 信息")  # 将是 Pty 类型


class EventPtyCreated(BaseModel):
    """PTY 已创建事件。"""

    type: Literal["pty.created"] = "pty.created"
    properties: EventPtyCreatedProperties = Field(..., description="事件属性")


class EventPtyUpdatedProperties(BaseModel):
    """PTY 已更新事件属性。"""

    info: Any = Field(..., description="PTY 信息")  # 将是 Pty 类型


class EventPtyUpdated(BaseModel):
    """PTY 已更新事件。"""

    type: Literal["pty.updated"] = "pty.updated"
    properties: EventPtyUpdatedProperties = Field(..., description="事件属性")


class EventPtyExitedProperties(BaseModel):
    """PTY 已退出事件属性。"""

    id: str = Field(..., description="PTY ID")
    exit_code: int = Field(..., alias="exitCode", description="退出代码")

    class Config:
        populate_by_name = True


class EventPtyExited(BaseModel):
    """PTY 已退出事件。"""

    type: Literal["pty.exited"] = "pty.exited"
    properties: EventPtyExitedProperties = Field(..., description="事件属性")


class EventPtyDeletedProperties(BaseModel):
    """PTY 已删除事件属性。"""

    id: str = Field(..., description="PTY ID")


class EventPtyDeleted(BaseModel):
    """PTY 已删除事件。"""

    type: Literal["pty.deleted"] = "pty.deleted"
    properties: EventPtyDeletedProperties = Field(..., description="事件属性")


# ============================================================================
# 事件联合类型
# ============================================================================

Event = Union[
    EventServerInstanceDisposed,
    EventServerConnected,
    EventInstallationUpdated,
    EventInstallationUpdateAvailable,
    EventLspClientDiagnostics,
    EventLspUpdated,
    EventMessageUpdated,
    EventMessageRemoved,
    EventMessagePartUpdated,
    EventMessagePartRemoved,
    EventPermissionUpdated,
    EventPermissionReplied,
    EventSessionStatus,
    EventSessionIdle,
    EventSessionCompacted,
    EventSessionCreated,
    EventSessionUpdated,
    EventSessionDeleted,
    EventSessionDiff,
    EventSessionError,
    EventFileEdited,
    EventFileWatcherUpdated,
    EventVcsBranchUpdated,
    EventTodoUpdated,
    EventCommandExecuted,
    EventTuiPromptAppend,
    EventTuiCommandExecute,
    EventTuiToastShow,
    EventPtyCreated,
    EventPtyUpdated,
    EventPtyExited,
    EventPtyDeleted,
]


class GlobalEvent(BaseModel):
    """全局事件包装器。"""

    directory: str = Field(..., description="目录")
    payload: Event = Field(..., description="事件载荷")
