# File 资源 - 文件操作

File 资源提供文件操作功能，包括列出文件、读取文件和获取文件状态。

## 📋 方法列表

1. [list](#1-list) - 列出文件和目录
2. [read](#2-read) - 读取文件内容
3. [status](#3-status) - 获取文件状态

---

## 📖 详细文档

### 1. list

列出文件和目录。

**参数:**
- `path` (str) - 目录路径（默认为当前目录）
- `recursive` (bool) - 是否递归列出子目录
- `max_depth` (Optional[int]) - 最大递归深度

**返回值:**
- `List[FileNode]` - FileNode 对象列表

**示例:**
```python
# 列出当前目录
files = client.files.list()
for file in files:
    print(f"{file.name} ({'dir' if file.is_directory else 'file'})")

# 递归列出所有文件
files = client.files.list(recursive=True, max_depth=3)
```

---

### 2. read

读取文件内容。

**参数:**
- `path` (str) - 文件路径
- `start_line` (Optional[int]) - 起始行号（可选）
- `end_line` (Optional[int]) - 结束行号（可选）

**返回值:**
- `FileContent` - FileContent 对象

**异常:**
- `NotFoundError` - 文件不存在
- `BadRequestError` - 文件无法读取

**示例:**
```python
# 读取整个文件
content = client.files.read("README.md")
print(content.content)

# 读取指定行
content = client.files.read("README.md", start_line=1, end_line=10)
print(content.content)
```

---

### 3. status

获取文件状态。

返回文件系统的状态信息，如修改的文件、未跟踪的文件等。

**返回值:**
- `Dict[str, Any]` - 文件状态字典

**示例:**
```python
status = client.files.status()
print(f"修改的文件: {len(status.get('modified', []))}")
print(f"未跟踪的文件: {len(status.get('untracked', []))}")
```

---

## 💡 使用建议

1. **浏览文件** - 使用 `list()` 浏览项目文件结构
2. **读取文件** - 使用 `read()` 读取文件内容
3. **查看状态** - 使用 `status()` 查看文件修改状态

## 🔗 相关资源

- [Find 资源](find.md) - 搜索功能
- [Project 资源](project.md) - 项目管理
