"""
Formatter 资源模块。

提供代码格式化器状态查询功能。
"""

from typing import List, Dict, Any
from .base import BaseResource


class FormatterResource(BaseResource):
    """
    Formatter 资源类。
    
    提供代码格式化器状态查询功能。
    """
    
    def status(self) -> List[Dict[str, Any]]:
        """
        获取格式化器状态。
        
        检索所有已配置的代码格式化器的状态信息。
        
        Returns:
            格式化器状态列表，每个格式化器包含：
            - name: 格式化器名称
            - status: 状态信息
            - languages: 支持的语言列表
            
        Example:
            >>> formatters = client.formatter.status()
            >>> for fmt in formatters:
            ...     print(f"{fmt['name']}: {fmt['status']}")
            ...     print(f"支持语言: {', '.join(fmt.get('languages', []))}")
        """
        response = self._http_client.get('/formatter')
        return response
