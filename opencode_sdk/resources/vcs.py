"""
VCS 资源模块。

提供版本控制系统信息查询功能。
"""

from typing import Dict, Any, Optional
from .base import BaseResource


class VcsResource(BaseResource):
    """
    VCS 资源类。
    
    提供版本控制系统（VCS）信息查询功能，如 git 分支信息。
    """
    
    def get(self) -> Dict[str, Optional[str]]:
        """
        获取 VCS 信息。
        
        检索当前项目的版本控制系统信息，如 git 分支。
        
        Returns:
            VCS 信息字典，包含：
            - branch: 当前 git 分支名称（如果有）
            
        Example:
            >>> vcs_info = client.vcs.get()
            >>> if vcs_info['branch']:
            ...     print(f"当前分支: {vcs_info['branch']}")
            ... else:
            ...     print("不在 git 仓库中")
        """
        response = self._http_client.get('/vcs')
        return response
