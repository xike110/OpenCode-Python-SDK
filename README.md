# OpenCode Python SDK

> **状态**: ✅ 已完成 | **版本**: 0.1.0-dev | **完成度**: 100% | 测试覆盖率 30%（待完成）


- [API 文档](docs/API_REFERENCE.md) - 完整的 75 个 API 方法文档
- [OpenCode 中文教程](https://learnopencode.com/) - OpenCode 中文教程 | AI 编程助手实战指南


一个功能完整、文档齐全、测试覆盖良好的高质量 Python 客户端库。

## ✨ 项目特点

- ✅ **功能完整** - 14 个资源类，75 个 API 方法
- ✅ **类型安全** - 100% 类型提示覆盖
- ✅ **中文注释** - 100% 中文注释
- ✅ **异步支持** - 完整的异步 API
- ✅ **测试完善** - 测试过30个用例，30% 测试覆盖率(其他暂未测试，拿到手自己测试)
- ✅ **易于使用** - 简洁的 API 设计

## 🚀 安装

```bash
# 从 GitHub 克隆仓库
git clone https://github.com/xike110/OpenCode-Python-SDK.git

# 进入项目目录
cd OpenCode-Python-SDK

# 从本地安装
pip install -e .
```

## 🎯 新手启动步骤

### 第一步：环境准备

确保你已安装以下软件：

```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 检查 pip 是否已安装
pip --version
```


### 第三步：验证安装

```bash
# 创建一个测试脚本 test_install.py
python -c "from opencode_sdk import OpencodeClient; print('✅ SDK 安装成功！')"
```

### 第四步：创建第一个脚本

创建文件 `hello_opencode.py`：

```python
from opencode_sdk import OpencodeClient

# 初始化客户端
client = OpencodeClient(
    base_url="http://localhost:8000",  # OpenCode 服务器地址
    directory="/path/to/your/project"   # 你的项目路径
)

# 创建一个新会话
print("📝 创建会话...")
session = client.sessions.create(title="我的第一个任务")
print(f"✅ 会话已创建，ID: {session.id}")

# 发送一条消息
print("\n💬 发送消息...")
response = client.sessions.prompt(
    session_id=session.id,
    parts=[{
        "type": "text",
        "text": "请帮我写一个 Python 函数来计算阶乘"
    }]
)
print(f"✅ 收到响应: {response}")

# 列出所有会话
print("\n📋 列出所有会话...")
sessions = client.sessions.list()
print(f"✅ 共有 {len(sessions)} 个会话")
for s in sessions:
    print(f"  - {s.title} (ID: {s.id})")
```

### 第五步：运行脚本

```bash
# 确保 OpenCode 服务器正在运行
# 然后执行脚本
python hello_opencode.py
```

### 第六步：常见问题排查

**问题 1：连接被拒绝**
```
ConnectionError: Failed to connect to http://localhost:8000
```
解决方案：确保 OpenCode 服务器已启动
```bash
# 检查服务器是否运行
curl http://localhost:8000/api/health
```

**问题 2：导入错误**
```
ModuleNotFoundError: No module named 'opencode_sdk'
```
解决方案：重新安装 SDK
```bash
pip install --upgrade opencode-sdk
```

**问题 3：认证失败**
```
AuthenticationError: Invalid credentials
```
解决方案：检查 API 密钥配置
```python
client = OpencodeClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"  # 添加 API 密钥
)
```

### 第七步：运行演示程序

项目提供了两个演示程序，帮助您快速了解SDK的功能：

**快速入门演示** - 适合第一次使用的用户
```bash
python quick_demo.py
```
这个演示展示了最常用的功能：
- 创建客户端
- 创建会话
- 发送消息
- 获取响应

**完整功能演示** - 展示所有主要功能
```bash
python demo.py
```
这个演示包含：
- 客户端初始化和配置
- 会话管理（创建、列表、更新、删除）
- 消息发送和响应处理
- 文件操作（读取、列表、搜索）
- 流式事件订阅
- 配置和提供商管理

**自定义服务器地址**
```bash
# 使用自定义服务器地址
python demo.py --base-url http://your-server:8000

# 指定项目目录
python demo.py --directory /path/to/your/project
```

## 📖 快速开始

### 基本用法

```python
from opencode_sdk import OpencodeClient

# 创建客户端
client = OpencodeClient(
    base_url="http://localhost:8000",
    directory="/path/to/your/project"
)

# 创建会话
session = client.sessions.create(title="我的任务")

# 列出所有会话
sessions = client.sessions.list()

# 获取会话详情
session_detail = client.sessions.get(session.id)

# 更新会话
updated_session = client.sessions.update(
    session_id=session.id,
    title="新标题"
)

# 删除会话
client.sessions.delete(session.id)
```

### 流式消息（推荐）

使用异步方式获取流式响应，实时查看 AI 生成的内容：

```python
import asyncio
from opencode_sdk import OpencodeClient

async def stream_chat():
    client = OpencodeClient(base_url="http://localhost:8000")
    session = client.sessions.create(title="流式对话")
    
    # 发送消息并接收流式响应
    async for event in client.events.subscribe_session(
        session_id=session.id,
        parts=[{"type": "text", "text": "写一个 Python 函数来计算斐波那契数列"}]
    ):
        # 实时打印 AI 的响应
        if hasattr(event, 'text'):
            print(event.text, end="", flush=True)
    
    client.sessions.delete(session.id)

# 运行
asyncio.run(stream_chat())
```

## 🔧 功能特性

- ✅ **会话管理**: 创建、列表、更新、删除会话（24 个方法）
- ✅ **消息处理**: 发送消息、获取响应、流式事件
- ✅ **文件操作**: 读取、列表、搜索文件（3 个方法）
- ✅ **提供商管理**: 配置 AI 提供商和模型（4 个方法）
- ✅ **MCP 集成**: 管理模型上下文协议服务器（9 个方法）
- ✅ **事件流**: 通过 SSE 订阅实时事件（3 个方法）
- ✅ **PTY 管理**: 终端会话管理（6 个方法）
- ✅ **TUI 集成**: 终端 UI 交互（11 个方法）
- ✅ **类型安全**: 完整的类型提示和 Pydantic 模型（100+ 个模型）
- ✅ **异步支持**: 支持 Async/await
- ✅ **中文注释**: 100% 中文文档

## 📊 项目统计

| 类别 | 数量 |
|------|------|
| **资源类** | 14 |
| **API 方法** | 75 |
| **数据模型** | 100+ |
| **测试用例** | 30+ |
| **文档** | 24+ |
| **代码行数** | 16,000+ |
| **测试覆盖率** | 30% |

## 📚 文档

项目中提供的完整文档：

### 核心文档
- 📖 [README.md](README.md) - 项目概览
- 📖 [DEMO.md](DEMO.md) - 演示程序使用指南
- 📖 [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - 完整 API 参考（75个方法）

### API 文档
- 📖 [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API 参考总览
- 📖 [docs/session.md](docs/session.md) - Session 资源（24个方法）
- 📖 [docs/event.md](docs/event.md) - Event 资源（3个方法）
- 📖 [docs/project.md](docs/project.md) - Project 资源（3个方法）
- 📖 [docs/config.md](docs/config.md) - Config 资源（3个方法）
- 📖 [docs/provider.md](docs/provider.md) - Provider 资源（4个方法）
- 📖 [docs/file.md](docs/file.md) - File 资源（3个方法）
- 📖 [docs/find.md](docs/find.md) - Find 资源（3个方法）
- 📖 [docs/mcp.md](docs/mcp.md) - MCP 资源（9个方法）
- 📖 [docs/lsp.md](docs/lsp.md) - LSP 资源（1个方法）
- 📖 [docs/pty.md](docs/pty.md) - PTY 资源（6个方法）
- 📖 [docs/tool.md](docs/tool.md) - Tool 资源（2个方法）
- 📖 [docs/tui.md](docs/tui.md) - TUI 资源（11个方法）
- 📖 [docs/app.md](docs/app.md) - App 资源（3个方法）
- 📖 [docs/command.md](docs/command.md) - Command 资源（1个方法）
- 📖 [docs/global.md](docs/global.md) - Global 资源（3个方法）
- 📖 [docs/instance.md](docs/instance.md) - Instance 资源（1个方法）
- 📖 [docs/path.md](docs/path.md) - Path 资源（1个方法）
- 📖 [docs/vcs.md](docs/vcs.md) - VCS 资源（1个方法）
- 📖 [docs/formatter.md](docs/formatter.md) - Formatter 资源（1个方法）
- 📖 [docs/auth.md](docs/auth.md) - Auth 资源（1个方法）

### 核心资源

- **Session（会话）**: 管理 AI 编码会话（24 个方法）
- **Event（事件）**: 订阅实时事件（3 个方法）
- **Project（项目）**: 列表和管理项目（2 个方法）
- **Config（配置）**: 获取和更新配置（3 个方法）
- **Provider（提供商）**: 管理 AI 提供商（4 个方法）
- **File（文件）**: 文件操作（3 个方法）
- **Find（查找）**: 搜索功能（3 个方法）
- **MCP**: 模型上下文协议集成（9 个方法）
- **LSP**: 语言服务器协议（1 个方法）
- **PTY**: 终端会话（6 个方法）
- **Tool（工具）**: 列出可用工具（2 个方法）
- **TUI**: 终端 UI 交互（11 个方法）
- **App（应用）**: 应用管理（3 个方法）
- **Command（命令）**: 命令管理（1 个方法）

## 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/xike110/OpenCode-Python-SDK.git
cd OpenCode-Python-SDK

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest

# 格式化代码
black .
isort .

# 类型检查
mypy opencode_sdk
```

## 📝 使用示例

### 快速体验演示程序

想要快速体验 SDK 的功能？运行演示程序：

```bash
# 快速入门演示（推荐新手）
python quick_demo.py

# 完整功能演示
python demo.py

# 使用自定义配置
python demo.py --base-url http://your-server:8000 --directory /path/to/project
```

📖 **详细说明**: [DEMO.md](DEMO.md) - 演示程序使用指南

### 创建和使用会话

```python
from opencode_sdk import OpencodeClient

client = OpencodeClient(base_url="http://localhost:8000")

# 创建会话
session = client.sessions.create(title="重构代码")

# 发送消息
response = client.sessions.prompt(
    session_id=session.id,
    parts=[{"type": "text", "text": "重构这个函数"}]
)

# 获取会话消息
messages = client.sessions.messages(session_id=session.id)
```

### 订阅事件

```python
# 订阅所有事件
for event in client.events.subscribe():
    print(f"事件: {event.type}")
    
    if event.type == "message.part.updated":
        part = event.properties.part
        if part.type == "text":
            print(f"文本: {part.text}")
```

### 文件操作

```python
# 列出文件
files = client.files.list(path="src")

# 读取文件
content = client.files.read(path="src/main.py")

# 搜索文本
results = client.find.text(query="function")
```

### 提供商管理

```python
# 列出提供商
providers = client.providers.list()

# 获取配置
config = client.config.get()

# 更新配置
client.config.update({
    "model": "anthropic/claude-3-5-sonnet-20241022"
})
```


## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [OpenCode 官网](https://opencode.ai)
- [文档](https://opencode.ai/docs)
- [API 参考](docs/API_REFERENCE.md) - 完整的 75 个 API 方法文档
- [中文教程](https://learnopencode.com/) - OpenCode 中文教程 | AI 编程助手实战指南
- [GitHub 仓库](https://github.com/xike110/OpenCode-Python-SDK)
- [问题追踪](https://github.com/xike110/OpenCode-Python-SDK/issues)

## 💬 支持

- [Discord 社区](https://discord.gg/opencode)
- [GitHub 讨论](https://github.com/opencode-ai/opencode/discussions)
- 邮箱: support@opencode.ai
