# MCP 资源 - 模型上下文协议

MCP (Model Context Protocol) 资源提供 MCP 服务器管理功能，包括添加、连接、断开和 OAuth 认证。

## 📋 方法列表

### MCP 资源
1. [status](#1-status) - 获取所有 MCP 服务器的状态
2. [add](#2-add) - 动态添加新的 MCP 服务器
3. [connect](#3-connect) - 连接 MCP 服务器
4. [disconnect](#4-disconnect) - 断开 MCP 服务器连接
5. [auth](#5-auth) - 获取 MCP OAuth 认证资源

### MCP Auth 资源
6. [auth.start](#6-authstart) - 开始 OAuth 认证流程
7. [auth.callback](#7-authcallback) - 完成 OAuth 认证
8. [auth.authenticate](#8-authauthenticate) - 启动 OAuth 流程并等待回调
9. [auth.remove](#9-authremove) - 移除 OAuth 凭证

---

## 📖 详细文档

### 1. status

获取所有 MCP 服务器的状态。

**返回值:**
- `Dict[str, Dict[str, Any]]` - MCP 服务器状态字典，键为服务器名称

**示例:**
```python
status = client.mcp.status()
for name, info in status.items():
    print(f"{name}: {info['status']}")
```

---

### 2. add

动态添加新的 MCP 服务器。

**参数:**
- `name` (str) - MCP 服务器名称
- `config` (Union[McpLocalConfig, McpRemoteConfig, Dict[str, Any]]) - MCP 服务器配置（本地或远程）

**返回值:**
- `Dict[str, Dict[str, Any]]` - 更新后的 MCP 服务器状态字典

**示例:**
```python
# 添加本地 MCP 服务器
config = {
    "command": "node",
    "args": ["server.js"],
    "env": {"API_KEY": "xxx"}
}
status = client.mcp.add("my-server", config)

# 添加远程 MCP 服务器
config = {
    "url": "https://api.example.com/mcp",
    "headers": {"Authorization": "Bearer token"}
}
status = client.mcp.add("remote-server", config)
```

---

### 3. connect

连接 MCP 服务器。

**参数:**
- `name` (str) - MCP 服务器名称

**返回值:**
- `bool` - 是否成功连接

**示例:**
```python
success = client.mcp.connect("my-server")
if success:
    print("MCP 服务器已连接")
```

---

### 4. disconnect

断开 MCP 服务器连接。

**参数:**
- `name` (str) - MCP 服务器名称

**返回值:**
- `bool` - 是否成功断开

**示例:**
```python
success = client.mcp.disconnect("my-server")
if success:
    print("MCP 服务器已断开")
```

---

### 5. auth

获取 MCP OAuth 认证资源。

**参数:**
- `name` (str) - MCP 服务器名称

**返回值:**
- `McpAuthResource` - MCP OAuth 认证资源实例

**示例:**
```python
# 开始 OAuth 认证
result = client.mcp.auth("github").start()
print(result["authorizationUrl"])

# 完成 OAuth 认证
status = client.mcp.auth("github").callback("auth_code")

# 一键认证（打开浏览器）
status = client.mcp.auth("github").authenticate()

# 移除认证
result = client.mcp.auth("github").remove()
```

---

### 6. auth.start

开始 OAuth 认证流程。

**返回值:**
- `Dict[str, str]` - 包含 authorizationUrl 的字典

**示例:**
```python
result = client.mcp.auth("github").start()
print(result["authorizationUrl"])
```

---

### 7. auth.callback

完成 OAuth 认证（使用授权码）。

**参数:**
- `code` (str) - OAuth 回调返回的授权码

**返回值:**
- `Dict[str, Any]` - MCP 服务器状态

**示例:**
```python
status = client.mcp.auth("github").callback("auth_code_123")
```

---

### 8. auth.authenticate

启动 OAuth 流程并等待回调（会打开浏览器）。

这是一个便捷方法，会自动打开浏览器并等待用户完成认证。

**返回值:**
- `Dict[str, Any]` - MCP 服务器状态

**示例:**
```python
status = client.mcp.auth("github").authenticate()
```

---

### 9. auth.remove

移除 OAuth 凭证。

**返回值:**
- `Dict[str, bool]` - 包含 success 字段的字典

**示例:**
```python
result = client.mcp.auth("github").remove()
print(result["success"])
```

---

## 💡 使用建议

1. **添加服务器** - 使用 `add()` 添加本地或远程 MCP 服务器
2. **连接管理** - 使用 `connect()` 和 `disconnect()` 管理连接
3. **OAuth 认证** - 使用 `auth()` 资源完成 OAuth 认证流程

## 🔗 相关资源

- [Provider 资源](provider.md) - 提供商管理
- [Tool 资源](tool.md) - 工具管理
