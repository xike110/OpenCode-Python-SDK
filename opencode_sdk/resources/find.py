"""
Find 资源模块。

提供搜索功能，包括文本搜索、文件搜索和符号搜索。
"""

from typing import List, Optional, Dict, Any
from .base import BaseResource


class FindResource(BaseResource):
    """
    Find 资源类。
    
    提供搜索功能，包括：
    - 在文件中搜索文本
    - 搜索文件名
    - 搜索工作区符号
    """
    
    def text(
        self,
        query: str,
        path: Optional[str] = None,
        case_sensitive: bool = False,
        whole_word: bool = False,
        regex: bool = False,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        在文件中搜索文本。
        
        Args:
            query: 搜索查询字符串
            path: 可选的搜索路径（限制搜索范围）
            case_sensitive: 是否区分大小写
            whole_word: 是否匹配整个单词
            regex: 是否使用正则表达式
            max_results: 最大结果数量
            
        Returns:
            搜索结果列表，每个结果包含文件路径、行号、匹配内容等
            
        Example:
            >>> # 搜索文本
            >>> results = client.find.text("TODO")
            >>> for result in results:
            ...     print(f"{result['path']}:{result['line']}: {result['text']}")
            
            >>> # 使用正则表达式搜索
            >>> results = client.find.text(r"function\s+\w+", regex=True)
        """
        params: Dict[str, Any] = {'query': query}
        if path:
            params['path'] = path
        if case_sensitive:
            params['caseSensitive'] = True
        if whole_word:
            params['wholeWord'] = True
        if regex:
            params['regex'] = True
        if max_results is not None:
            params['maxResults'] = max_results
            
        response = self._http_client.get('/find/text', params=params)
        return response
    
    def files(
        self,
        query: str,
        path: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索文件名。
        
        Args:
            query: 文件名搜索查询（支持模糊匹配）
            path: 可选的搜索路径
            max_results: 最大结果数量
            
        Returns:
            匹配的文件列表
            
        Example:
            >>> # 搜索文件
            >>> files = client.find.files("*.py")
            >>> for file in files:
            ...     print(file['path'])
            
            >>> # 模糊搜索
            >>> files = client.find.files("readme")
        """
        params: Dict[str, Any] = {'query': query}
        if path:
            params['path'] = path
        if max_results is not None:
            params['maxResults'] = max_results
            
        response = self._http_client.get('/find/files', params=params)
        return response
    
    def symbols(
        self,
        query: str,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索工作区符号。
        
        搜索代码中的符号（函数、类、变量等）。
        
        Args:
            query: 符号名称搜索查询
            max_results: 最大结果数量
            
        Returns:
            符号列表，每个符号包含名称、类型、位置等信息
            
        Example:
            >>> # 搜索函数
            >>> symbols = client.find.symbols("main")
            >>> for symbol in symbols:
            ...     print(f"{symbol['name']} ({symbol['kind']}) in {symbol['path']}")
        """
        params: Dict[str, Any] = {'query': query}
        if max_results is not None:
            params['maxResults'] = max_results
            
        response = self._http_client.get('/find/symbols', params=params)
        return response
