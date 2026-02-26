"""
Auth 资源模块。

提供认证凭据管理功能。
"""

from typing import Dict, Any
from .base import BaseResource


class AuthResource(BaseResource):
    """
    Auth 资源类。
    
    提供认证凭据管理功能。
    """
    
    def set(self, provider_id: str, credentials: Dict[str, Any]) -> bool:
        """
        设置认证凭据。
        
        为指定的提供商设置认证凭据。
        
        Args:
            provider_id: 提供商 ID
            credentials: 认证凭据字典，可能包含：
                - api_key: API 密钥
                - access_token: 访问令牌
                - refresh_token: 刷新令牌
                - 其他提供商特定的凭据
            
        Returns:
            是否成功设置
            
        Raises:
            BadRequestError: 凭据格式无效
            
        Example:
            >>> # 设置 API 密钥
            >>> success = client.auth.set(
            ...     provider_id="anthropic",
            ...     credentials={"api_key": "sk-ant-..."}
            ... )
            >>> if success:
            ...     print("认证凭据已设置")
            
            >>> # 设置 OAuth 令牌
            >>> success = client.auth.set(
            ...     provider_id="github",
            ...     credentials={
            ...         "access_token": "gho_...",
            ...         "refresh_token": "ghr_..."
            ...     }
            ... )
        """
        response = self._http_client.put(
            f'/auth/{provider_id}',
            json_data=credentials
        )
        return response
