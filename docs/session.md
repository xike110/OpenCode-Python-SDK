# Session 资源 - 会话管理

Session 资源提供完整的会话管理功能，包括创建、查询、更新、删除会话，以及消息交互、命令执行、版本控制等功能。

## 📋 方法列表

### 基础 CRUD 操作
1. [list](#1-list) - 列出所有会话
2. [create](#2-create) - 创建新会话
3. [get](#3-get) - 获取会话详情
4. [delete](#4-delete) - 删除会话
5. [update](#5-update) - 更新会话属性

### 状态和消息
6. [status](#6-status) - 获取会话状态
7. [messages](#7-messages) - 获取会话的消息列表
8. [message](#8-message) - 获取单条消息

### 交互操作
9. [prompt](#9-prompt) - 发送消息到会话（同步）
10. [prompt_async](#10-prompt_async) - 发送消息到会话（异步流式）
11. [command](#11-command) - 执行命令
12. [shell](#12-shell) - 执行 Shell 命令
13. [abort](#13-abort) - 中止会话

### 分享和协作
14. [share](#14-share) - 分享会话
15. [unshare](#15-unshare) - 取消分享会话

### 差异和总结
16. [diff](#16-diff) - 获取会话的文件差异
17. [summarize](#17-summarize) - 总结会话

### 版本控制
18. [revert](#18-revert) - 回退到指定消息
19. [unrevert](#19-unrevert) - 恢复所有回退的消息

### 关系和层级
20. [children](#20-children) - 获取子会话列表
21. [todo](#21-todo) - 获取待办事项列表
22. [fork](#22-fork) - 在指定消息处分叉会话

### 初始化
23. [init](#23-init) - 初始化会话

---

## 📖 详细文档

### 1. list

列出所有会话。

**参数:**
- `directory` (Optional[str]) - 可选的目录路径，用于过滤特定目录的会话

**返回值:**
- `List[Session]` - 会话列表

**示例:**
```python
sessions = client.sessions.list()
for session in sessions:
    print(f"{session.id}: {session.name}")

# 按目录过滤
sessions = client.sessions.list(directory="/path/to/project")
```

---

### 2. create

创建新会话。

**参数:**
- `title` (Optional[str]) - 会话标题
- `directory` (Optional[str]) - 项目目录（作为查询参数，用于指定项目）
- `parent_id` (Optional[str]) - 父会话 ID（用于创建子会话）
- `permission` (Optional[Dict[str, Any]]) - 权限规则集
- `**kwargs` - 其他可选参数

**返回值:**
- `Session` - 创建的会话对象

**示例:**
```python
# 创建普通会话
session = client.sessions.create(title="新会话")

# 在指定目录创建会话（自动创建项目）
session = client.sessions.create(
    title="新会话",
    directory="/path/to/project"
)

# 创建子会话
child_session = client.sessions.create(
    title="子会话",
    parent_id="ses_parent_id"
)
```

---

### 3. get

获取会话详情。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `Session` - 会话对象

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
session = client.sessions.get("session_123")
print(session.name)
print(session.created_at)
```

---

### 4. delete

删除会话及其所有数据。

**参数:**
- `session_id` (str) - 会话 ID

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
client.sessions.delete("session_123")
```

---

### 5. update

更新会话属性。

**参数:**
- `session_id` (str) - 会话 ID
- `**kwargs` - 要更新的属性（name, providerId, modelId 等）

**返回值:**
- `Session` - 更新后的会话对象

**异常:**
- `NotFoundError` - 会话不存在
- `BadRequestError` - 参数无效

**示例:**
```python
session = client.sessions.update(
    "session_123",
    name="新名称",
    modelId="claude-3-5-sonnet-20241022"
)
```

---

### 6. status

获取会话状态。

**参数:**
- `session_id` (Optional[str]) - 可选的会话 ID，如果不提供则返回所有会话的状态

**返回值:**
- `Dict[str, SessionStatus]` - 会话状态字典，键为会话 ID，值为状态对象

**示例:**
```python
# 获取所有会话状态
statuses = client.sessions.status()

# 获取特定会话状态
status = client.sessions.status("session_123")
print(status.status)
print(status.message_count)
```

---

### 7. messages

获取会话的消息列表。

**参数:**
- `session_id` (str) - 会话 ID
- `limit` (Optional[int]) - 限制返回的消息数量
- `offset` (Optional[int]) - 偏移量，用于分页

**返回值:**
- `List[Message]` - 消息列表

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
messages = client.sessions.messages("session_123", limit=10)
for msg in messages:
    print(f"{msg.role}: {msg.parts[0].text}")
```

---

### 8. message

获取单条消息。

**参数:**
- `session_id` (str) - 会话 ID
- `message_id` (str) - 消息 ID

**返回值:**
- `Message` - 消息对象

**异常:**
- `NotFoundError` - 会话或消息不存在

**示例:**
```python
message = client.sessions.message("session_123", "msg_456")
print(message.parts[0].text)
```

---

### 9. prompt

发送消息到会话（同步）。

此方法会等待 AI 完成响应后返回。

**参数:**
- `session_id` (str) - 会话 ID
- `parts` (List[Dict[str, Any]]) - 消息部分列表，每个部分是一个字典
- `**kwargs` - 其他可选参数

**返回值:**
- `Message` - AI 的响应消息

**异常:**
- `NotFoundError` - 会话不存在
- `BadRequestError` - 参数无效
- `MessageAbortedError` - 消息被中止

**示例:**
```python
response = client.sessions.prompt(
    "session_123",
    parts=[{"type": "text", "text": "你好"}]
)
print(response.parts[0].text)

# 发送多部分消息
response = client.sessions.prompt(
    "session_123",
    parts=[
        {"type": "text", "text": "请分析这个文件："},
        {"type": "file", "path": "main.py"}
    ]
)
```

---

### 10. prompt_async

发送消息到会话（异步流式）。

此方法立即返回，通过事件流接收 AI 的响应。

**参数:**
- `session_id` (str) - 会话 ID
- `parts` (List[Dict[str, Any]]) - 消息部分列表
- `**kwargs` - 其他可选参数

**返回值:**
- `AsyncIterator[Event]` - 事件对象迭代器

**异常:**
- `NotFoundError` - 会话不存在
- `BadRequestError` - 参数无效

**示例:**
```python
async for event in client.sessions.prompt_async(
    "session_123",
    parts=[{"type": "text", "text": "你好"}]
):
    if event.type == "text":
        print(event.text, end="", flush=True)
```

---

### 11. command

执行命令。

**参数:**
- `session_id` (str) - 会话 ID
- `name` (str) - 命令名称
- `args` (Optional[Dict[str, Any]]) - 命令参数

**返回值:**
- `Message` - 命令执行结果消息

**异常:**
- `NotFoundError` - 会话不存在
- `BadRequestError` - 命令无效

**示例:**
```python
result = client.sessions.command(
    "session_123",
    name="search",
    args={"query": "TODO"}
)
print(result.parts[0].text)
```

---

### 12. shell

执行 Shell 命令。

**参数:**
- `session_id` (str) - 会话 ID
- `command` (str) - Shell 命令字符串

**返回值:**
- `Message` - 命令执行结果消息

**异常:**
- `NotFoundError` - 会话不存在
- `BadRequestError` - 命令无效

**示例:**
```python
result = client.sessions.shell(
    "session_123",
    command="ls -la"
)
print(result.parts[0].text)
```

---

### 13. abort

中止会话。

停止当前正在执行的操作。

**参数:**
- `session_id` (str) - 会话 ID

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
client.sessions.abort("session_123")
```

---

### 14. share

分享会话。

生成分享链接，允许其他人查看会话。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `Session` - 更新后的会话对象（包含分享信息）

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
session = client.sessions.share("session_123")
print(f"分享链接: {session.share_url}")
```

---

### 15. unshare

取消分享会话。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `Session` - 更新后的会话对象

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
session = client.sessions.unshare("session_123")
```

---

### 16. diff

获取会话的文件差异。

返回会话中所有文件的修改差异。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `List[FileDiff]` - 文件差异列表

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
diffs = client.sessions.diff("session_123")
for diff in diffs:
    print(f"{diff.path}: +{diff.additions} -{diff.deletions}")
```

---

### 17. summarize

总结会话。

生成会话的摘要信息。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `SessionSummary` - 会话摘要对象

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
summary = client.sessions.summarize("session_123")
print(summary.summary)
```

---

### 18. revert

回退到指定消息。

将会话状态回退到指定消息之前的状态。

**参数:**
- `session_id` (str) - 会话 ID
- `message_id` (str) - 要回退到的消息 ID

**返回值:**
- `Session` - 更新后的会话对象

**异常:**
- `NotFoundError` - 会话或消息不存在

**示例:**
```python
session = client.sessions.revert("session_123", "msg_456")
```

---

### 19. unrevert

恢复所有回退的消息。

取消之前的回退操作，恢复到最新状态。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `Session` - 更新后的会话对象

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
session = client.sessions.unrevert("session_123")
```

---

### 20. children

获取子会话列表。

返回从当前会话分叉出的所有子会话。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `List[Session]` - 子会话列表

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
children = client.sessions.children("session_123")
for child in children:
    print(f"子会话: {child.name}")
```

---

### 21. todo

获取待办事项列表。

返回会话中标记的所有待办事项。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `List[Todo]` - 待办事项列表

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
todos = client.sessions.todo("session_123")
for todo in todos:
    checkbox = "☑" if todo.completed else "☐"
    print(f"{checkbox} {todo.text}")
```

---

### 22. fork

在指定消息处分叉会话。

创建一个新会话，从指定消息开始。

**参数:**
- `session_id` (str) - 原会话 ID
- `message_id` (str) - 分叉点消息 ID

**返回值:**
- `Session` - 新创建的会话对象

**异常:**
- `NotFoundError` - 会话或消息不存在

**示例:**
```python
new_session = client.sessions.fork("session_123", "msg_456")
print(f"新会话 ID: {new_session.id}")
```

---

### 23. init

初始化会话。

分析应用并创建 AGENTS.md 文件。

**参数:**
- `session_id` (str) - 会话 ID

**异常:**
- `NotFoundError` - 会话不存在

**示例:**
```python
client.sessions.init("session_123")
```

---

## 💡 使用建议

1. **创建会话** - 使用 `create()` 方法创建新会话
2. **发送消息** - 使用 `prompt()` 进行同步交互，使用 `prompt_async()` 进行流式交互
3. **管理会话** - 使用 `list()`, `get()`, `update()`, `delete()` 管理会话
4. **版本控制** - 使用 `revert()` 和 `unrevert()` 管理会话版本
5. **协作功能** - 使用 `share()` 和 `unshare()` 分享会话

## 🔗 相关资源

- [Event 资源](event.md) - 事件订阅和流式响应
- [Project 资源](project.md) - 项目管理
- [Config 资源](config.md) - 配置管理
