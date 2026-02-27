"""
Session 资源模块。

提供会话管理的所有 API 方法，包括创建、查询、更新、删除会话，
以及消息交互、命令执行、版本控制等功能。
"""

from typing import List, Dict, Any, Optional, AsyncIterator
from ..models.session import Session, SessionStatus, SessionSummary
from ..models.message import Message, Part
from ..models.common import FileDiff, Todo
from ..models.events import Event
from .base import BaseResource


class SessionResource(BaseResource):
    """
    Session 资源类。
    
    提供会话管理的完整功能，包括：
    - 基础 CRUD 操作（创建、读取、更新、删除）
    - 消息交互（发送消息、获取消息列表）
    - 命令执行（执行命令、Shell 命令）
    - 版本控制（回退、恢复）
    - 会话管理（分享、分叉、中止）
    - 状态查询（状态、差异、待办事项）
    """
    
    # ==================== 基础 CRUD 操作 ====================
    
    def list(self, directory: Optional[str] = None) -> List[Session]:
        """
        列出所有会话。
        
        Args:
            directory: 可选的目录路径，用于过滤特定目录的会话
            
        Returns:
            会话列表
            
        Example:
            >>> sessions = client.sessions.list()
            >>> for session in sessions:
            ...     print(f"{session.id}: {session.name}")
        """
        params = {}
        if directory:
            params['directory'] = directory
            
        response = self._http_client.get('/session', params=params)
        return [Session(**item) for item in response]
    
    def create(
        self,
        title: Optional[str] = None,
        directory: Optional[str] = None,
        parent_id: Optional[str] = None,
        permission: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Session:
        """
        创建新会话。
        
        Args:
            title: 会话标题
            directory: 项目目录（作为查询参数，用于指定项目）
            parent_id: 父会话 ID（用于创建子会话）
            permission: 权限规则集
            **kwargs: 其他可选参数
            
        Returns:
            创建的会话对象
            
        Example:
            >>> # 创建普通会话
            >>> session = client.sessions.create(title="新会话")
            
            >>> # 在指定目录创建会话（自动创建项目）
            >>> session = client.sessions.create(
            ...     title="新会话",
            ...     directory="/path/to/project"
            ... )
            
            >>> # 创建子会话
            >>> child_session = client.sessions.create(
            ...     title="子会话",
            ...     parent_id="ses_parent_id"
            ... )
        """
        # 构建查询参数
        params = {}
        if directory:
            params['directory'] = directory
        
        # 构建请求体
        data = {}
        if title:
            data['title'] = title
        if parent_id:
            data['parentID'] = parent_id
        if permission:
            data['permission'] = permission
        data.update(kwargs)
        
        response = self._http_client.post('/session', params=params, json_data=data)
        return Session(**response)
    
    def get(self, session_id: str) -> Session:
        """
        获取会话详情。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            会话对象
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> session = client.sessions.get("session_123")
            >>> print(session.name)
        """
        response = self._http_client.get(f'/session/{session_id}')
        return Session(**response)
    
    def delete(self, session_id: str) -> None:
        """
        删除会话及其所有数据。
        
        Args:
            session_id: 会话 ID
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> client.sessions.delete("session_123")
        """
        self._http_client.delete(f'/session/{session_id}')
    
    def update(self, session_id: str, **kwargs) -> Session:
        """
        更新会话属性。
        
        Args:
            session_id: 会话 ID
            **kwargs: 要更新的属性（name, providerId, modelId 等）
            
        Returns:
            更新后的会话对象
            
        Raises:
            NotFoundError: 会话不存在
            BadRequestError: 参数无效
            
        Example:
            >>> session = client.sessions.update(
            ...     "session_123",
            ...     name="新名称",
            ...     modelId="claude-3-5-sonnet-20241022"
            ... )
        """
        response = self._http_client.patch(f'/session/{session_id}', json_data=kwargs)
        return Session(**response)
    
    # ==================== 状态和消息 ====================
    
    def status(self, session_id: Optional[str] = None) -> Dict[str, SessionStatus]:
        """
        获取会话状态。
        
        Args:
            session_id: 可选的会话 ID，如果不提供则返回所有会话的状态
            
        Returns:
            会话状态字典，键为会话 ID，值为状态对象
            
        Example:
            >>> # 获取所有会话状态
            >>> statuses = client.sessions.status()
            >>> 
            >>> # 获取特定会话状态
            >>> status = client.sessions.status("session_123")
        """
        params = {}
        if session_id:
            params['sessionId'] = session_id
            
        response = self._http_client.get('/session/status', params=params)
        return {k: SessionStatus(**v) for k, v in response.items()}
    
    def messages(
        self,
        session_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Message]:
        """
        获取会话的消息列表。
        
        Args:
            session_id: 会话 ID
            limit: 限制返回的消息数量
            offset: 偏移量，用于分页
            
        Returns:
            消息列表
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> messages = client.sessions.messages("session_123", limit=10)
            >>> for msg in messages:
            ...     print(f"{msg.role}: {msg.parts[0].text}")
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
            
        response = self._http_client.get(f'/session/{session_id}/message', params=params)
        
        from ..models.message import UserMessage, AssistantMessage
        
        messages = []
        for item in response:
            role = item.get('role')
            if role == 'user':
                messages.append(UserMessage(**item))
            elif role == 'assistant':
                messages.append(AssistantMessage(**item))
            else:
                messages.append(Message(**item))
        return messages
    
    def message(self, session_id: str, message_id: str) -> Message:
        """
        获取单条消息。
        
        Args:
            session_id: 会话 ID
            message_id: 消息 ID
            
        Returns:
            消息对象
            
        Raises:
            NotFoundError: 会话或消息不存在
            
        Example:
            >>> message = client.sessions.message("session_123", "msg_456")
            >>> print(message.parts[0].text)
        """
        response = self._http_client.get(f'/session/{session_id}/message/{message_id}')
        
        from ..models.message import UserMessage, AssistantMessage
        
        role = response.get('role')
        if role == 'user':
            return UserMessage(**response)
        elif role == 'assistant':
            return AssistantMessage(**response)
        else:
            return Message(**response)
    
    # ==================== 交互操作 ====================
    
    def prompt(
        self,
        session_id: str,
        parts: List[Dict[str, Any]],
        **kwargs
    ) -> Message:
        """
        发送消息到会话（同步）。
        
        此方法会等待 AI 完成响应后返回。
        
        Args:
            session_id: 会话 ID
            parts: 消息部分列表，每个部分是一个字典
            **kwargs: 其他可选参数
            
        Returns:
            AI 的响应消息
            
        Raises:
            NotFoundError: 会话不存在
            BadRequestError: 参数无效
            MessageAbortedError: 消息被中止
            
        Example:
            >>> response = client.sessions.prompt(
            ...     "session_123",
            ...     parts=[{"type": "text", "text": "你好"}]
            ... )
            >>> print(response.parts[0].text)
        """
        data = {'parts': parts}
        data.update(kwargs)
        
        response = self._http_client.post(f'/session/{session_id}/message', json_data=data)
        
        if isinstance(response, dict) and 'info' in response and 'parts' in response:
            message_data = {**response['info'], 'parts': response['parts']}
        else:
            message_data = response
        
        from ..models.message import UserMessage, AssistantMessage
        
        role = message_data.get('role')
        if role == 'user':
            return UserMessage(**message_data)
        elif role == 'assistant':
            return AssistantMessage(**message_data)
        else:
            return Message(**message_data)
    
    async def prompt_async(
        self,
        session_id: str,
        parts: List[Dict[str, Any]],
        **kwargs
    ) -> AsyncIterator[Event]:
        """
        发送消息到会话（异步流式）。
        
        此方法立即返回，通过事件流接收 AI 的响应。
        
        Args:
            session_id: 会话 ID
            parts: 消息部分列表
            **kwargs: 其他可选参数
            
        Yields:
            事件对象，包含 AI 响应的各个部分
            
        Raises:
            NotFoundError: 会话不存在
            BadRequestError: 参数无效
            
        Example:
            >>> async for event in client.sessions.prompt_async(
            ...     "session_123",
            ...     parts=[{"type": "text", "text": "你好"}]
            ... ):
            ...     if event.type == "text":
            ...         print(event.text, end="", flush=True)
        """
        # 使用 Event 资源的 subscribe_session 方法
        from .event import EventResource
        event_resource = EventResource(self._http_client)
        
        async for event in event_resource.subscribe_session(
            session_id=session_id,
            parts=parts,
            **kwargs
        ):
            yield event
    
    def command(
        self,
        session_id: str,
        name: str,
        args: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        执行命令。
        
        Args:
            session_id: 会话 ID
            name: 命令名称
            args: 命令参数
            
        Returns:
            命令执行结果消息
            
        Raises:
            NotFoundError: 会话不存在
            BadRequestError: 命令无效
            
        Example:
            >>> result = client.sessions.command(
            ...     "session_123",
            ...     name="search",
            ...     args={"query": "TODO"}
            ... )
        """
        data = {'name': name}
        if args:
            data['args'] = args
            
        response = self._http_client.post(f'/session/{session_id}/command', json_data=data)
        
        from ..models.message import UserMessage, AssistantMessage
        
        role = response.get('role')
        if role == 'user':
            return UserMessage(**response)
        elif role == 'assistant':
            return AssistantMessage(**response)
        else:
            return Message(**response)
    
    def shell(self, session_id: str, command: str) -> Message:
        """
        执行 Shell 命令。
        
        Args:
            session_id: 会话 ID
            command: Shell 命令字符串
            
        Returns:
            命令执行结果消息
            
        Raises:
            NotFoundError: 会话不存在
            BadRequestError: 命令无效
            
        Example:
            >>> result = client.sessions.shell(
            ...     "session_123",
            ...     command="ls -la"
            ... )
            >>> print(result.parts[0].text)
        """
        data = {'command': command}
        response = self._http_client.post(f'/session/{session_id}/shell', json_data=data)
        
        from ..models.message import UserMessage, AssistantMessage
        
        role = response.get('role')
        if role == 'user':
            return UserMessage(**response)
        elif role == 'assistant':
            return AssistantMessage(**response)
        else:
            return Message(**response)
    
    def abort(self, session_id: str) -> None:
        """
        中止会话。
        
        停止当前正在执行的操作。
        
        Args:
            session_id: 会话 ID
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> client.sessions.abort("session_123")
        """
        self._http_client.post(f'/session/{session_id}/abort')
    
    # ==================== 分享和协作 ====================
    
    def share(self, session_id: str) -> Session:
        """
        分享会话。
        
        生成分享链接，允许其他人查看会话。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            更新后的会话对象（包含分享信息）
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> session = client.sessions.share("session_123")
            >>> print(f"分享链接: {session.share_url}")
        """
        response = self._http_client.post(f'/session/{session_id}/share')
        return Session(**response)
    
    def unshare(self, session_id: str) -> Session:
        """
        取消分享会话。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            更新后的会话对象
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> session = client.sessions.unshare("session_123")
        """
        response = self._http_client.delete(f'/session/{session_id}/share')
        return Session(**response)
    
    # ==================== 差异和总结 ====================
    
    def diff(self, session_id: str) -> List[FileDiff]:
        """
        获取会话的文件差异。
        
        返回会话中所有文件的修改差异。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            文件差异列表
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> diffs = client.sessions.diff("session_123")
            >>> for diff in diffs:
            ...     print(f"{diff.path}: +{diff.additions} -{diff.deletions}")
        """
        response = self._http_client.get(f'/session/{session_id}/diff')
        return [FileDiff(**item) for item in response]
    
    def summarize(self, session_id: str) -> SessionSummary:
        """
        总结会话。
        
        生成会话的摘要信息。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            会话摘要对象
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> summary = client.sessions.summarize("session_123")
            >>> print(summary.summary)
        """
        response = self._http_client.post(f'/session/{session_id}/summarize')
        return SessionSummary(**response)
    
    # ==================== 版本控制 ====================
    
    def revert(self, session_id: str, message_id: str) -> Session:
        """
        回退到指定消息。
        
        将会话状态回退到指定消息之前的状态。
        
        Args:
            session_id: 会话 ID
            message_id: 要回退到的消息 ID
            
        Returns:
            更新后的会话对象
            
        Raises:
            NotFoundError: 会话或消息不存在
            
        Example:
            >>> session = client.sessions.revert("session_123", "msg_456")
        """
        data = {'messageId': message_id}
        response = self._http_client.post(f'/session/{session_id}/revert', json_data=data)
        return Session(**response)
    
    def unrevert(self, session_id: str) -> Session:
        """
        恢复所有回退的消息。
        
        取消之前的回退操作，恢复到最新状态。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            更新后的会话对象
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> session = client.sessions.unrevert("session_123")
        """
        response = self._http_client.post(f'/session/{session_id}/unrevert')
        return Session(**response)
    
    # ==================== 关系和层级 ====================
    
    def children(self, session_id: str) -> List[Session]:
        """
        获取子会话列表。
        
        返回从当前会话分叉出的所有子会话。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            子会话列表
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> children = client.sessions.children("session_123")
            >>> for child in children:
            ...     print(f"子会话: {child.name}")
        """
        response = self._http_client.get(f'/session/{session_id}/children')
        return [Session(**item) for item in response]
    
    def todo(self, session_id: str) -> List[Todo]:
        """
        获取待办事项列表。
        
        返回会话中标记的所有待办事项。
        
        Args:
            session_id: 会话 ID
            
        Returns:
            待办事项列表
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> todos = client.sessions.todo("session_123")
            >>> for todo in todos:
            ...     print(f"[ ] {todo.text}")
        """
        response = self._http_client.get(f'/session/{session_id}/todo')
        return [Todo(**item) for item in response]
    
    def fork(self, session_id: str, message_id: str) -> Session:
        """
        在指定消息处分叉会话。
        
        创建一个新会话，从指定消息开始。
        
        Args:
            session_id: 原会话 ID
            message_id: 分叉点消息 ID
            
        Returns:
            新创建的会话对象
            
        Raises:
            NotFoundError: 会话或消息不存在
            
        Example:
            >>> new_session = client.sessions.fork("session_123", "msg_456")
            >>> print(f"新会话 ID: {new_session.id}")
        """
        data = {'messageId': message_id}
        response = self._http_client.post(f'/session/{session_id}/fork', json_data=data)
        return Session(**response)
    
    # ==================== 初始化 ====================
    
    def init(self, session_id: str) -> None:
        """
        初始化会话。
        
        分析应用并创建 AGENTS.md 文件。
        
        Args:
            session_id: 会话 ID
            
        Raises:
            NotFoundError: 会话不存在
            
        Example:
            >>> client.sessions.init("session_123")
        """
        self._http_client.post(f'/session/{session_id}/init')
