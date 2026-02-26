# Global 资源 - 全局管理

Global 资源提供全局系统管理功能，用于健康检查、全局事件订阅和实例管理。

## 📋 方法列表

1. [health](#1-health) - 获取服务器健康状态
2. [subscribe_events](#2-subscribe_events) - 订阅全局事件流
3. [dispose](#3-dispose) - 释放所有实例

---

## 📖 详细文档

### 1. health

获取服务器健康状态。

检查 OpenCode 服务器是否正常运行。

**返回值:**
- `Dict[str, Any]` - 健康状态信息字典，包含：
  - `healthy` - 是否健康 (True/False)
  - `version` - 服务器版本号

**示例:**
```python
health = client.global_resource.health()
if health['healthy']:
    print(f"服务器正常运行，版本: {health['version']}")
else:
    print("服务器异常")
```

---

### 2. subscribe_events

订阅全局事件流。

订阅来自所有项目实例的全局事件，使用 Server-Sent Events (SSE)。

**返回值:**
- `Generator[Dict[str, Any], None, None]` - 全局事件生成器

**示例:**
```python
# 订阅全局事件
for event in client.global_resource.subscribe_events():
    directory = event.get('directory')
    payload = event.get('payload', {})
    event_type = payload.get('type')
    print(f"[{directory}] {event_type}")

    if event_type == 'server.connected':
        print("服务器已连接")
    elif event_type == 'global.disposed':
        print("全局实例已释放")
        break
```

---

### 3. dispose

释放所有实例。

清理并释放所有 OpenCode 实例，释放所有资源。这将关闭所有打开的项目和会话。

**返回值:**
- `bool` - 是否成功释放

**警告:**
此操作会关闭所有活动会话和项目，请谨慎使用。

**示例:**
```python
# 释放所有实例
success = client.global_resource.dispose()
if success:
    print("所有实例已成功释放")
```

---

## 💡 使用建议

1. **健康检查** - 使用 `health()` 检查服务器状态
2. **全局事件** - 使用 `subscribe_events()` 订阅系统级事件
3. **清理资源** - 使用 `dispose()` 释放所有实例（谨慎使用）

## 🔗 相关资源

- [Instance 资源](instance.md) - 实例管理
- [Event 资源](event.md) - 事件订阅
