# Instance 资源 - 实例管理

Instance 资源提供实例管理功能。

## 📋 方法列表

1. [dispose](#1-dispose) - 释放当前实例

---

## 📖 详细文档

### 1. dispose

释放当前实例。

清理并释放当前 OpenCode 实例，释放所有资源。

**返回值:**
- `bool` - 是否成功释放

**警告:**
此操作会关闭当前实例的所有会话和资源，请谨慎使用。

**示例:**
```python
# 释放当前实例
success = client.instance.dispose()
if success:
    print("实例已成功释放")
```

---

## 💡 使用建议

1. **清理资源** - 使用 `dispose()` 释放当前实例（谨慎使用）

## 🔗 相关资源

- [Global 资源](global.md) - 全局管理
- [Session 资源](session.md) - 会话管理
