# Config 资源 - 配置管理

Config 资源提供配置管理功能，用于查询和更新 OpenCode 配置。

## 📋 方法列表

1. [get](#1-get) - 获取配置信息
2. [update](#2-update) - 更新配置
3. [providers](#3-providers) - 列出所有提供商配置

---

## 📖 详细文档

### 1. get

获取配置信息。

返回当前的 OpenCode 配置。

**返回值:**
- `Config` - 配置对象

**示例:**
```python
config = client.config.get()
print(f"默认提供商: {config.default_provider_id}")
print(f"默认模型: {config.default_model_id}")
print(f"日志级别: {config.log_level}")
```

---

### 2. update

更新配置。

更新 OpenCode 配置的一个或多个字段。

**参数:**
- `**kwargs` - 要更新的配置字段
  - `default_provider_id` - 默认提供商 ID
  - `default_model_id` - 默认模型 ID
  - `agent_id` - 代理 ID
  - 其他配置字段...

**返回值:**
- `Config` - 更新后的 Config 对象

**异常:**
- `BadRequestError` - 配置参数无效

**示例:**
```python
# 更新默认提供商和模型
config = client.config.update(
    default_provider_id="anthropic",
    default_model_id="claude-3-5-sonnet-20241022"
)
print(f"配置已更新: {config.default_provider_id}")

# 更新日志级别
config = client.config.update(log_level="DEBUG")

# 更新主题
config = client.config.update(theme="dark")
```

---

### 3. providers

列出所有提供商配置。

返回所有已配置的 AI 提供商列表。

**返回值:**
- `List[Dict[str, Any]]` - 提供商配置列表

**示例:**
```python
providers = client.config.providers()
for provider in providers:
    print(f"{provider['id']}: {provider['name']}")
```

---

## 💡 使用建议

1. **查看配置** - 使用 `get()` 查看当前配置
2. **修改配置** - 使用 `update()` 更新配置
3. **提供商管理** - 使用 `providers()` 查看已配置的提供商

## 🔗 相关资源

- [Provider 资源](provider.md) - 提供商管理
- [Session 资源](session.md) - 会话管理
