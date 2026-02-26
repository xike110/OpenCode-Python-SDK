"""
Instance 资源模块。

提供实例管理功能。
"""

from typing import Dict, Any
from .base import BaseResource


class InstanceResource(BaseResource):
    """
    Instance 资源类。
    
    提供 OpenCode 实例管理功能。
    """
    
    def dispose(self) -> bool:
        """
        释放当前实例。
        
        清理并释放当前 OpenCode 实例，释放所有资源。
        
        Returns:
            是否成功释放
            
        Warning:
            此操作会关闭当前实例的所有会话和资源，请谨慎使用。
            
        Example:
            >>> # 释放当前实例
            >>> success = client.instance.dispose()
            >>> if success:
            ...     print("实例已成功释放")
        """
        response = self._http_client.post('/instance/dispose')
        return response
