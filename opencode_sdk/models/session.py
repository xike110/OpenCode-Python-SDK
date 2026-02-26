"""会话数据模型。"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .common import FileDiff


class SessionStatusIdle(BaseModel):
    """会话空闲状态。"""

    type: Literal["idle"] = "idle"


class SessionStatusRetry(BaseModel):
    """会话重试状态。"""

    type: Literal["retry"] = "retry"
    attempt: int = Field(..., description="重试次数")
    message: str = Field(..., description="重试消息")
    next: int = Field(..., description="下次重试时间戳")


class SessionStatusBusy(BaseModel):
    """会话忙碌状态。"""

    type: Literal["busy"] = "busy"


# 会话状态联合类型
SessionStatus = Union[SessionStatusIdle, SessionStatusRetry, SessionStatusBusy]


class SessionSummary(BaseModel):
    """会话摘要信息。"""

    additions: int = Field(..., description="新增行数")
    deletions: int = Field(..., description="删除行数")
    files: int = Field(..., description="修改的文件数")
    diffs: Optional[List[FileDiff]] = Field(None, description="文件差异列表")


class SessionShare(BaseModel):
    """会话分享信息。"""

    url: str = Field(..., description="分享链接")


class SessionRevert(BaseModel):
    """会话回退信息。"""

    message_id: str = Field(..., alias="messageID", description="要回退到的消息 ID")
    part_id: Optional[str] = Field(None, alias="partID", description="要回退到的部分 ID")
    snapshot: Optional[str] = Field(None, description="快照数据")
    diff: Optional[str] = Field(None, description="差异数据")

    class Config:
        populate_by_name = True


class SessionTime(BaseModel):
    """会话时间信息。"""

    created: int = Field(..., description="创建时间戳")
    updated: int = Field(..., description="最后更新时间戳")
    compacting: Optional[int] = Field(None, description="压缩时间戳")


class Session(BaseModel):
    """会话模型。"""

    id: str = Field(..., description="会话 ID")
    project_id: str = Field(..., alias="projectID", description="项目 ID")
    directory: str = Field(..., description="项目目录")
    parent_id: Optional[str] = Field(None, alias="parentID", description="父会话 ID")
    summary: Optional[SessionSummary] = Field(None, description="会话摘要")
    share: Optional[SessionShare] = Field(None, description="分享信息")
    title: str = Field(..., description="会话标题")
    version: str = Field(..., description="会话版本")
    time: SessionTime = Field(..., description="时间信息")
    revert: Optional[SessionRevert] = Field(None, description="回退信息")

    class Config:
        populate_by_name = True
