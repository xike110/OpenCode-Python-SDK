# PTY 资源 - 终端会话管理

PTY (Pseudo-Terminal) 资源提供 PTY 会话管理功能，包括创建、更新、删除和连接 PTY 会话。

## 📋 方法列表

1. [list](#1-list) - 列出所有活动的 PTY 会话
2. [create](#2-create) - 创建新的 PTY 会话
3. [get](#3-get) - 获取指定 PTY 会话的详细信息
4. [update](#4-update) - 更新 PTY 会话属性
5. [remove](#5-remove) - 移除并终止 PTY 会话
6. [connect](#6-connect) - 建立 WebSocket 连接

---

## 📖 详细文档

### 1. list

列出所有活动的 PTY 会话。

**返回值:**
- `List[Dict[str, Any]]` - PTY 会话列表

**示例:**
```python
sessions = client.pty.list()
for pty in sessions:
    print(f"{pty['id']}: {pty['title']}")
```

---

### 2. create

创建新的 PTY 会话。

**参数:**
- `command` (Optional[str]) - 要执行的命令（可选）
- `args` (Optional[List[str]]) - 命令参数列表（可选）
- `cwd` (Optional[str]) - 工作目录（可选）
- `title` (Optional[str]) - PTY 会话标题（可选）
- `env` (Optional[Dict[str, str]]) - 环境变量字典（可选）

**返回值:**
- `Dict[str, Any]` - 创建的 PTY 会话信息

**示例:**
```python
# 创建默认 shell 会话
pty = client.pty.create()

# 创建自定义命令会话
pty = client.pty.create(
    command="python",
    args=["-m", "http.server"],
    cwd="/path/to/project",
    title="HTTP Server",
    env={"PORT": "8000"}
)
```

---

### 3. get

获取指定 PTY 会话的详细信息。

**参数:**
- `pty_id` (str) - PTY 会话 ID

**返回值:**
- `Dict[str, Any]` - PTY 会话信息

**示例:**
```python
pty = client.pty.get("pty_123")
print(pty["title"])
```

---

### 4. update

更新 PTY 会话属性。

**参数:**
- `pty_id` (str) - PTY 会话 ID
- `title` (Optional[str]) - 新标题（可选）
- `size` (Optional[Dict[str, int]]) - 终端大小 {"rows": 24, "cols": 80}（可选）

**返回值:**
- `Dict[str, Any]` - 更新后的 PTY 会话信息

**示例:**
```python
# 更新标题
pty = client.pty.update("pty_123", title="新标题")

# 更新终端大小
pty = client.pty.update(
    "pty_123",
    size={"rows": 30, "cols": 120}
)
```

---

### 5. remove

移除并终止 PTY 会话。

**参数:**
- `pty_id` (str) - PTY 会话 ID

**返回值:**
- `bool` - 是否成功移除

**示例:**
```python
success = client.pty.remove("pty_123")
```

---

### 6. connect

建立 WebSocket 连接以与 PTY 会话实时交互。

注意: 此方法返回连接状态，实际的 WebSocket 连接需要使用 WebSocket 客户端。

**参数:**
- `pty_id` (str) - PTY 会话 ID

**返回值:**
- `bool` - 是否可以连接

**示例:**
```python
can_connect = client.pty.connect("pty_123")
if can_connect:
    # 使用 WebSocket 客户端连接到 ws://host/pty/pty_123/connect
    pass
```

---

## 💡 使用建议

1. **创建会话** - 使用 `create()` 创建新的 PTY 会话
2. **管理会话** - 使用 `list()`, `get()`, `update()`, `remove()` 管理会话
3. **实时交互** - 使用 `connect()` 建立 WebSocket 连接进行实时交互

## 🔗 相关资源

- [Session 资源](session.md) - 会话管理
- [Command 资源](command.md) - 命令管理
