# Auth 资源 - 认证管理

Auth 资源提供认证凭据管理功能。

## 📋 方法列表

1. [set](#1-set) - 设置认证凭据

---

## 📖 详细文档

### 1. set

设置认证凭据。

为指定的提供商设置认证凭据。

**参数:**
- `provider_id` (str) - 提供商 ID
- `credentials` (Dict[str, Any]) - 认证凭据字典，可能包含：
  - `api_key` - API 密钥
  - `access_token` - 访问令牌
  - `refresh_token` - 刷新令牌
  - 其他提供商特定的凭据

**返回值:**
- `bool` - 是否成功设置

**异常:**
- `BadRequestError` - 凭据格式无效

**示例:**
```python
# 设置 API 密钥
success = client.auth.set(
    provider_id="anthropic",
    credentials={"api_key": "sk-ant-..."}
)
if success:
    print("认证凭据已设置")

# 设置 OAuth 令牌
success = client.auth.set(
    provider_id="github",
    credentials={
        "access_token": "gho_...",
        "refresh_token": "ghr_..."
    }
)
```

---

## 💡 使用建议

1. **设置凭据** - 使用 `set()` 为提供商设置认证凭据

## 🔗 相关资源

- [Provider 资源](provider.md) - 提供商管理
- [Config 资源](config.md) - 配置管理
