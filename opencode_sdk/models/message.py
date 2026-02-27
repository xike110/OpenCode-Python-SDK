"""消息和部分数据模型。"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .common import FileDiff, Range


# ============================================================================
# 消息模型
# ============================================================================


class MessageTime(BaseModel):
    """消息时间信息。"""

    created: int = Field(..., description="创建时间戳")
    completed: Optional[int] = Field(None, description="完成时间戳")


class MessageModel(BaseModel):
    """消息模型信息。"""

    provider_id: str = Field(..., alias="providerID", description="提供商 ID")
    model_id: str = Field(..., alias="modelID", description="模型 ID")

    class Config:
        populate_by_name = True


class MessageSummary(BaseModel):
    """消息摘要信息。"""

    title: Optional[str] = Field(None, description="摘要标题")
    body: Optional[str] = Field(None, description="摘要正文")
    diffs: List[FileDiff] = Field(default_factory=list, description="文件差异列表")


class UserMessage(BaseModel):
    """用户消息。"""

    id: str = Field(..., description="消息 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    role: Literal["user"] = "user"
    time: MessageTime = Field(..., description="时间信息")
    summary: Optional[MessageSummary] = Field(None, description="消息摘要")
    agent: str = Field(..., description="代理名称")
    model: MessageModel = Field(..., description="模型信息")
    system: Optional[str] = Field(None, description="系统提示")
    tools: Optional[Dict[str, bool]] = Field(None, description="工具可用性")
    parts: List["Part"] = Field(default_factory=list, description="消息部分列表")

    class Config:
        populate_by_name = True


class MessagePath(BaseModel):
    """消息路径信息。"""

    cwd: str = Field(..., description="当前工作目录")
    root: str = Field(..., description="根目录")


class MessageTokens(BaseModel):
    """消息令牌使用情况。"""

    input: int = Field(..., description="输入令牌数")
    output: int = Field(..., description="输出令牌数")
    reasoning: int = Field(..., description="推理令牌数")
    cache: Dict[str, int] = Field(..., description="缓存令牌数（读取、写入）")


class MessageError(BaseModel):
    """消息错误信息。"""

    name: str = Field(..., description="错误名称")
    data: Dict[str, Any] = Field(..., description="错误数据")


class AssistantMessage(BaseModel):
    """助手消息。"""

    id: str = Field(..., description="消息 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    role: Literal["assistant"] = "assistant"
    time: MessageTime = Field(..., description="时间信息")
    error: Optional[MessageError] = Field(None, description="错误信息")
    parent_id: str = Field(..., alias="parentID", description="父消息 ID")
    model_id: str = Field(..., alias="modelID", description="模型 ID")
    provider_id: str = Field(..., alias="providerID", description="提供商 ID")
    mode: str = Field(..., description="模式")
    path: MessagePath = Field(..., description="路径信息")
    summary: Optional[bool] = Field(None, description="是否为摘要")
    cost: float = Field(..., description="成本")
    tokens: MessageTokens = Field(..., description="令牌使用情况")
    finish: Optional[str] = Field(None, description="完成原因")
    parts: List["Part"] = Field(default_factory=list, description="消息部分列表")

    class Config:
        populate_by_name = True


# 消息联合类型
Message = Union[UserMessage, AssistantMessage]


# ============================================================================
# 部分模型
# ============================================================================


class PartTime(BaseModel):
    """部分时间信息。"""

    start: int = Field(..., description="开始时间戳")
    end: Optional[int] = Field(None, description="结束时间戳")
    compacted: Optional[int] = Field(None, description="压缩时间戳")


class TextPart(BaseModel):
    """文本部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["text"] = "text"
    text: str = Field(..., description="文本内容")
    synthetic: Optional[bool] = Field(None, description="是否为合成内容")
    ignored: Optional[bool] = Field(None, description="是否被忽略")
    time: Optional[PartTime] = Field(None, description="时间信息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")

    class Config:
        populate_by_name = True


class ReasoningPart(BaseModel):
    """推理部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["reasoning"] = "reasoning"
    text: str = Field(..., description="推理文本")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    time: PartTime = Field(..., description="时间信息")

    class Config:
        populate_by_name = True


class FilePartSourceText(BaseModel):
    """文件部分源文本。"""

    value: str = Field(..., description="文本值")
    start: int = Field(..., description="起始位置")
    end: int = Field(..., description="结束位置")


class FileSource(BaseModel):
    """文件源。"""

    text: FilePartSourceText = Field(..., description="源文本")
    type: Literal["file"] = "file"
    path: str = Field(..., description="文件路径")


class SymbolSource(BaseModel):
    """符号源。"""

    text: FilePartSourceText = Field(..., description="源文本")
    type: Literal["symbol"] = "symbol"
    path: str = Field(..., description="文件路径")
    range: Range = Field(..., description="符号范围")
    name: str = Field(..., description="符号名称")
    kind: int = Field(..., description="符号类型")


FilePartSource = Union[FileSource, SymbolSource]


class FilePart(BaseModel):
    """文件部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["file"] = "file"
    mime: str = Field(..., description="MIME 类型")
    filename: Optional[str] = Field(None, description="文件名")
    url: str = Field(..., description="文件 URL")
    source: Optional[FilePartSource] = Field(None, description="源信息")

    class Config:
        populate_by_name = True


