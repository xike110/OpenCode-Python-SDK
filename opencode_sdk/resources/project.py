"""
Project 资源模块。

提供项目管理功能，用于查询和管理 OpenCode 项目。
"""

from typing import List, Optional
from .base import BaseResource


class ProjectResource(BaseResource):
    """
    Project 资源类。
    
    提供项目管理功能，包括：
    - 列出所有项目
    - 获取当前项目信息
    - 更新项目属性
    """
    
    def list(self, directory: Optional[str] = None) -> List[dict]:
        """
        列出所有项目。
        
        返回已在 OpenCode 中打开的所有项目列表。
        
        Args:
            directory: 可选的目录路径，用于过滤特定目录的项目
            
        Returns:
            项目列表，每个项目是一个字典
            
        Example:
            >>> projects = client.projects.list()
            >>> for project in projects:
            ...     print(f"{project['name']}: {project['path']}")
        """
        params = {}
        if directory:
            params['directory'] = directory
            
        response = self._http_client.get('/project', params=params)
        return response
    
    def current(self, directory: Optional[str] = None) -> dict:
        """
        获取当前项目信息。
        
        返回当前正在使用的项目信息。
        
        Args:
            directory: 可选的目录路径
            
        Returns:
            当前项目信息字典
            
        Raises:
            NotFoundError: 项目不存在
            
        Example:
            >>> project = client.projects.current()
            >>> print(f"当前项目: {project['name']}")
            >>> print(f"路径: {project['path']}")
        """
        params = {}
        if directory:
            params['directory'] = directory
            
        response = self._http_client.get('/project/current', params=params)
        return response
    
    def update(
        self,
        project_id: str,
        name: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None
    ) -> dict:
        """
        更新项目属性。
        
        更新项目的名称、图标或颜色等属性。
        
        Args:
            project_id: 项目 ID
            name: 可选的新项目名称
            icon: 可选的新项目图标
            color: 可选的新项目颜色
            
        Returns:
            更新后的项目信息字典
            
        Raises:
            NotFoundError: 项目不存在
            BadRequestError: 参数无效
            
        Example:
            >>> # 更新项目名称
            >>> project = client.projects.update(
            ...     project_id="proj_123",
            ...     name="新项目名称"
            ... )
            
            >>> # 更新项目图标和颜色
            >>> project = client.projects.update(
            ...     project_id="proj_123",
            ...     icon="🚀",
            ...     color="#FF5733"
            ... )
        """
        data = {}
        if name is not None:
            data['name'] = name
        if icon is not None:
            data['icon'] = icon
        if color is not None:
            data['color'] = color
        
        if not data:
            raise ValueError("至少需要提供一个更新参数 (name, icon, color)")
        
        response = self._http_client.patch(f'/project/{project_id}', json_data=data)
        return response
