"""配置数据模型。"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


# ============================================================================
# 快捷键配置
# ============================================================================


class KeybindsConfig(BaseModel):
    """自定义快捷键配置。"""

    leader: Optional[str] = Field(None, description="快捷键组合的前导键")
    app_exit: Optional[str] = Field(None, description="退出应用程序")
    editor_open: Optional[str] = Field(None, description="打开外部编辑器")
    theme_list: Optional[str] = Field(None, description="列出可用主题")
    sidebar_toggle: Optional[str] = Field(None, description="切换侧边栏")
    scrollbar_toggle: Optional[str] = Field(None, description="切换会话滚动条")
    username_toggle: Optional[str] = Field(None, description="切换用户名显示")
    status_view: Optional[str] = Field(None, description="查看状态")
    session_export: Optional[str] = Field(None, description="导出会话到编辑器")
    session_new: Optional[str] = Field(None, description="创建新会话")
    session_list: Optional[str] = Field(None, description="列出所有会话")
    # 可以添加更多快捷键配置


# ============================================================================
# Agent 配置
# ============================================================================


class AgentPermission(BaseModel):
    """代理权限配置。"""

    edit: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="编辑权限")
    bash: Optional[Union[Literal["ask", "allow", "deny"], Dict[str, Literal["ask", "allow", "deny"]]]] = Field(
        None, description="Bash 权限"
    )
    webfetch: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="网页抓取权限")
    doom_loop: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="死循环权限")
    external_directory: Optional[Literal["ask", "allow", "deny"]] = Field(
        None, description="外部目录权限"
    )


class AgentConfig(BaseModel):
    """代理配置。"""

    model: Optional[str] = Field(None, description="使用的模型")
    temperature: Optional[float] = Field(None, description="温度参数")
    top_p: Optional[float] = Field(None, description="Top P 参数")
    prompt: Optional[str] = Field(None, description="系统提示")
    tools: Optional[Dict[str, bool]] = Field(None, description="工具可用性")
    disable: Optional[bool] = Field(None, description="禁用代理")
    description: Optional[str] = Field(None, description="何时使用该代理的描述")
    mode: Optional[Literal["subagent", "primary", "all"]] = Field(None, description="代理模式")
    color: Optional[str] = Field(None, description="代理的十六进制颜色代码（例如 #FF5733）")
    max_steps: Optional[int] = Field(
        None,
        alias="maxSteps",
        description="强制纯文本响应前的最大代理迭代次数",
    )
    permission: Optional[AgentPermission] = Field(None, description="权限配置")

    class Config:
        populate_by_name = True
        extra = "allow"  # 允许额外字段


# ============================================================================
# Provider 配置
# ============================================================================


class ProviderModelCost(BaseModel):
    """提供商模型成本配置。"""

    input: float = Field(..., description="输入成本")
    output: float = Field(..., description="输出成本")
    cache_read: Optional[float] = Field(None, description="缓存读取成本")
    cache_write: Optional[float] = Field(None, description="缓存写入成本")
    context_over_200k: Optional[Dict[str, float]] = Field(None, description="超过 200k 上下文的成本")


class ProviderModelLimit(BaseModel):
    """提供商模型限制配置。"""

    context: int = Field(..., description="上下文限制")
    output: int = Field(..., description="输出限制")


class ProviderModelModalities(BaseModel):
    """提供商模型模态配置。"""

    input: List[Literal["text", "audio", "image", "video", "pdf"]] = Field(..., description="输入模态")
    output: List[Literal["text", "audio", "image", "video", "pdf"]] = Field(..., description="输出模态")


class ProviderModelConfig(BaseModel):
    """提供商模型配置。"""

    id: Optional[str] = Field(None, description="模型 ID")
    name: Optional[str] = Field(None, description="模型名称")
    release_date: Optional[str] = Field(None, description="发布日期")
    attachment: Optional[bool] = Field(None, description="支持附件")
    reasoning: Optional[bool] = Field(None, description="支持推理")
    temperature: Optional[bool] = Field(None, description="支持温度参数")
    tool_call: Optional[bool] = Field(None, description="支持工具调用")
    cost: Optional[ProviderModelCost] = Field(None, description="成本配置")
    limit: Optional[ProviderModelLimit] = Field(None, description="限制配置")
    modalities: Optional[ProviderModelModalities] = Field(None, description="模态配置")
    experimental: Optional[bool] = Field(None, description="是否为实验性")
    status: Optional[Literal["alpha", "beta", "deprecated"]] = Field(None, description="模型状态")
    options: Optional[Dict[str, Any]] = Field(None, description="额外选项")
    headers: Optional[Dict[str, str]] = Field(None, description="自定义 headers")
    provider: Optional[Dict[str, str]] = Field(None, description="提供商配置")


class ProviderOptions(BaseModel):
    """提供商选项配置。"""

    api_key: Optional[str] = Field(None, alias="apiKey", description="API 密钥")
    base_url: Optional[str] = Field(None, alias="baseURL", description="基础 URL")
    enterprise_url: Optional[str] = Field(
        None, alias="enterpriseUrl", description="GitHub Enterprise URL（用于 copilot 认证）"
    )
    set_cache_key: Optional[bool] = Field(
        None, alias="setCacheKey", description="为此提供商启用 promptCacheKey（默认 false）"
    )
    timeout: Optional[Union[int, bool]] = Field(
        None,
        description="此提供商请求的超时时间（毫秒）。默认为 300000（5 分钟）。设置为 false 禁用超时。",
    )

    class Config:
        populate_by_name = True
        extra = "allow"  # 允许额外字段


class ProviderConfig(BaseModel):
    """提供商配置。"""

    api: Optional[str] = Field(None, description="API 端点")
    name: Optional[str] = Field(None, description="提供商名称")
    env: Optional[List[str]] = Field(None, description="环境变量")
    id: Optional[str] = Field(None, description="提供商 ID")
    npm: Optional[str] = Field(None, description="NPM 包")
    models: Optional[Dict[str, ProviderModelConfig]] = Field(None, description="模型配置")
    whitelist: Optional[List[str]] = Field(None, description="白名单")
    blacklist: Optional[List[str]] = Field(None, description="黑名单")
    options: Optional[ProviderOptions] = Field(None, description="提供商选项")


# ============================================================================
# MCP 配置
# ============================================================================


class McpLocalConfig(BaseModel):
    """MCP 本地服务器配置。"""

    type: Literal["local"] = "local"
    command: List[str] = Field(..., description="运行 MCP 服务器的命令和参数")
    environment: Optional[Dict[str, str]] = Field(
        None, description="运行 MCP 服务器时设置的环境变量"
    )
    enabled: Optional[bool] = Field(None, description="启动时启用或禁用 MCP 服务器")
    timeout: Optional[int] = Field(
        None,
        description="从 MCP 服务器获取工具的超时时间（毫秒）。如果未指定，默认为 5000（5 秒）。",
    )


class McpOAuthConfig(BaseModel):
    """MCP OAuth 配置。"""

    client_id: Optional[str] = Field(
        None,
        alias="clientId",
        description="OAuth 客户端 ID。如果未提供，将尝试动态客户端注册（RFC 7591）。",
    )
    client_secret: Optional[str] = Field(
        None, alias="clientSecret", description="OAuth 客户端密钥（如果授权服务器需要）"
    )
    scope: Optional[str] = Field(None, description="授权期间请求的 OAuth 范围")

    class Config:
        populate_by_name = True


class McpRemoteConfig(BaseModel):
    """MCP 远程服务器配置。"""

    type: Literal["remote"] = "remote"
    url: str = Field(..., description="远程 MCP 服务器的 URL")
    enabled: Optional[bool] = Field(None, description="启动时启用或禁用 MCP 服务器")
    headers: Optional[Dict[str, str]] = Field(None, description="随请求发送的 headers")
    oauth: Optional[Union[McpOAuthConfig, bool]] = Field(
        None,
        description="MCP 服务器的 OAuth 认证配置。设置为 false 禁用 OAuth 自动检测。",
    )
    timeout: Optional[int] = Field(
        None,
        description="从 MCP 服务器获取工具的超时时间（毫秒）。如果未指定，默认为 5000（5 秒）。",
    )


McpConfig = Union[McpLocalConfig, McpRemoteConfig]


# ============================================================================
# 主配置
# ============================================================================


class TuiScrollAcceleration(BaseModel):
    """TUI 滚动加速配置。"""

    enabled: bool = Field(..., description="启用滚动加速")


class TuiConfig(BaseModel):
    """TUI 特定设置。"""

    scroll_speed: Optional[int] = Field(None, description="TUI 滚动速度")
    scroll_acceleration: Optional[TuiScrollAcceleration] = Field(None, description="滚动加速设置")
    diff_style: Optional[Literal["auto", "stacked"]] = Field(
        None,
        description="控制差异渲染样式：'auto' 适应终端宽度，'stacked' 始终显示单列",
    )


class CommandConfig(BaseModel):
    """命令配置。"""

    template: str = Field(..., description="命令模板")
    description: Optional[str] = Field(None, description="命令描述")
    agent: Optional[str] = Field(None, description="使用的代理")
    model: Optional[str] = Field(None, description="使用的模型")
    subtask: Optional[bool] = Field(None, description="是否为子任务")


class WatcherConfig(BaseModel):
    """监视器配置。"""

    ignore: Optional[List[str]] = Field(None, description="要忽略的模式")


class FormatterConfig(BaseModel):
    """格式化器配置。"""

    disabled: Optional[bool] = Field(None, description="禁用格式化器")
    command: Optional[List[str]] = Field(None, description="格式化器命令")
    environment: Optional[Dict[str, str]] = Field(None, description="环境变量")
    extensions: Optional[List[str]] = Field(None, description="文件扩展名")


class LspConfigDisabled(BaseModel):
    """LSP 禁用配置。"""

    disabled: Literal[True] = True


class LspConfigEnabled(BaseModel):
    """LSP 启用配置。"""

    command: List[str] = Field(..., description="LSP 命令")
    extensions: Optional[List[str]] = Field(None, description="文件扩展名")
    disabled: Optional[bool] = Field(None, description="禁用 LSP")
    env: Optional[Dict[str, str]] = Field(None, description="环境变量")
    initialization: Optional[Dict[str, Any]] = Field(None, description="初始化选项")


LspConfig = Union[LspConfigDisabled, LspConfigEnabled]


class PermissionConfig(BaseModel):
    """权限配置。"""

    edit: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="编辑权限")
    bash: Optional[Union[Literal["ask", "allow", "deny"], Dict[str, Literal["ask", "allow", "deny"]]]] = Field(
        None, description="Bash 权限"
    )
    webfetch: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="网页抓取权限")
    doom_loop: Optional[Literal["ask", "allow", "deny"]] = Field(None, description="死循环权限")
    external_directory: Optional[Literal["ask", "allow", "deny"]] = Field(
        None, description="外部目录权限"
    )


class EnterpriseConfig(BaseModel):
    """企业配置。"""

    url: Optional[str] = Field(None, description="企业 URL")


class ExperimentalHookConfig(BaseModel):
    """实验性钩子配置。"""

    command: List[str] = Field(..., description="要执行的命令")
    environment: Optional[Dict[str, str]] = Field(None, description="环境变量")


class ExperimentalConfig(BaseModel):
    """实验性配置。"""

    hook: Optional[Dict[str, Any]] = Field(None, description="钩子配置")
    chat_max_retries: Optional[int] = Field(
        None, alias="chatMaxRetries", description="聊天完成失败时的重试次数"
    )
    disable_paste_summary: Optional[bool] = Field(None, description="禁用粘贴摘要")
    batch_tool: Optional[bool] = Field(None, description="启用批处理工具")
    open_telemetry: Optional[bool] = Field(
        None,
        alias="openTelemetry",
        description="为 AI SDK 调用启用 OpenTelemetry spans（使用 'experimental_telemetry' 标志）",
    )
    primary_tools: Optional[List[str]] = Field(
        None, description="仅对主代理可用的工具。"
    )

    class Config:
        populate_by_name = True


class Config(BaseModel):
    """主配置模型。"""

    schema_: Optional[str] = Field(None, alias="$schema", description="配置验证的 JSON schema 引用")
    theme: Optional[str] = Field(None, description="界面使用的主题名称")
    keybinds: Optional[KeybindsConfig] = Field(None, description="快捷键配置")
    log_level: Optional[Literal["DEBUG", "INFO", "WARN", "ERROR"]] = Field(None, alias="logLevel", description="日志级别")
    tui: Optional[TuiConfig] = Field(None, description="TUI 特定设置")
    command: Optional[Dict[str, CommandConfig]] = Field(None, description="命令配置")
    watcher: Optional[WatcherConfig] = Field(None, description="监视器配置")
    plugin: Optional[List[str]] = Field(None, description="插件列表")
    snapshot: Optional[bool] = Field(None, description="启用快照")
    share: Optional[Literal["manual", "auto", "disabled"]] = Field(
        None,
        description="控制分享行为：'manual' 允许通过命令手动分享，'auto' 启用自动分享，'disabled' 禁用所有分享",
    )
    autoshare: Optional[bool] = Field(None, description="已弃用：使用 'share' 字段代替。自动分享新创建的会话")
    autoupdate: Optional[Union[bool, Literal["notify"]]] = Field(
        None,
        description="自动更新到最新版本。设置为 true 自动更新，false 禁用，或 'notify' 显示更新通知",
    )
    disabled_providers: Optional[List[str]] = Field(None, description="禁用自动加载的提供商")
    enabled_providers: Optional[List[str]] = Field(
        None, description="设置后，仅启用这些提供商。所有其他提供商将被忽略"
    )
    model: Optional[str] = Field(None, description="使用的模型，格式为 provider/model，例如 anthropic/claude-2")
    small_model: Optional[str] = Field(
        None, description="用于标题生成等任务的小模型，格式为 provider/model"
    )
    username: Optional[str] = Field(None, description="在对话中显示的自定义用户名，而不是系统用户名")
    mode: Optional[Dict[str, AgentConfig]] = Field(None, description="已弃用：使用 `agent` 字段代替。")
    agent: Optional[Dict[str, AgentConfig]] = Field(None, description="代理配置")
    provider: Optional[Dict[str, ProviderConfig]] = Field(None, description="自定义提供商配置和模型覆盖")
    mcp: Optional[Dict[str, McpConfig]] = Field(None, description="MCP（模型上下文协议）服务器配置")
    formatter: Optional[Union[bool, Dict[str, FormatterConfig]]] = Field(None, description="格式化器配置")
    lsp: Optional[Union[bool, Dict[str, LspConfig]]] = Field(None, description="LSP 配置")
    instructions: Optional[List[str]] = Field(None, description="要包含的额外指令文件或模式")
    layout: Optional[Literal["auto", "stretch"]] = Field(None, description="已弃用：始终使用拉伸布局。")
    permission: Optional[PermissionConfig] = Field(None, description="权限配置")
    tools: Optional[Dict[str, bool]] = Field(None, description="工具可用性")
    enterprise: Optional[EnterpriseConfig] = Field(None, description="企业配置")
    experimental: Optional[ExperimentalConfig] = Field(None, description="实验性配置")

    class Config:
        populate_by_name = True
        extra = "allow"  # 允许额外字段
