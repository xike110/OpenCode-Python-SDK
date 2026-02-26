"""高级功能资源使用示例。"""

import asyncio
from opencode_sdk import OpencodeClient


def mcp_examples():
    """MCP 资源使用示例。"""
    print("=" * 60)
    print("MCP 资源示例")
    print("=" * 60)
    
    client = OpencodeClient(base_url="http://localhost:8000")
    
    # 1. 获取 MCP 服务器状态
    print("\n1. 获取 MCP 服务器状态")
    status = client.mcp.status()
    for name, info in status.items():
        print(f"  {name}: {info.get('status', 'unknown')}")
    
    # 2. 添加本地 MCP 服务器
    print("\n2. 添加本地 MCP 服务器")
    config = {
        "command": "node",
        "args": ["server.js"],
        "env": {"API_KEY": "your_api_key"}
    }
    status = client.mcp.add("my-local-server", config)
    print(f"  添加成功: {status}")
    
    # 3. 添加远程 MCP 服务器
    print("\n3. 添加远程 MCP 服务器")
    config = {
        "url": "https://api.example.com/mcp",
        "headers": {"Authorization": "Bearer token"}
    }
    status = client.mcp.add("my-remote-server", config)
    print(f"  添加成功: {status}")
    
    # 4. 连接 MCP 服务器
    print("\n4. 连接 MCP 服务器")
    success = client.mcp.connect("my-local-server")
    print(f"  连接成功: {success}")
    
    # 5. OAuth 认证流程
    print("\n5. OAuth 认证流程")
    
    # 方式1: 手动流程
    print("  方式1: 手动 OAuth 流程")
    result = client.mcp.auth("github").start()
    print(f"  请访问: {result['authorizationUrl']}")
    # 用户在浏览器中完成认证后，获取授权码
    # auth_code = input("请输入授权码: ")
    # status = client.mcp.auth("github").callback(auth_code)
    # print(f"  认证成功: {status}")
    
    # 方式2: 一键认证（自动打开浏览器）
    print("  方式2: 一键 OAuth 认证")
    # status = client.mcp.auth("github").authenticate()
    # print(f"  认证成功: {status}")
    
    # 6. 移除 OAuth 认证
    print("\n6. 移除 OAuth 认证")
    # result = client.mcp.auth("github").remove()
    # print(f"  移除成功: {result['success']}")
    
    # 7. 断开 MCP 服务器
    print("\n7. 断开 MCP 服务器")
    success = client.mcp.disconnect("my-local-server")
    print(f"  断开成功: {success}")


def lsp_examples():
    """LSP 资源使用示例。"""
    print("\n" + "=" * 60)
    print("LSP 资源示例")
    print("=" * 60)
    
    client = OpencodeClient(base_url="http://localhost:8000")
    
    # 获取 LSP 服务器状态
    print("\n获取 LSP 服务器状态")
    status_list = client.lsp.status()
    for lsp in status_list:
        print(f"  {lsp.get('name', 'unknown')}: {lsp.get('status', 'unknown')}")


