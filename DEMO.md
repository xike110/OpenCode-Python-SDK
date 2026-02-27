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
stream_chat_test.py 
```

### 输出示例

```
创建会话...
会话已创建: ses_3622e0964ffewInt5rWC2YT24P

问题：当前什么时间？
AI 响应:

程序你好老板
当前日期：2026-02-27
若需精确的当地时间，请告知你的时区或所在城市，我可以给出对应的具体时间。

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
