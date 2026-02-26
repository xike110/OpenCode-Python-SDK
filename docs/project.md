# Project 资源 - 项目管理

Project 资源提供项目管理功能，用于查询和管理 OpenCode 项目。

## 📋 方法列表

1. [list](#1-list) - 列出所有项目
2. [current](#2-current) - 获取当前项目信息
3. [update](#3-update) - 更新项目属性

---

## 📖 详细文档

### 1. list

列出所有项目。

返回已在 OpenCode 中打开的所有项目列表。

**参数:**
- `directory` (Optional[str]) - 可选的目录路径，用于过滤特定目录的项目

**返回值:**
- `List[dict]` - 项目列表，每个项目是一个字典

**示例:**
```python
projects = client.projects.list()
for project in projects:
    print(f"{project['name']}: {project['path']}")

# 按目录过滤
projects = client.projects.list(directory="/path/to/project")
```

---

### 2. current

获取当前项目信息。

返回当前正在使用的项目信息。

**参数:**
- `directory` (Optional[str]) - 可选的目录路径

**返回值:**
- `dict` - 当前项目信息字典

**异常:**
- `NotFoundError` - 项目不存在

**示例:**
```python
project = client.projects.current()
print(f"当前项目: {project['name']}")
print(f"路径: {project['path']}")
```

---

### 3. update

更新项目属性。

更新项目的名称、图标或颜色等属性。

**参数:**
- `project_id` (str) - 项目 ID
- `name` (Optional[str]) - 可选的新项目名称
- `icon` (Optional[str]) - 可选的新项目图标
- `color` (Optional[str]) - 可选的新项目颜色

**返回值:**
- `dict` - 更新后的项目信息字典

**异常:**
- `NotFoundError` - 项目不存在
- `BadRequestError` - 参数无效

**示例:**
```python
# 更新项目名称
project = client.projects.update(
    project_id="proj_123",
    name="新项目名称"
)

# 更新项目图标和颜色
project = client.projects.update(
    project_id="proj_123",
    icon="🚀",
    color="#FF5733"
)
```

---

## 💡 使用建议

1. **查看项目** - 使用 `list()` 查看所有打开的项目
2. **当前项目** - 使用 `current()` 获取当前项目信息
3. **自定义项目** - 使用 `update()` 修改项目外观

## 🔗 相关资源

- [Session 资源](session.md) - 会话管理
- [Config 资源](config.md) - 配置管理
- [File 资源](file.md) - 文件操作
