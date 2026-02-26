# OpenCode Python SDK - 演示程序使用指南

本指南详细介绍了如何使用 OpenCode Python SDK 的演示程序。

## 📋 演示程序概述

项目提供了两个演示程序：

1. **quick_demo.py** - 快速入门演示（推荐新手）
2. **demo.py** - 完整功能演示

## 🚀 快速入门演示 (quick_demo.py)

### 功能介绍

快速入门演示展示了 SDK 最常用的基础功能，适合第一次使用 SDK 的用户。

### 包含的功能

- ✅ 创建客户端
- ✅ 创建会话
- ✅ 发送消息
- ✅ 获取响应
- ✅ 列出所有会话
- ✅ 删除会话

### 运行方法

```bash
# 基本运行
python quick_demo.py

# 使用自定义服务器地址
python quick_demo.py --base-url http://your-server:8000

# 指定项目目录
python quick_demo.py --directory /path/to/your/project
```

### 输出示例

```
============================================================
OpenCode Python SDK - 快速入门演示
============================================================

步骤1: 创建客户端
------------------------------------------------------------
✅ 客户端创建成功
   服务器地址: http://localhost:8000

步骤2: 创建会话
------------------------------------------------------------
✅ 会话创建成功
   会话 ID: abc123...
   会话名称: 快速入门演示

步骤3: 发送消息
------------------------------------------------------------
✅ 消息发送成功
   消息 ID: msg456...
   角色: assistant
   回复: 你好！我是 OpenCode AI 助手...

步骤4: 列出所有会话
------------------------------------------------------------
✅ 共有 5 个会话
   - 快速入门演示 (ID: abc123...)
   - 我的第一个任务 (ID: def456...)
   ...

步骤5: 删除会话
------------------------------------------------------------
✅ 会话已删除

============================================================
✅ 演示完成！
============================================================
```

## 🎯 完整功能演示 (demo.py)

### 功能介绍

完整功能演示展示了 SDK 的所有主要功能，包括同步和异步操作。

### 包含的功能

#### 1. 客户端初始化和配置
- 创建客户端实例
- 配置服务器地址和项目目录
- 显示客户端信息

#### 2. 会话管理
- 列出所有会话
- 创建新会话
- 获取会话详情
- 更新会话信息
- 删除会话

#### 3. 消息处理
- 发送消息到会话
- 获取消息响应
- 列出会话消息
- 显示消息预览

#### 4. 文件操作
- 列出当前目录文件
- 获取文件状态
- 显示修改和未跟踪文件

#### 5. 搜索功能
- 搜索文本内容
- 搜索文件
- 搜索符号定义

#### 6. 配置管理
- 获取系统配置
- 列出所有提供商
- 显示提供商和模型信息

#### 7. 流式事件订阅
- 订阅实时事件流
- 接收流式响应
- 实时显示 AI 生成内容

#### 8. 会话状态和清理
- 获取会话状态
- 查看待办事项
- 清理演示会话

### 运行方法

```bash
# 基本运行
python demo.py

# 使用自定义服务器地址
python demo.py --base-url http://your-server:8000

# 指定项目目录
python demo.py --directory /path/to/your/project

# 同时指定服务器和目录
python demo.py --base-url http://your-server:8000 --directory /path/to/project
```

### 命令行参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--base-url` | OpenCode 服务器地址 | `http://localhost:8000` | `http://192.168.1.100:8000` |
| `--directory` | 项目目录路径 | `None` | `/home/user/myproject` |

### 输出示例

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
  OpenCode Python SDK - 完整功能演示
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

======================================================================
  演示1: 客户端初始化
======================================================================
ℹ️  服务器地址: http://localhost:8000
ℹ️  项目目录: 未设置
✅ 客户端初始化成功

======================================================================
  演示2: 会话管理
======================================================================
ℹ️  获取现有会话列表...
✅ 找到 5 个现有会话
ℹ️  创建新会话...
✅ 会话创建成功 - ID: abc123...
ℹ️  名称: OpenCode SDK 演示会话
ℹ️  提供商: anthropic
ℹ️  模型: claude-3-5-sonnet-20241022
...

======================================================================
  演示完成