def pty_examples():
    """PTY 资源使用示例。"""
    print("\n" + "=" * 60)
    print("PTY 资源示例")
    print("=" * 60)
    
    client = OpencodeClient(base_url="http://localhost:8000")
    
    # 1. 列出所有 PTY 会话
    print("\n1. 列出所有 PTY 会话")
    sessions = client.pty.list()
    for pty in sessions:
        print(f"  {pty['id']}: {pty.get('title', 'untitled')}")
    
    # 2. 创建默认 shell 会话
    print("\n2. 创建默认 shell 会话")
    pty = client.pty.create()
    print(f"  创建成功: {pty['id']}")
    
    # 3. 创建自定义命令会话
    print("\n3. 创建自定义命令会话")
    pty = client.pty.create(
        command="python",
        args=["-m", "http.server", "8000"],
        cwd="/path/to/project",
        title="HTTP Server",
        env={"PORT": "8000"}
    )
    print(f"  创建成功: {pty['id']}")
    pty_id = pty['id']
    
    # 4. 获取 PTY 会话信息
    print("\n4. 获取 PTY 会话信息")
    pty = client.pty.get(pty_id)
    print(f"  标题: {pty.get('title', 'untitled')}")
    
    # 5. 更新 PTY 会话
    print("\n5. 更新 PTY 会话")
    pty = client.pty.update(pty_id, title="新标题")
    print(f"  更新成功: {pty.get('title')}")
    
    # 6. 更新终端大小
    print("\n6. 更新终端大小")
    pty = client.pty.update(pty_id, size={"rows": 30, "cols": 120})
    print(f"  更新成功")
    
    # 7. 连接 PTY 会话（WebSocket）
    print("\n7. 连接 PTY 会话")
    can_connect = client.pty.connect(pty_id)
    print(f"  可以连接: {can_connect}")
    # 实际的 WebSocket 连接需要使用 WebSocket 客户端
    # ws_url = f"ws://localhost:8000/pty/{pty_id}/connect"
    
    # 8. 移除 PTY 会话
    print("\n8. 移除 PTY 会话")
    success = client.pty.remove(pty_id)
    print(f"  移除成功: {success}")


def tool_examples():
    """Tool 资源使用示例。"""
    print("\n" + "=" * 60)
    print("Tool 资源示例")
    print("=" * 60)
    
    client = OpencodeClient(base_url="http://localhost:8000")
    
    # 1. 获取所有工具 ID
    print("\n1. 获取所有工具 ID")
    tool_ids = client.tools.ids()
    for category, ids in tool_ids.items():
        print(f"  {category}: {', '.join(ids)}")
    
    # 2. 获取指定模型的工具列表
    print("\n2. 获取指定模型的工具列表")
    tools = client.tools.list("anthropic", "claude-3-5-sonnet-20241022")
    for tool in tools:
        print(f"  {tool['name']}: {tool.get('description', '')}")


def tui_examples():
    """TUI 资源使用示例。"""
    print("\n" + "=" * 60)
    print("TUI 资源示例")
    print("=" * 60)
    
    client = OpencodeClient(base_url="http://localhost:8000")
    
    # 1. 追加提示文本
    print("\n1. 追加提示文本")
    client.tui.append_prompt("帮我写一个")
    client.tui.append_prompt("Python 函数")
    print("  追加成功")
    
    # 2. 提交提示
    print("\n2. 提交提示")
    success = client.tui.submit_prompt()
    print(f"  提交成功: {success}")
    
    # 3. 清空提示
    print("\n3. 清空提示")
    success = client.tui.clear_prompt()
    print(f"  清空成功: {success}")
    
    # 4. 执行 TUI 命令
    print("\n4. 执行 TUI 命令")
    success = client.tui.execute_command("agent_cycle")
    print(f"  执行成功: {success}")
    
    # 5. 显示提示消息
    print("\n5. 显示提示消息")
    
    # 成功消息
    client.tui.show_toast("操作成功", "success")
    
    # 错误消息
    client.tui.show_toast(
        "操作失败",
        "error",
        title="错误",
        duration=10000
    )
    
    # 警告消息
    client.tui.show_toast("请注意", "warning", title="警告")
    
    # 信息消息
    client.tui.show_toast("这是一条信息", "info")
    
    print("  显示成功")
    
    # 6. 打开对话框
    print("\n6. 打开对话框")
    client.tui.open_help()  # 打开帮助
    client.tui.open_sessions()  # 打开会话列表
    client.tui.open_themes()  # 打开主题列表
    client.tui.open_models()  # 打开模型列表
    print("  打开成功")
    
    # 7. 选择会话
    print("\n7. 选择会话")
    success = client.tui.select_session("ses_123")
    print(f"  选择成功: {success}")
    
    # 8. 发布 TUI 事件
    print("\n8. 发布 TUI 事件")
    event = {
        "type": "tui.prompt.append",
        "text": "Hello"
    }
    success = client.tui.publish(event)
    print(f"  发布成功: {success}")


