"""
SSE (Server-Sent Events) 客户端模块。

提供异步事件流处理功能，用于接收服务器推送的实时事件。
"""

import json
import asyncio
from typing import AsyncIterator, Optional, Dict, Any
import httpx
from .models.events import Event
from .exceptions import ConnectionError, TimeoutError, APIError


class SSEClient:
    """
    SSE (Server-Sent Events) 客户端。
    
    用于处理服务器推送的事件流，支持异步迭代。
    """
    
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ):
        """
        初始化 SSE 客户端。
        
        Args:
            base_url: API 基础 URL
            headers: 请求头
            timeout: 超时时间（秒）
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """异步上下文管理器入口。"""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout
        )
        return self
    
    async def __aexit__(self, *args):
        """异步上下文管理器退出。"""
        if self._client:
            await self._client.aclose()
    
    async def connect(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        json_data: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator[Event]:
        """
        连接到 SSE 端点并接收事件流。
        
        Args:
            url: SSE 端点 URL（相对路径）
            params: 查询参数（用于 GET 请求）
            method: HTTP 方法（GET 或 POST）
            json_data: JSON 数据（用于 POST 请求）
            
        Yields:
            Event 对象
            
        Raises:
            ConnectionError: 连接失败
            TimeoutError: 连接超时
            APIError: API 错误
            
        Example:
            >>> async with SSEClient(base_url="http://localhost:8000") as client:
            ...     async for event in client.connect("/global/event"):
            ...         print(f"收到事件: {event.type}")
        """
        if not self._client:
            raise RuntimeError("SSEClient 必须在 async with 语句中使用")
        
        try:
            # 根据方法类型构建请求
            request_kwargs = {
                "headers": {"Accept": "text/event-stream"},
                "timeout": None  # SSE 连接不应该有超时
            }
            
            if method.upper() == "POST":
                request_kwargs["json"] = json_data
            else:
                request_kwargs["params"] = params
            
            
            async with self._client.stream(
                method,
                url,
                **request_kwargs
            ) as response:
                # 检查响应状态
                # 200: 正常响应
                # 204: 无内容（请求成功但没有流式响应）
                if response.status_code == 204:
                    # 204 表示请求成功但没有流式内容，直接返回
                    return
                elif response.status_code != 200:
                    error_text = await response.aread()
                    raise APIError(
                        message=f"SSE 连接失败: {response.status_code}",
                        status_code=response.status_code,
                        response_body=error_text.decode()
                    )
                
                # 处理事件流
                async for event in self._parse_stream(response):
                    yield event
                    
        except httpx.TimeoutException as e:
            raise TimeoutError(f"SSE 连接超时: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"SSE 连接失败: {str(e)}")
        except Exception as e:
            if isinstance(e, (APIError, TimeoutError, ConnectionError)):
                raise
            raise APIError(f"SSE 处理错误: {str(e)}")
    
    async def _parse_stream(self, response: httpx.Response) -> AsyncIterator[Event]:
        """
        解析 SSE 事件流。
        
        Args:
            response: HTTP 响应对象
            
        Yields:
            Event 对象
        """
        event_type: Optional[str] = None
        event_data: str = ""
        
        async for line in response.aiter_lines():
            line = line.strip()
            
            # 空行表示事件结束
            if not line:
                if event_data:
                    # 解析并生成事件（event_type 可能为 None，从 data 中获取）
                    event = self._parse_event(event_type, event_data)
                    if event:
                        yield event
                    
                    # 重置状态
                    event_type = None
                    event_data = ""
                continue
            
            # 解析事件字段
            if line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data:"):
                data = line[5:].strip()
                if event_data:
                    event_data += "\n" + data
                else:
                    event_data = data
            # 忽略其他字段（id, retry 等）
    
    def _parse_event(self, event_type: Optional[str], event_data: str) -> Optional[Event]:
        """
        解析单个事件。
        
        Args:
            event_type: 事件类型（可能为 None，从 data 中获取）
            event_data: 事件数据（JSON 字符串）
            
        Returns:
            Event 对象，如果解析失败则返回 None
        """
        try:
            # 解析 JSON 数据
            data = json.loads(event_data)
            
            # 如果 data 不是字典，返回 None
            if not isinstance(data, dict):
                return None
            
            # 获取事件类型
            if event_type is None:
                event_type = data.get("type")
            
            if not event_type:
                return None
            
            # 根据事件类型导入对应的类
            from .models.events import (
                EventServerConnected,
                EventServerInstanceDisposed,
                EventSessionStatus,
                EventSessionIdle,
                EventSessionCreated,
                EventSessionUpdated,
                EventSessionDeleted,
                EventSessionDiff,
                EventSessionError,
                EventSessionCompacted,
                EventMessageUpdated,
                EventMessageRemoved,
                EventMessagePartUpdated,
                EventMessagePartRemoved,
                EventMessagePartDelta,
                EventPermissionUpdated,
                EventPermissionReplied,
                EventFileEdited,
                EventFileWatcherUpdated,
                EventVcsBranchUpdated,
                EventTodoUpdated,
                EventCommandExecuted,
                EventTuiPromptAppend,
                EventTuiCommandExecute,
                EventTuiToastShow,
                EventPtyCreated,
                EventPtyUpdated,
                EventPtyExited,
                EventPtyDeleted,
                EventInstallationUpdated,
                EventInstallationUpdateAvailable,
                EventLspClientDiagnostics,
                EventLspUpdated,
            )
            
            # 事件类型映射
            event_class_map = {
                "server.connected": EventServerConnected,
                "server.instance.disposed": EventServerInstanceDisposed,
                "session.status": EventSessionStatus,
                "session.idle": EventSessionIdle,
                "session.created": EventSessionCreated,
                "session.updated": EventSessionUpdated,
                "session.deleted": EventSessionDeleted,
                "session.diff": EventSessionDiff,
                "session.error": EventSessionError,
                "session.compacted": EventSessionCompacted,
                "message.updated": EventMessageUpdated,
                "message.removed": EventMessageRemoved,
                "message.part.updated": EventMessagePartUpdated,
                "message.part.removed": EventMessagePartRemoved,
                "message.part.delta": EventMessagePartDelta,
                "permission.updated": EventPermissionUpdated,
                "permission.replied": EventPermissionReplied,
                "file.edited": EventFileEdited,
                "file.watcher.updated": EventFileWatcherUpdated,
                "vcs.branch.updated": EventVcsBranchUpdated,
                "todo.updated": EventTodoUpdated,
                "command.executed": EventCommandExecuted,
                "tui.prompt.append": EventTuiPromptAppend,
                "tui.command.execute": EventTuiCommandExecute,
                "tui.toast.show": EventTuiToastShow,
                "pty.created": EventPtyCreated,
                "pty.updated": EventPtyUpdated,
                "pty.exited": EventPtyExited,
                "pty.deleted": EventPtyDeleted,
                "installation.updated": EventInstallationUpdated,
                "installation.update-available": EventInstallationUpdateAvailable,
                "lsp.client.diagnostics": EventLspClientDiagnostics,
                "lsp.updated": EventLspUpdated,
            }
            
            # 获取对应的事件类
            event_class = event_class_map.get(event_type)
            if event_class:
                return event_class(**data)
            else:
                # 未知事件类型，静默忽略
                return None
            
        except json.JSONDecodeError:
            # JSON 解析失败，静默忽略
            return None
        except Exception:
            # 其他错误，静默忽略
            return None


async def subscribe_events(
    base_url: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None
) -> AsyncIterator[Event]:
    """
    订阅事件流的便捷函数。
    
    Args:
        base_url: API 基础 URL
        url: SSE 端点 URL
        headers: 请求头
        params: 查询参数
        timeout: 超时时间
        
    Yields:
        Event 对象
        
    Example:
        >>> async for event in subscribe_events(
        ...     base_url="http://localhost:8000",
        ...     url="/global/event"
        ... ):
        ...     print(f"收到事件: {event.type}")
    """
    async with SSEClient(base_url, headers, timeout) as client:
        async for event in client.connect(url, params):
            yield event
