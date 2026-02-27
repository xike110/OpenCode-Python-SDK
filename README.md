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

### 同步发行消息

创建文件 `hello_opencode.py`：

```python
from opencode_sdk import OpencodeClient

# 初始化客户端 - 使用 /api 前缀
client = OpencodeClient(
    base_url="http://192.168.77.28:8001",
    directory="/data/seo/workspace"
)

# 创建一个新会话
print("📝 创建会话...")
session = client.sessions.create(title="测试会话")
print(f"✅ 会话已创建，ID: {session.id}")

# 发送一条消息
print("\n💬 发送消息...")
response = client.sessions.prompt(
    session_id=session.id,
    parts=[{"type": "text", "text": "当前时间"}],
    agent="build",
    model={
        "modelID": "gpt-5-nano",
        "providerID": "opencode"
    },
    variant="low"
)

print(f"✅ 收到响应!")
print(f"消息ID: {response.id}")
print(f"角色: {response.role}")
print(f"时间: {response.time}")
print(f"模型: {response.model_id} ({response.provider_id})")
print(f"令牌: 输入={response.tokens.input}, 输出={response.tokens.output}, 推理={response.tokens.reasoning}")
print(f"部分 ({len(response.parts)}):")
for i, part in enumerate(response.parts):
    print(f"  [{i}] 类型: {part.type}")
    if hasattr(part, 'text') and part.text:
        text_preview = part.text[:100] + "..." if len(part.text) > 100 else part.text
        print(f"      文本: {text_preview}")
    if hasattr(part, 'reason'):
        print(f"      原因: {part.reason}")
    print(f"      ID: {part.id}")
print()


# 列出所有会话
print("\n📋 列出所有会话...")
sessions = client.sessions.list()
print(f"✅ 共有 {len(sessions)} 个会话")
for s in sessions[:5]:  # 只显示前5个
    print(f"  - {s.title} (ID: {s.id})")

```


### 流式消息（推荐）

使用异步方式获取流式响应，实时查看 AI 生成的内容：

```python
import asyncio
from opencode_sdk import OpencodeClient


async def stream_chat():
    # 使用你的服务器地址
    client = OpencodeClient(base_url="http://192.168.77.28:8001")
    
    print("创建会话...")
    # 创建会话
    session = client.sessions.create(
        title="流式对话",
        directory="/data/seo/workspace"
    )
    
    print(f"会话已创建: {session.id}\n")
    print("AI 响应:\n")
    
    # 发送消息并接收流式响应
    try:
        async for event in client.events.subscribe_session(
            session_id=session.id,
            parts=[{"type": "text", "text": "当前时间"}],
            directory="/data/seo/workspace",
            agent="build",
            model={
                "modelID": "gpt-5-nano",
                "providerID": "opencode"
            },
            variant="low"
        ):
            # 只打印流式文本的增量
            if event.type == "message.part.delta":
                print(event.properties.delta, end="", flush=True)
    except Exception as e:
        print(f"\n\n错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n\n会话完成，正在清理...")
    client.sessions.delete(session.id)


# 运行
asyncio.run(stream_chat())
```

### 订阅方式

SDK 提供三种事件订阅方式，均返回异步迭代器：

#### 1. subscribe_session - 订阅会话事件

订阅特定会话的事件流，可发送消息并接收实时响应：

```python
async for event in client.events.subscribe_session(
    session_id="session_id",
    parts=[{"type": "text", "text": "消息内容"}],
    agent="build",
    model={"modelID": "gpt-5-nano", "providerID": "opencode"},
    variant="low"
):
    if event.type == "message.part.delta":
        print(event.properties.delta, end="", flush=True)
```

**参数说明：**
- `session_id` (str) - 会话 ID
- `parts` (list) - 消息部分列表，每部分包含 `type` 和内容
- `agent` (str) - 代理名称（如 "build"）
- `model` (dict) - 模型配置，包含 `modelID` 和 `providerID`
- `variant` (str) - 变体级别（"low"/"medium"/"high"）

#### 2. subscribe_global - 订阅全局事件

订阅服务器全局事件：

```python
async for event in client.events.subscribe_global():
    if event.payload.type == "session.created":
        print(f"新会话创建: {event.payload.properties.info}")
```

**返回值：** `AsyncIterator[GlobalEvent]`

#### 3. subscribe - 通用订阅

订阅事件流（可选指定会话 ID）：

```python
# 订阅全局事件
async for event in client.events.subscribe():
    print(f"事件: {event.type}")

# 订阅特定会话事件
async for event in client.events.subscribe(session_id="session_id"):
    print(f"会话事件: {event.type}")
```

**返回值：** `AsyncIterator[Event]`

### 常用事件类型

| 事件类型 | 说明 | 属性访问 |
|---------|------|---------|
| `message.part.delta` | 流式文本增量 | `event.properties.delta` |
| `message.part.updated` | 消息部分更新 | `event.properties.part` |
| `session.status` | 会话状态变化 | `event.properties.status` |
| `session.created` | 会话已创建 | `event.properties.info` |
| `session.error` | 会话错误 | `event.properties.error` |
| `file.edited` | 文件已编辑 | `event.properties.file` |

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