def app_examples():
    """App 资源使用示例。"""
    print("\n" + "=" * 60)
    print("App 资源示例")
    print("=" * 60)
    
    client = OpencodeClient(base_url="http://localhost:8000")
    
    # 1. 写入日志
    print("\n1. 写入日志")
    
    # 信息日志
    client.app.log("my-service", "info", "操作成功")
    
    # 错误日志
    client.app.log("my-service", "error", "操作失败")
    
    # 带元数据的日志
    client.app.log(
        "my-service",
        "warn",
        "警告信息",
        extra={"user_id": "123", "action": "delete"}
    )
    
    print("  日志写入成功")
    
    # 2. 列出所有代理
    print("\n2. 列出所有代理")
    agents = client.app.agents()
    for agent in agents:
        print(f"  {agent['name']}: {agent.get('description', '')}")
    
    # 3. 列出所有技能
    print("\n3. 列出所有技能")
    skills = client.app.skills()
    for skill in skills:
        print(f"  {skill['name']}: {skill.get('description', '')}")


def command_examples():
    """Command 资源使用示例。"""
    print("\n" + "=" * 60)
    print("Command 资源示例")
    print("=" * 60)
    
    client = OpencodeClient(base_url="http://localhost:8000")
    
    # 列出所有命令
    print("\n列出所有命令")
    commands = client.commands.list()
    for cmd in commands:
        print(f"  {cmd['name']}: {cmd.get('description', '')}")


def comprehensive_example():
    """综合使用示例。"""
    print("\n" + "=" * 60)
    print("综合使用示例")
    print("=" * 60)
    
    client = OpencodeClient(
        base_url="http://localhost:8000",
        directory="/path/to/project"
    )
    
    # 1. 配置 MCP 服务器
    print("\n1. 配置 MCP 服务器")
    mcp_config = {
        "command": "node",
        "args": ["mcp-server.js"]
    }
    client.mcp.add("my-mcp", mcp_config)
    client.mcp.connect("my-mcp")
    print("  MCP 服务器配置完成")
    
    # 2. 创建 PTY 会话
    print("\n2. 创建 PTY 会话")
    pty = client.pty.create(title="开发终端")
    pty_id = pty['id']
    print(f"  PTY 会话创建: {pty_id}")
    
    # 3. 创建会话并发送消息
    print("\n3. 创建会话并发送消息")
    session = client.sessions.create(
        name="开发任务",
        provider_id="anthropic",
        model_id="claude-3-5-sonnet-20241022"
    )
    print(f"  会话创建: {session['id']}")
    
    # 4. 在 TUI 中显示进度
    print("\n4. 在 TUI 中显示进度")
    client.tui.show_toast("任务开始", "info")
    
    # 5. 发送消息
    print("\n5. 发送消息")
    response = client.sessions.prompt(
        session['id'],
        parts=[{"type": "text", "text": "帮我分析这个项目"}]
    )
    print(f"  收到响应: {len(response.get('messages', []))} 条消息")
    
    # 6. 记录日志
    print("\n6. 记录日志")
    client.app.log(
        "dev-task",
        "info",
        "任务完成",
        extra={"session_id": session['id'], "pty_id": pty_id}
    )
    
    # 7. 显示完成提示
    print("\n7. 显示完成提示")
    client.tui.show_toast("任务完成", "success")
    
    # 8. 清理资源
    print("\n8. 清理资源")
    client.pty.remove(pty_id)
    client.mcp.disconnect("my-mcp")
    print("  资源清理完成")


if __name__ == "__main__":
    """运行所有示例。"""
    try:
        # MCP 示例
        mcp_examples()
        
        # LSP 示例
        lsp_examples()
        
        # PTY 示例
        pty_examples()
        
        # Tool 示例
        tool_examples()
        
        # TUI 示例
        tui_examples()
        
        # App 示例
        app_examples()
        
        # Command 示例
        command_examples()
        
        # 综合示例
        comprehensive_example()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {e}")
        print("请确保 OpenCode 服务器正在运行")
