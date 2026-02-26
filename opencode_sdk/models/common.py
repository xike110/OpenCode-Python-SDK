"""通用数据模型。"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Range(BaseModel):
    """代码范围，包含起始和结束位置。"""

    start: Dict[str, int] = Field(..., description="起始位置（行号，字符位置）")
    end: Dict[str, int] = Field(..., description="结束位置（行号，字符位置）")


class FileDiff(BaseModel):
    """文件差异信息。"""

    file: str = Field(..., description="文件路径")
    before: str = Field(..., description="修改前的内容")
    after: str = Field(..., description="修改后的内容")
    additions: int = Field(..., description="新增行数")
    deletions: int = Field(..., description="删除行数")


class Permission(BaseModel):
    """权限请求。"""

    id: str = Field(..., description="权限 ID")
    type: str = Field(..., description="权限类型")
    pattern: Optional[str | list[str]] = Field(None, description="匹配模式")
    session_id: str = Field(..., alias="sessionID", description="会话 ID")
    message_id: str = Field(..., alias="messageID", description="消息 ID")
    call_id: Optional[str] = Field(None, alias="callID", description="工具调用 ID")
    title: str = Field(..., description="权限标题")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="额外的元数据")
    time: Dict[str, int] = Field(..., description="时间戳信息")

    class Config:
        populate_by_name = True


class Todo(BaseModel):
    """待办事项。"""

    id: str = Field(..., description="唯一标识符")
    content: str = Field(..., description="任务的简要描述")
    status: str = Field(..., description="状态: pending, in_progress, completed, cancelled")
    priority: str = Field(..., description="优先级: high, medium, low")
