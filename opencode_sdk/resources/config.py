"""
Config 资源模块。

提供配置管理功能，用于查询和更新 OpenCode 配置。
"""

from typing import Dict, Any, List, Optional
from ..models.config import Config
from .base import BaseResource


class ConfigResource(BaseResource):
    """
    Config 资源类。
    
    提供配置管理功能，包括：
    - 获取配置信息
    - 更新配置
    - 列出提供商配置
    """
    
    def get(self) -> Config:
        """
        获取配置信息。
        
        返回当前的 OpenCode 配置。
        
        Returns:
            Config 对象
            
        Example:
            >>> config = client.config.get()
            >>> print(f"默认提供商: {config.default_provider_id}")
            >>> print(f"默认模型: {config.default_model_id}")
        """
        response = self._http_client.get('/config')
        return Config(**response)
    
    def update(self, **kwargs) -> Config:
        """
        更新配置。
        
        更新 OpenCode 配置的一个或多个字段。
        
        Args:
            **kwargs: 要更新的配置字段
                - default_provider_id: 默认提供商 ID
                - default_model_id: 默认模型 ID
                - agent_id: 代理 ID
                - 其他配置字段...
            
        Returns:
            更新后的 Config 对象
            
        Raises:
            BadRequestError: 配置参数无效
            
        Example:
            >>> config = client.config.update(
            ...     default_provider_id="anthropic",
            ...     default_model_id="claude-3-5-sonnet-20241022"
            ... )
            >>> print(f"配置已更新: {config.default_provider_id}")
        """
        response = self._http_client.patch('/config', json_data=kwargs)
        return Config(**response)
    
    def providers(self) -> List[Dict[str, Any]]:
        """
        列出所有提供商配置。
        
        返回所有已配置的 AI 提供商列表。
        
        Returns:
            提供商配置列表
            
        Example:
            >>> providers = client.config.providers()
            >>> for provider in providers:
            ...     print(f"{provider['id']}: {provider['name']}")
        """
        response = self._http_client.get('/config/providers')
        return response
