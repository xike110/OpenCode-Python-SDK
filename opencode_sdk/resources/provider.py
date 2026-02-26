"""
Provider 资源模块。

提供 AI 提供商管理功能，包括列出提供商、获取认证方法和 OAuth 认证。
"""

from typing import List, Dict, Any, Optional
from ..models.provider import Provider, ProviderAuthMethod
from .base import BaseResource


class OAuthResource(BaseResource):
    """
    OAuth 认证资源类。
    
    处理提供商的 OAuth 认证流程。
    """
    
    def authorize(self, provider_id: str) -> Dict[str, Any]:
        """
        启动 OAuth 授权流程。
        
        Args:
            provider_id: 提供商 ID
            
        Returns:
            包含授权 URL 的字典
            
        Raises:
            NotFoundError: 提供商不存在
            BadRequestError: 提供商不支持 OAuth
            
        Example:
            >>> result = client.providers.oauth.authorize("github")
            >>> print(f"请访问: {result['url']}")
        """
        response = self._http_client.post(f'/provider/{provider_id}/oauth/authorize')
        return response
    
    def callback(self, provider_id: str, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        处理 OAuth 回调。
        
        Args:
            provider_id: 提供商 ID
            code: 授权码
            state: 可选的状态参数
            
        Returns:
            认证结果字典
            
        Raises:
            NotFoundError: 提供商不存在
            BadRequestError: 授权码无效
            
        Example:
            >>> result = client.providers.oauth.callback(
            ...     "github",
            ...     code="auth_code_123"
            ... )
            >>> print(f"认证成功: {result['success']}")
        """
        data = {'code': code}
        if state:
            data['state'] = state
            
        response = self._http_client.post(
            f'/provider/{provider_id}/oauth/callback',
            json_data=data
        )
        return response


class ProviderResource(BaseResource):
    """
    Provider 资源类。
    
    提供 AI 提供商管理功能，包括：
    - 列出所有提供商
    - 获取认证方法
    - OAuth 认证
    """
    
    def __init__(self, http_client):
        """
        初始化 Provider 资源。
        
        Args:
            http_client: HTTP 客户端实例
        """
        super().__init__(http_client)
        self.oauth = OAuthResource(http_client)
    
    def list(self) -> List[Provider]:
        """
        列出所有提供商。
        
        返回所有可用的 AI 提供商列表。
        
        Returns:
            Provider 对象列表
            
        Example:
            >>> providers = client.providers.list()
            >>> for provider in providers:
            ...     print(f"{provider.id}: {provider.name}")
            ...     for model in provider.models:
            ...         print(f"  - {model.id}")
        """
        response = self._http_client.get('/provider')
        return [Provider(**item) for item in response]
    
    def auth(self) -> Dict[str, List[ProviderAuthMethod]]:
        """
        获取提供商认证方法。
        
        返回所有提供商支持的认证方法。
        
        Returns:
            字典，键为提供商 ID，值为认证方法列表
            
        Example:
            >>> auth_methods = client.providers.auth()
            >>> for provider_id, methods in auth_methods.items():
            ...     print(f"{provider_id}:")
            ...     for method in methods:
            ...         print(f"  - {method.type}")
        """
        response = self._http_client.get('/provider/auth')
        
        # 转换为 ProviderAuthMethod 对象
        result = {}
        for provider_id, methods in response.items():
            result[provider_id] = [
                ProviderAuthMethod(**method) for method in methods
            ]
        
        return result
