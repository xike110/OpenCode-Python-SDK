# Event 资源 - 事件订阅

Event 资源提供事件订阅功能，用于接收服务器推送的实时事件。

## 📋 方法列表

1. [subscribe](#1-subscribe) - 订阅事件流
2. [subscribe_global](#2-subscribe_global) - 订阅全局事件
3. [subscribe_session](#3-subscribe_session) - 订阅会话事件

---

## 📖 详细文档

### 1. subscribe

订阅事件流。

如果提供 session_id，则订阅特定会话的事件；否则订阅全局事件。

**参数:**
- `session_id` (Optional[str]) - 可选的会话 ID
- `**kwargs` - 其他查询参数

**返回值:**
- `AsyncIterator[Event]` - 事件对象迭代器

**异常:**
- `ConnectionError` - 连接失败
- `TimeoutError` - 连接超时
- `APIError` - API 错误

**示例:**
```python
# 订阅全局事件
async for event in client.events.subscribe():
    print(f"全局事件: {event.type}")

# 订阅会话事件
async for event in client.events.subscribe(session_id="session_123"):
    if event.type == "text":
        print(event.text, end="", flush=True)
```

---

### 2. subscribe_global

订阅全局事件。

这是 `subscribe()` 的便捷方法，专门用于订阅全局事件。

**返回值:**
- `AsyncIterator[GlobalEvent]` - 全局事件对象迭代器

**示例:**
```python
async for event in client.events.subscribe_global():
    print(f"全局事件: {event.type}")
    if event.type == "session:created":
        print(f"新会话: {event.info.name}")
```

---

### 3. subscribe_session

订阅会话事件（发送消息并接收响应流）。

正确的流程：
1. 先订阅 /event 端点（SSE 流）
2. 发送消息到 /session/{id}/prompt_async
3. 通过 /event 流接收响应

**参数:**
- `session_id` (str) - 会话 ID
- `parts` (Optional[list]) - 消息部分列表（如果提供，则发送消息）
- `agent` (Optional[str]) - 代理名称（如 "build"）
- `model` (Optional[Dict[str, str]]) - 模型配置，包含：
  - `modelID` (str) - 模型 ID（如 "gpt-5-nano", "claude-3-5-sonnet-20241022"）
  - `providerID` (str) - 提供商 ID（如 "opencode", "anthropic", "openai"）
- `variant` (Optional[str]) - 变体（如 "low", "medium", "high"）
- `**kwargs` - 其他参数

**返回值:**
- `AsyncIterator[Event]` - 事件对象迭代器

**示例:**
```python
# 基本用法 - 发送消息并接收流式响应
async for event in client.events.subscribe_session(
    session_id="session_123",
    parts=[{"type": "text", "text": "你好"}]
):
    if event.type == "text":
        print(event.text, end="", flush=True)

# 使用指定模型和代理
async for event in client.events.subscribe_session(
    session_id="session_123",
    parts=[{"type": "text", "text": "当前时间"}],
    agent="build",
    model={
        "modelID": "gpt-5-nano",
        "providerID": "opencode"
    },
    variant="low"
):
    if event.type == "text":
        print(event.text, end="", flush=True)

# 使用 Claude 模型
async for event in client.events.subscribe_session(
    session_id="session_123",
    parts=[{"type": "text", "text": "帮我写一个 Python 函数"}],
    model={
        "modelID": "claude-3-5-sonnet-20241022",
        "providerID": "anthropic"
    }
):
    if event.type == "text":
        print(event.text, end="", flush=True)

# 使用 GPT 模型
async for event in client.events.subscribe_session(
    session_id="session_123",
    parts=[{"type": "text", "text": "分析这段代码"}],
    model={
        "modelID": "gpt-4-turbo",
        "providerID": "openai"
    },
    variant="high"
):
    if event.type == "text":
        print(event.text, end="", flush=True)

# 只订阅事件，不发送消息
async for event in client.events.subscribe_session(session_id="session_123"):
    print(f"事件类型: {event.type}")
```

---

## 💡 使用建议

1. **流式响应** - 使用 `subscribe_session()` 获取实时 AI 响应
2. **全局事件** - 使用 `subscribe_global()` 监听系统级事件
3. **事件处理** - 根据事件类型（type）处理不同的事件

## 🔗 相关资源

- [Session 资源](session.md) - 会话管理和消息交互
- [Global 资源](global.md) - 全局事件订阅