======================================================================
✅ 所有演示已完成！

提示:
  - 查看 examples/ 目录了解更多示例
  - 阅读 README.md 了解完整文档
  - 访问 https://opencode.ai 获取更多信息
```

## 💡 使用技巧

### 1. 环境准备

在运行演示程序之前，请确保：

```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 安装 SDK
pip install -e .

# 确保 OpenCode 服务器正在运行
curl http://localhost:8000/api/health
```

### 2. 自定义配置

如果需要连接到远程服务器或使用特定项目目录：

```bash
# 远程服务器
python demo.py --base-url http://your-server.com:8000

# 指定项目目录
python demo.py --directory /path/to/your/project

# 同时指定
python demo.py --base-url http://your-server.com:8000 --directory /path/to/project
```

### 3. 调试模式

如果遇到问题，可以修改演示代码添加调试信息：

```python
# 在 demo.py 中添加
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 4. 错误处理

演示程序已经包含了完善的错误处理，如果遇到错误：

1. 检查服务器是否运行
2. 验证服务器地址是否正确
3. 确认网络连接正常
4. 查看错误消息获取详细信息

## 📚 相关资源

### 文档

- [README.md](README.md) - 项目概览
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [API_REFERENCE.md](API_REFERENCE.md) - 完整 API 参考
- [BEST_PRACTICES.md](BEST_PRACTICES.md) - 最佳实践

### 示例代码

- [examples/basic_usage.py](examples/basic_usage.py) - 基础用法示例
- [examples/session_usage.py](examples/session_usage.py) - 会话管理示例
- [examples/core_resources_usage.py](examples/core_resources_usage.py) - 核心资源示例
- [examples/event_usage.py](examples/event_usage.py) - 事件订阅示例
- [examples/advanced_resources_usage.py](examples/advanced_resources_usage.py) - 高级功能示例

### 在线资源

- [OpenCode 官网](https://opencode.ai)
- [文档](https://opencode.ai/docs)
- [GitHub 仓库](https://github.com/opencode-ai/opencode)
- [Discord 社区](https://discord.gg/opencode)

## ❓ 常见问题

### Q1: 连接被拒绝

```
ConnectionError: Failed to connect to http://localhost:8000
```

**解决方案**: 确保 OpenCode 服务器已启动

```bash
# 检查服务器状态
curl http://localhost:8000/api/health

# 如果服务器未运行，请启动 OpenCode 服务器
```

### Q2: 导入错误

```
ModuleNotFoundError: No module named 'opencode_sdk'
```

**解决方案**: 安装 SDK

```bash
pip install -e .
```

### Q3: 认证失败

```
AuthenticationError: Invalid credentials
```

**解决方案**: 检查 API 密钥配置（如果需要）

```python
client = OpencodeClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"  # 如果需要
)
```

### Q4: 会话创建失败

**可能原因**:
- 提供商 ID 不正确
- 模型 ID 不正确
- 服务器配置问题

**解决方案**:
1. 检查可用的提供商和模型
2. 使用 `client.providers.list()` 查看可用选项
3. 确保提供商已正确配置

## 🎓 学习路径

### 初学者

1. 运行 `quick_demo.py` 了解基础功能
2. 阅读 [QUICKSTART.md](QUICKSTART.md)
3. 查看 [examples/basic_usage.py](examples/basic_usage.py)

### 进阶用户

1. 运行 `demo.py` 了解所有功能
2. 阅读 [API_REFERENCE.md](API_REFERENCE.md)
3. 查看 [examples/](examples/) 目录中的其他示例
4. 学习流式事件订阅

### 高级用户

1. 阅读 [BEST_PRACTICES.md](BEST_PRACTICES.md)
2. 学习异步编程模式
3. 探索高级功能（MCP、LSP、PTY 等）
4. 参与社区贡献

## 🤝 贡献

如果您发现演示程序有问题或有改进建议：

1. 提交 Issue: [GitHub Issues](https://github.com/opencode-ai/opencode/issues)
2. 提交 Pull Request: [GitHub PR](https://github.com/opencode-ai/opencode/pulls)
3. 加入讨论: [GitHub Discussions](https://github.com/opencode-ai/opencode/discussions)

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
