"""其他数据模型（PTY、Agent、Command 等）。"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ============================================================================
# PTY 模型
# ============================================================================


class Pty(BaseModel):
    """PTY（伪终端）会话。"""

    id: str = Field(..., description="PTY ID")
    title: str = Field(..., description="PTY 标题")
    command: str = Field(..., description="命令")
    args: List[str] = Field(..., description="命令参数")
    cwd: str = Field(..., description="当前工作目录")
    status: Literal["running", "exited"] = Field(..., description="PTY 状态")
    pid: int = Field(..., description="进程 ID")


# ============================================================================
# Agent 模型
# ============================================================================


class AgentPermission(BaseModel):
    """代理权限配置。"""

    edit: Literal["ask", "allow", "deny"] = Field(..., description="编辑权限")
    bash: Dict[str, Literal["ask", "allow", "deny"]] = Field(..., description="Bash 权限")
    webfetch: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="网页抓取权限")
    doom_loop: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="死循环权限")
    external_directory: Optional[Literal["ask", "allow", "deny"]] = Field(
        None, description="外部目录权限"
    )


class AgentModel(BaseModel):
    """代理模型配置。"""

    model_id: str = Field(..., alias="modelID", description="模型 ID")
    provider_id: str = Field(..., alias="providerID", description="提供商 ID")

    class Config:
        populate_by_name = True


class Agent(BaseModel):
    """代理配置。"""

    name: str = Field(..., description="代理名称")
    description: Optional[str] = Field(None, description="代理描述")
    mode: Literal["subagent", "primary", "all"] = Field(..., description="代理模式")
    built_in: bool = Field(..., alias="builtIn", description="是否为内置代理")
    top_p: Optional[float] = Field(None, alias="topP", description="Top P 参数")
    temperature: Optional[float] = Field(None, description="温度参数")
    color: Optional[str] = Field(None, description="代理颜色（十六进制）")
    permission: AgentPermission = Field(..., description="权限配置")
    model: Optional[AgentModel] = Field(None, description="模型配置")
    prompt: Optional[str] = Field(None, description="系统提示")
    tools: Dict[str, bool] = Field(..., description="工具可用性")
    options: Dict[str, Any] = Field(default_factory=dict, description="额外选项")
    max_steps: Optional[int] = Field(None, alias="maxSteps", description="最大步骤数")

    class Config:
        populate_by_name = True


# ============================================================================
# Command 模型
# ============================================================================


class Command(BaseModel):
    """命令配置。"""

    name: str = Field(..., description="命令名称")
    description: Optional[str] = Field(None, description="命令描述")
    agent: Optional[str] = Field(None, description="使用的代理")
    model: Optional[str] = Field(None, description="使用的模型")
    template: str = Field(..., description="命令模板")
    subtask: Optional[bool] = Field(None, description="是否为子任务")


# ============================================================================
# Tool 模型
# ============================================================================


class ToolListItem(BaseModel):
    """工具列表项。"""

    id: str = Field(..., description="工具 ID")
    description: str = Field(..., description="工具描述")
    parameters: Any = Field(..., description="工具参数模式")


# ============================================================================
# Path 模型
# ============================================================================


class Path(BaseModel):
    """路径信息。"""

    state: str = Field(..., description="状态路径")
    config: str = Field(..., description="配置路径")
    worktree: str = Field(..., description="工作树路径")
    directory: str = Field(..., description="目录路径")


# ============================================================================
# VCS 模型
# ============================================================================


class VcsInfo(BaseModel):
    """版本控制系统信息。"""

    branch: str = Field(..., description="当前分支")


# ============================================================================
# Project 模型
# ============================================================================


class Project(BaseModel):
    """项目信息。"""

    id: str = Field(..., description="项目 ID")
    worktree: str = Field(..., description="工作树路径")
    vcs_dir: Optional[str] = Field(None, alias="vcsDir", description="VCS 目录")
    vcs: Optional[Literal["git"]] = Field(None, description="VCS 类型")
    time: Dict[str, int] = Field(..., description="时间信息")

    class Config:
        populate_by_name = True


# ============================================================================
# MCP 状态模型
# ============================================================================


class McpStatusConnected(BaseModel):
    """MCP 已连接状态。"""

    status: Literal["connected"] = "connected"


class McpStatusDisabled(BaseModel):
    """MCP 已禁用状态。"""

    status: Literal["disabled"] = "disabled"


class McpStatusFailed(BaseModel):
    """MCP 失败状态。"""

    status: Literal["failed"] = "failed"
    error: str = Field(..., description="错误消息")


class McpStatusNeedsAuth(BaseModel):
    """MCP 需要认证状态。"""

    status: Literal["needs_auth"] = "needs_auth"


class McpStatusNeedsClientRegistration(BaseModel):
    """MCP 需要客户端注册状态。"""

    status: Literal["needs_client_registration"] = "needs_client_registration"
    error: str = Field(..., description="错误消息")


McpStatus = McpStatusConnected | McpStatusDisabled | McpStatusFailed | McpStatusNeedsAuth | McpStatusNeedsClientRegistration


# ============================================================================
# LSP 状态模型
# ============================================================================


class LspStatus(BaseModel):
    """LSP 服务器状态。"""

    id: str = Field(..., description="LSP 服务器 ID")
    name: str = Field(..., description="LSP 服务器名称")
    root: str = Field(..., description="根目录")
    status: Literal["connected", "error"] = Field(..., description="LSP 状态")


# ============================================================================
# Formatter 状态模型
# ============================================================================


class FormatterStatus(BaseModel):
    """格式化器状态。"""

    name: str = Field(..., description="格式化器名称")
    extensions: List[str] = Field(..., description="文件扩展名")
    enabled: bool = Field(..., description="是否启用")


# ============================================================================
# Auth 模型
# ============================================================================


class OAuth(BaseModel):
    """OAuth 认证。"""

    type: Literal["oauth"] = "oauth"
    refresh: str = Field(..., description="刷新令牌")
    access: str = Field(..., description="访问令牌")
    expires: int = Field(..., description="过期时间戳")
    enterprise_url: Optional[str] = Field(None, alias="enterpriseUrl", description="企业 URL")

    class Config:
        populate_by_name = True


class ApiAuth(BaseModel):
    """API 密钥认证。"""

    type: Literal["api"] = "api"
    key: str = Field(..., description="API 密钥")


class WellKnownAuth(BaseModel):
    """已知认证。"""

    type: Literal["wellknown"] = "wellknown"
    key: str = Field(..., description="API 密钥")
    token: str = Field(..., description="令牌")


Auth = OAuth | ApiAuth | WellKnownAuth
