"""
Path 资源模块。

提供路径信息查询功能。
"""

from typing import Dict, Any
from .base import BaseResource


class PathResource(BaseResource):
    """
    Path 资源类。
    
    提供路径信息查询功能。
    """
    
    def get(self) -> Dict[str, str]:
        """
        获取路径信息。
        
        检索当前工作目录和相关路径信息。
        
        Returns:
            路径信息字典，包含：
            - home: 用户主目录
            - state: 状态目录
            - config: 配置目录
            - worktree: 工作树目录
            - directory: 当前目录
            
        Example:
            >>> paths = client.path.get()
            >>> print(f"主目录: {paths['home']}")
            >>> print(f"配置目录: {paths['config']}")
            >>> print(f"当前目录: {paths['directory']}")
        """
        response = self._http_client.get('/path')
        return response
