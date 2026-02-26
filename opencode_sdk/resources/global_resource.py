"""
Global 资源模块。

提供全局系统管理功能，用于健康检查、全局事件订阅和实例管理。
"""

from typing import Generator, Dict, Any
from .base import BaseResource


class GlobalResource(BaseResource):
    """
    Global 资源类。
    
    提供全局系统管理功能，包括：
    - 健康检查
    - 全局事件订阅
    - 全局实例管理
    """
    
    def health(self) -> Dict[str, Any]:
        """
        获取服务器健康状态。
        
        检查 OpenCode 服务器是否正常运行。
        
        Returns:
            健康状态信息字典，包含：
            - healthy: 是否健康 (True/False)
            - version: 服务器版本号
            
        Example:
            >>> health = client.global_resource.health()
            >>> if health['healthy']:
            ...     print(f"服务器正常运行，版本: {health['version']}")
            ... else:
            ...     print("服务器异常")
        """
        response = self._http_client.get('/global/health')
        return response
    
    def subscribe_events(self) -> Generator[Dict[str, Any], None, None]:
        """
        订阅全局事件流。
        
        订阅来自所有项目实例的全局事件，使用 Server-Sent Events (SSE)。
        
        Yields:
            全局事件字典，包含：
            - directory: 事件来源的目录
            - payload: 事件负载数据
              - type: 事件类型
              - properties: 事件属性
            
        Example:
            >>> # 订阅全局事件
            >>> for event in client.global_resource.subscribe_events():
            ...     directory = event.get('directory')
            ...     payload = event.get('payload', {})
            ...     event_type = payload.get('type')
            ...     print(f"[{directory}] {event_type}")
            ...     
            ...     if event_type == 'server.connected':
            ...         print("服务器已连接")
            ...     elif event_type == 'global.disposed':
            ...         print("全局实例已释放")
            ...         break
        """
        return self._http_client.stream_sse('/global/event')
    
    def dispose(self) -> bool:
        """
        释放所有实例。
        
        清理并释放所有 OpenCode 实例，释放所有资源。
        这将关闭所有打开的项目和会话。
        
        Returns:
            是否成功释放 (True/False)
            
        Warning:
            此操作会关闭所有活动会话和项目，请谨慎使用。
            
        Example:
            >>> # 释放所有实例
            >>> success = client.global_resource.dispose()
            >>> if success:
            ...     print("所有实例已成功释放")
        """
        response = self._http_client.post('/global/dispose')
        return response
