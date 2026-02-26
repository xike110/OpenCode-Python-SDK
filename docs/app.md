# App 资源 - 应用管理

App 资源提供应用管理功能，包括日志写入、代理列表和技能列表。

## 📋 方法列表

1. [log](#1-log) - 写入日志到服务器
2. [agents](#2-agents) - 列出所有可用的 AI 代理
3. [skills](#3-skills) - 列出所有可用的技能

---

## 📖 详细文档

### 1. log

写入日志到服务器。

**参数:**
- `service` (str) - 服务名称
- `level` (Literal["debug", "info", "warn", "error"]) - 日志级别
- `message` (str) - 日志消息
- `extra` (Optional[Dict[str, Any]]) - 额外的元数据（可选）

**返回值:**
- `bool` - 是否成功写入

**示例:**
```python
# 写入信息日志
client.app.log("my-service", "info", "操作成功")

# 写入错误日志并附加元数据
client.app.log(
    "my-service",
    "error",
    "操作失败",
    extra={"user_id": "123", "action": "delete"}
)
```

---

### 2. agents

列出所有可用的 AI 代理。

**返回值:**
- `List[Dict[str, Any]]` - 代理列表

**示例:**
```python
agents = client.app.agents()
for agent in agents:
    print(f"{agent['name']}: {agent['description']}")
```

---

### 3. skills

列出所有可用的技能。

**返回值:**
- `List[Dict[str, Any]]` - 技能列表

**示例:**
```python
skills = client.app.skills()
for skill in skills:
    print(f"{skill['name']}: {skill['description']}")
```

---

## 💡 使用建议

1. **日志记录** - 使用 `log()` 记录应用日志
2. **查看代理** - 使用 `agents()` 查看可用的 AI 代理
3. **查看技能** - 使用 `skills()` 查看可用的技能

## 🔗 相关资源

- [Session 资源](session.md) - 会话管理
- [Command 资源](command.md) - 命令管理
