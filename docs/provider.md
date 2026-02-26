# Provider 资源 - 提供商管理

Provider 资源提供 AI 提供商管理功能，包括列出提供商、获取认证方法和 OAuth 认证。

## 📋 方法列表

### Provider 资源
1. [list](#1-list) - 列出所有提供商
2. [auth](#2-auth) - 获取提供商认证方法

### OAuth 资源
3. [oauth.authorize](#3-oauthauthorize) - 启动 OAuth 授权流程
4. [oauth.callback](#4-oauthcallback) - 处理 OAuth 回调

---

## 📖 详细文档

### 1. list

列出所有提供商。

返回所有可用的 AI 提供商列表。

**返回值:**
- `List[Provider]` - Provider 对象列表

**示例:**
```python
providers = client.providers.list()
for provider in providers:
    print(f"{provider.id}: {provider.name}")
    for model in provider.models:
        print(f"  - {model.id}")
```

---

### 2. auth

获取提供商认证方法。

返回所有提供商支持的认证方法。

**返回值:**
- `Dict[str, List[ProviderAuthMethod]]` - 字典，键为提供商 ID，值为认证方法列表

**示例:**
```python
auth_methods = client.providers.auth()
for provider_id, methods in auth_methods.items():
    print(f"{provider_id}:")
    for method in methods:
        print(f"  - {method.type}")
```

---

### 3. oauth.authorize

启动 OAuth 授权流程。

**参数:**
- `provider_id` (str) - 提供商 ID

**返回值:**
- `Dict[str, Any]` - 包含授权 URL 的字典

**异常:**
- `NotFoundError` - 提供商不存在
- `BadRequestError` - 提供商不支持 OAuth

**示例:**
```python
result = client.providers.oauth.authorize("github")
print(f"请访问: {result['url']}")
```

---

### 4. oauth.callback

处理 OAuth 回调。

**参数:**
- `provider_id` (str) - 提供商 ID
- `code` (str) - 授权码
- `state` (Optional[str]) - 可选的状态参数

**返回值:**
- `Dict[str, Any]` - 认证结果字典

**异常:**
- `NotFoundError` - 提供商不存在
- `BadRequestError` - 授权码无效

**示例:**
```python
result = client.providers.oauth.callback(
    "github",
    code="auth_code_123"
)
print(f"认证成功: {result['success']}")
```

---

## 💡 使用建议

1. **查看提供商** - 使用 `list()` 查看所有可用的提供商和模型
2. **认证方法** - 使用 `auth()` 查看提供商支持的认证方式
3. **OAuth 认证** - 使用 `oauth.authorize()` 和 `oauth.callback()` 完成 OAuth 流程

## 🔗 相关资源

- [Config 资源](config.md) - 配置管理
- [Auth 资源](auth.md) - 认证凭据管理
