"""
File 资源模块。

提供文件操作功能，包括列出文件、读取文件和获取文件状态。
"""

from typing import List, Optional, Dict, Any
from ..models.file import FileNode, FileContent
from .base import BaseResource


class FileResource(BaseResource):
    """
    File 资源类。
    
    提供文件操作功能，包括：
    - 列出文件和目录
    - 读取文件内容
    - 获取文件状态
    """
    
    def list(
        self,
        path: str = ".",
        recursive: bool = False,
        max_depth: Optional[int] = None
    ) -> List[FileNode]:
        """
        列出文件和目录。
        
        Args:
            path: 目录路径（默认为当前目录）
            recursive: 是否递归列出子目录
            max_depth: 最大递归深度
            
        Returns:
            FileNode 对象列表
            
        Example:
            >>> # 列出当前目录
            >>> files = client.files.list()
            >>> for file in files:
            ...     print(f"{file.name} ({'dir' if file.is_directory else 'file'})")
            
            >>> # 递归列出所有文件
            >>> files = client.files.list(recursive=True, max_depth=3)
        """
        params: Dict[str, Any] = {'path': path}
        if recursive:
            params['recursive'] = True
        if max_depth is not None:
            params['maxDepth'] = max_depth
            
        response = self._http_client.get('/file', params=params)
        return [FileNode(**item) for item in response]
    
    def read(
        self,
        path: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None
    ) -> FileContent:
        """
        读取文件内容。
        
        Args:
            path: 文件路径
            start_line: 起始行号（可选）
            end_line: 结束行号（可选）
            
        Returns:
            FileContent 对象
            
        Raises:
            NotFoundError: 文件不存在
            BadRequestError: 文件无法读取
            
        Example:
            >>> # 读取整个文件
            >>> content = client.files.read("README.md")
            >>> print(content.content)
            
            >>> # 读取指定行
            >>> content = client.files.read("README.md", start_line=1, end_line=10)
        """
        params: Dict[str, Any] = {'path': path}
        if start_line is not None:
            params['startLine'] = start_line
        if end_line is not None:
            params['endLine'] = end_line
            
        response = self._http_client.get('/file/read', params=params)
        return FileContent(**response)
    
    def status(self) -> Dict[str, Any]:
        """
        获取文件状态。
        
        返回文件系统的状态信息，如修改的文件、未跟踪的文件等。
        
        Returns:
            文件状态字典
            
        Example:
            >>> status = client.files.status()
            >>> print(f"修改的文件: {len(status.get('modified', []))}")
            >>> print(f"未跟踪的文件: {len(status.get('untracked', []))}")
        """
        response = self._http_client.get('/file/status')
        return response
