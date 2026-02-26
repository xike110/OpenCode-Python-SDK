# TUI 资源 - 终端用户界面

TUI (Terminal User Interface) 资源提供 TUI 交互功能，包括提示框操作、命令执行、对话框管理等。

## 📋 方法列表

### 提示框操作
1. [append_prompt](#1-append_prompt) - 追加文本到 TUI 提示框
2. [submit_prompt](#2-submit_prompt) - 提交 TUI 提示框中的内容
3. [clear_prompt](#3-clear_prompt) - 清空 TUI 提示框

### 命令执行
4. [execute_command](#4-execute_command) - 执行 TUI 命令

### 提示消息
5. [show_toast](#5-show_toast) - 在 TUI 中显示提示消息

### 对话框管理
6. [open_help](#6-open_help) - 打开 TUI 帮助对话框
7. [open_sessions](#7-open_sessions) - 打开 TUI 会话列表对话框
8. [open_themes](#8-open_themes) - 打开 TUI 主题选择对话框
9. [open_models](#9-open_models) - 打开 TUI 模型选择对话框

### 会话选择
10. [select_session](#10-select_session) - 选择指定的会话

### 事件发布
11. [publish](#11-publish) - 发布 TUI 事件

---

## 📖 详细文档

### 1. append_prompt

追加文本到 TUI 提示框。

**参数:**
- `text` (str) - 要追加的文本

**返回值:**
- `bool` - 是否成功追加

**示例:**
```python
success = client.tui.append_prompt("你好，")
success = client.tui.append_prompt("世界！")
```

---

### 2. submit_prompt

提交 TUI 提示框中的内容。

**返回值:**
- `bool` - 是否成功提交

**示例:**
```python
client.tui.append_prompt("帮我写一个函数")
client.tui.submit_prompt()
```

---

### 3. clear_prompt

清空 TUI 提示框。

**返回值:**
- `bool` - 是否成功清空

**示例:**
```python
success = client.tui.clear_prompt()
```

---

### 4. execute_command

执行 TUI 命令。

**参数:**
- `command` (str) - 要执行的命令（例如 "agent_cycle"）

**返回值:**
- `bool` - 是否成功执行

**示例:**
```python
success = client.tui.execute_command("agent_cycle")
```

---

### 5. show_toast

在 TUI 中显示提示消息。

**参数:**
- `message` (str) - 提示消息内容
- `variant` (Literal["info", "success", "warning", "error"]) - 消息类型
- `title` (Optional[str]) - 消息标题（可选）
- `duration` (int) - 显示时长（毫秒），默认 5000

**返回值:**
- `bool` - 是否成功显示

**示例:**
```python
# 显示成功消息
client.tui.show_toast("操作成功", "success")

# 显示错误消息
client.tui.show_toast(
    "操作失败",
    "error",
    title="错误",
    duration=10000
)
```

---

### 6. open_help

打开 TUI 帮助对话框。

**返回值:**
- `bool` - 是否成功打开

**示例:**
```python
success = client.tui.open_help()
```

---

### 7. open_sessions

打开 TUI 会话列表对话框。

**返回值:**
- `bool` - 是否成功打开

**示例:**
```python
success = client.tui.open_sessions()
```

---

### 8. open_themes

打开 TUI 主题选择对话框。

**返回值:**
- `bool` - 是否成功打开

**示例:**
```python
success = client.tui.open_themes()
```

---

### 9. open_models

打开 TUI 模型选择对话框。

**返回值:**
- `bool` - 是否成功打开

**示例:**
```python
success = client.tui.open_models()
```

---

### 10. select_session

选择指定的会话。

**参数:**
- `session_id` (str) - 会话 ID

**返回值:**
- `bool` - 是否成功选择

**示例:**
```python
success = client.tui.select_session("ses_123")
```

---

### 11. publish

发布 TUI 事件。

**参数:**
- `event` (Dict[str, Any]) - 事件数据

**返回值:**
- `bool` - 是否成功发布

**示例:**
```python
event = {
    "type": "tui.prompt.append",
    "text": "Hello"
}
success = client.tui.publish(event)
```

---

## 💡 使用建议

1. **提示框操作** - 使用 `append_prompt()`, `submit_prompt()`, `clear_prompt()` 操作提示框
2. **命令执行** - 使用 `execute_command()` 执行 TUI 命令
3. **提示消息** - 使用 `show_toast()` 显示各种类型的提示消息
4. **对话框管理** - 使用 `open_*()` 方法打开各种对话框

## 🔗 相关资源

- [Session 资源](session.md) - 会话管理
- [App 资源](app.md) - 应用管理
