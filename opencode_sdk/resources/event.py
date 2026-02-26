"""
Event 资源模块。

提供事件订阅功能，用于接收服务器推送的实时事件。
"""

from typing import AsyncIterator, Optional, Dict, Any
from ..models.events import Event, GlobalEvent
from ..sse_client import SSEClient
from .base import BaseResource


class EventResource(BaseResource):
    """
    Event 资源类。
    
    提供事件订阅功能，支持：
    - 全局事件订阅
    - 会话事件订阅
    - 实时事件流处理
    """
    
    async def subscribe(
        self,
        session_id: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[Event]:
        """
        订阅事件流。
        
        如果提供 session_id，则订阅特定会话的事件；
        否则订阅全局事件。
        
        Args:
            session_id: 可选的会话 ID
            **kwargs: 其他查询参数
            
        Yields:
            Event 对象
            
        Raises:
            ConnectionError: 连接失败
            TimeoutError: 连接超时
            APIError: API 错误
            
        Example:
            >>> # 订阅全局事件
            >>> async for event in client.events.subscribe():
            ...     print(f"全局事件: {event.type}")
            
            >>> # 订阅会话事件
            >>> async for event in client.events.subscribe(session_id="session_123"):
            ...     if event.type == "text":
            ...         print(event.text, end="", flush=True)
        """
        # 构建 URL
        if session_id:
            url = f"/session/{session_id}/prompt_async"
        else:
            url = "/global/event"
        
        # 构建查询参数
        params = dict(kwargs)
        
        # 创建 SSE 客户端
        async with SSEClient(
            base_url=self._http_client.base_url,
            headers=self._http_client.default_headers,
            timeout=self._http_client.timeout
        ) as sse_client:
            async for event in sse_client.connect(url, params):
                yield event
    
    async def subscribe_global(self) -> AsyncIterator[GlobalEvent]:
        """
        订阅全局事件。
        
        这是 subscribe() 的便捷方法，专门用于订阅全局事件。
        
        Yields:
            GlobalEvent 对象
            
        Example:
            >>> async for event in client.events.subscribe_global():
            ...     print(f"全局事件: {event.type}")
            ...     if event.type == "session:created":
            ...         print(f"新会话: {event.info.name}")
        """
        async for event in self.subscribe():
            # 全局事件应该是 GlobalEvent 类型
            if isinstance(event, dict):
                yield GlobalEvent(**event)
            else:
                yield event
    
    async def subscribe_session(
        self,
        session_id: str,
        parts: Optional[list] = None,
        **kwargs
    ) -> AsyncIterator[Event]:
        """
        订阅会话事件（发送消息并接收响应流）。
        
        正确的流程：
        1. 先订阅 /event 端点（SSE 流）
        2. 发送消息到 /session/{id}/prompt_async
        3. 通过 /event 流接收响应
        
        Args:
            session_id: 会话 ID
            parts: 消息部分列表（如果提供，则发送消息）
            **kwargs: 其他参数（如 model, agent 等）
            
        Yields:
            Event 对象
            
        Example:
            >>> async for event in client.events.subscribe_session(
            ...     session_id="session_123",
            ...     parts=[{"type": "text", "text": "你好"}],
            ...     model={"modelID": "minimax-m2.1-free", "providerID": "opencode"},
            ...     agent="build"
            ... ):
            ...     if event.type == "text":
            ...         print(event.text, end="", flush=True)
        """
        # 如果提供了 parts，需要先发送消息
        if parts:
            # 构建请求数据
            data = {"parts": parts}
            data.update(kwargs)
            
            # 先订阅事件流
            url = "/event"
            
            # 使用 SSE 客户端订阅事件
            async with SSEClient(
                base_url=self._http_client.base_url,
                headers=self._http_client.default_headers,
                timeout=self._http_client.timeout
            ) as sse_client:
                # 启动事件流连接
                event_stream = sse_client.connect(url, method="GET")
                
                # 等待第一个事件（server.connected）
                first_event = await event_stream.__anext__()
                yield first_event
                
                # 发送消息到 prompt_async 端点
                prompt_url = f"/session/{session_id}/prompt_async"
                response = self._http_client.post(prompt_url, json_data=data)
                # 204 响应表示消息已接受
                
                # 继续接收事件流
                async for event in event_stream:
                    yield event
                    
                    # 如果收到 session.idle 事件，表示会话完成
                    if hasattr(event, 'type') and event.type == "session.idle":
                        # 检查是否是当前会话
                        if hasattr(event, 'properties') and hasattr(event.properties, 'sessionID'):
                            if event.properties.sessionID == session_id:
                                break
        else:
            # 只订阅事件，不发送消息
            async for event in self.subscribe(session_id=session_id, **kwargs):
                yield event
