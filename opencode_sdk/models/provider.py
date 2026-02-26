"""提供商和模型数据模型。"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ============================================================================
# 模型配置
# ============================================================================


class ModelCost(BaseModel):
    """模型成本信息。"""

    input: float = Field(..., description="输入成本（每令牌）")
    output: float = Field(..., description="输出成本（每令牌）")
    cache: Dict[str, float] = Field(..., description="缓存成本（读取、写入）")
    experimental_over_200k: Optional[Dict[str, Any]] = Field(
        None, alias="experimentalOver200K", description="超过 200k 上下文的成本"
    )

    class Config:
        populate_by_name = True


class ModelLimit(BaseModel):
    """模型限制。"""

    context: int = Field(..., description="上下文窗口大小")
    output: int = Field(..., description="最大输出令牌数")


class ModelCapabilities(BaseModel):
    """模型能力。"""

    temperature: bool = Field(..., description="支持温度参数")
    reasoning: bool = Field(..., description="支持推理")
    attachment: bool = Field(..., description="支持附件")
    toolcall: bool = Field(..., description="支持工具调用")
    input: Dict[str, bool] = Field(..., description="输入模态")
    output: Dict[str, bool] = Field(..., description="输出模态")


class ModelApi(BaseModel):
    """模型 API 信息。"""

    id: str = Field(..., description="API ID")
    url: str = Field(..., description="API URL")
    npm: str = Field(..., description="NPM 包")


class Model(BaseModel):
    """模型信息。"""

    id: str = Field(..., description="模型 ID")
    provider_id: str = Field(..., alias="providerID", description="提供商 ID")
    api: ModelApi = Field(..., description="API 信息")
    name: str = Field(..., description="模型名称")
    capabilities: ModelCapabilities = Field(..., description="模型能力")
    cost: ModelCost = Field(..., description="成本信息")
    limit: ModelLimit = Field(..., description="限制信息")
    status: Literal["alpha", "beta", "deprecated", "active"] = Field(..., description="模型状态")
    options: Dict[str, Any] = Field(default_factory=dict, description="额外选项")
    headers: Dict[str, str] = Field(default_factory=dict, description="自定义 headers")

    class Config:
        populate_by_name = True


# ============================================================================
# 提供商配置
# ============================================================================


class Provider(BaseModel):
    """提供商信息。"""

    id: str = Field(..., description="提供商 ID")
    name: str = Field(..., description="提供商名称")
    source: Literal["env", "config", "custom", "api"] = Field(..., description="提供商来源")
    env: List[str] = Field(default_factory=list, description="环境变量")
    key: Optional[str] = Field(None, description="API 密钥")
    options: Dict[str, Any] = Field(default_factory=dict, description="提供商选项")
    models: Dict[str, Model] = Field(default_factory=dict, description="可用模型")


class ProviderAuthMethod(BaseModel):
    """提供商认证方法。"""

    type: Literal["oauth", "api"] = Field(..., description="认证类型")
    label: str = Field(..., description="认证标签")


class ProviderAuthAuthorization(BaseModel):
    """提供商 OAuth 授权信息。"""

    url: str = Field(..., description="授权 URL")
    method: Literal["auto", "code"] = Field(..., description="授权方法")
    instructions: str = Field(..., description="授权说明")
