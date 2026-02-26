# VCS 资源 - 版本控制

VCS 资源提供版本控制系统信息查询功能。

## 📋 方法列表

1. [get](#1-get) - 获取 VCS 信息

---

## 📖 详细文档

### 1. get

获取 VCS 信息。

检索当前项目的版本控制系统信息，如 git 分支。

**返回值:**
- `Dict[str, Optional[str]]` - VCS 信息字典，包含：
  - `branch` - 当前 git 分支名称（如果有）

**示例:**
```python
vcs_info = client.vcs.get()
if vcs_info['branch']:
    print(f"当前分支: {vcs_info['branch']}")
else:
    print("不在 git 仓库中")
```

---

## 💡 使用建议

1. **版本控制** - 使用 `get()` 获取当前项目的版本控制信息

## 🔗 相关资源

- [Project 资源](project.md) - 项目管理
- [File 资源](file.md) - 文件操作