class ToolStatePending(BaseModel):
    """工具待处理状态。"""

    status: Literal["pending"] = "pending"
    input: Dict[str, Any] = Field(..., description="工具输入")
    raw: str = Field(..., description="原始输入")


class ToolStateRunning(BaseModel):
    """工具运行中状态。"""

    status: Literal["running"] = "running"
    input: Dict[str, Any] = Field(..., description="工具输入")
    title: Optional[str] = Field(None, description="工具标题")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    time: Dict[str, int] = Field(..., description="时间信息")


class ToolStateCompleted(BaseModel):
    """工具已完成状态。"""

    status: Literal["completed"] = "completed"
    input: Dict[str, Any] = Field(..., description="工具输入")
    output: str = Field(..., description="工具输出")
    title: str = Field(..., description="工具标题")
    metadata: Dict[str, Any] = Field(..., description="元数据")
    time: Dict[str, int] = Field(..., description="时间信息")
    attachments: Optional[List["FilePart"]] = Field(None, description="附件")


class ToolStateError(BaseModel):
    """工具错误状态。"""

    status: Literal["error"] = "error"
    input: Dict[str, Any] = Field(..., description="工具输入")
    error: str = Field(..., description="错误消息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    time: Dict[str, int] = Field(..., description="时间信息")


ToolState = Union[ToolStatePending, ToolStateRunning, ToolStateCompleted, ToolStateError]


class ToolPart(BaseModel):
    """工具部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["tool"] = "tool"
    call_id: str = Field(..., alias="callID", description="调用 ID")
    tool: str = Field(..., description="工具名称")
    state: ToolState = Field(..., description="工具状态")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")

    class Config:
        populate_by_name = True


class StepStartPart(BaseModel):
    """步骤开始部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["step-start"] = "step-start"
    snapshot: Optional[str] = Field(None, description="快照")

    class Config:
        populate_by_name = True


class StepFinishPart(BaseModel):
    """步骤完成部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["step-finish"] = "step-finish"
    reason: str = Field(..., description="完成原因")
    snapshot: Optional[str] = Field(None, description="快照")
    cost: float = Field(..., description="成本")
    tokens: MessageTokens = Field(..., description="令牌使用情况")

    class Config:
        populate_by_name = True


class SnapshotPart(BaseModel):
    """快照部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["snapshot"] = "snapshot"
    snapshot: str = Field(..., description="快照数据")

    class Config:
        populate_by_name = True


class PatchPart(BaseModel):
    """补丁部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["patch"] = "patch"
    hash: str = Field(..., description="补丁哈希")
    files: List[str] = Field(..., description="文件列表")

    class Config:
        populate_by_name = True


class AgentPartSource(BaseModel):
    """代理部分源。"""

    value: str = Field(..., description="源值")
    start: int = Field(..., description="起始位置")
    end: int = Field(..., description="结束位置")


class AgentPart(BaseModel):
    """代理部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["agent"] = "agent"
    name: str = Field(..., description="代理名称")
    source: Optional[AgentPartSource] = Field(None, description="源信息")

    class Config:
        populate_by_name = True


class RetryPart(BaseModel):
    """重试部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["retry"] = "retry"
    attempt: int = Field(..., description="重试次数")
    error: MessageError = Field(..., description="错误信息")
    time: Dict[str, int] = Field(..., description="时间信息")

    class Config:
        populate_by_name = True


class CompactionPart(BaseModel):
    """压缩部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["compaction"] = "compaction"
    auto: bool = Field(..., description="是否自动压缩")

    class Config:
        populate_by_name = True


class SubtaskPart(BaseModel):
    """子任务部分。"""

    id: str = Field(..., description="部分 ID")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    type: Literal["subtask"] = "subtask"
    prompt: str = Field(..., description="子任务提示")
    description: str = Field(..., description="子任务描述")
    agent: str = Field(..., description="代理名称")

    class Config:
        populate_by_name = True


# 所有部分的联合类型
Part = Union[
    TextPart,
    SubtaskPart,
    ReasoningPart,
    FilePart,
    ToolPart,
    StepStartPart,
    StepFinishPart,
    SnapshotPart,
    PatchPart,
    AgentPart,
    RetryPart,
    CompactionPart,
]


# 更新前向引用
ToolStateCompleted.model_rebuild()
UserMessage.model_rebuild()
AssistantMessage.model_rebuild()
