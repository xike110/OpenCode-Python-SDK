"""Event 资源使用示例。"""

import asyncio
from opencode_sdk import OpencodeClient

# 创建客户端
client = OpencodeClient(
    base_url="http://localhost:8000",
    directory="/path/to/your/project"
)

print("=" * 60)
print("OpenCode Python SDK - Event 资源使用示例")
print("=" * 60)
print()


# ==================== 示例 1: 订阅全局事件 ====================
async def example_subscribe_global():
    """订阅全局事件。"""
    print("示例 1: 订阅全局事件")
    print("-" * 60)
    
    try:
        print("开始监听全局事件...")
        print("（按 Ctrl+C 停止）")
        print()
        
        event_count = 0
        async for event in client.events.subscribe():
            event_count += 1
            print(f"[{event_count}] 收到事件: {event.type}")
            
            # 根据事件类型显示详细信息
            if event.type == "session:created":
                print(f"    新会话创建: {event.info.name if hasattr(event, 'info') else 'N/A'}")
            elif event.type == "session:updated":
                print(f"    会话更新: {event.info.id if hasattr(event, 'info') else 'N/A'}")
            elif event.type == "session:deleted":
                print(f"    会话删除: {event.info.id if hasattr(event, 'info') else 'N/A'}")
            
            # 限制显示数量（演示用）
            if event_count >= 10:
                print()
                print("已接收 10 个事件，停止监听")
                break
                
    except KeyboardInterrupt:
        print()
        print("用户中断")
    except Exception as e:
        print(f"错误: {e}")
    
    print()


# ==================== 示例 2: 异步发送消息并接收响应 ====================
async def example_prompt_async():
    """异步发送消息并接收流式响应。"""
    print("示例 2: 异步发送消息并接收流式响应")
    print("-" * 60)
    
    try:
        # 首先创建一个会话
        session = client.sessions.create(
            name="异步测试会话",
            provider_id="anthropic",
            model_id="claude-3-5-sonnet-20241022"
        )
        print(f"✅ 创建会话: {session.id}")
        print()
        
        # 发送消息并接收流式响应
        print("发送消息: '请用一句话介绍你自己'")
        print("AI 回复: ", end="", flush=True)
        
        full_response = ""
        async for event in client.sessions.prompt_async(
            session.id,
            parts=[{"type": "text", "text": "请用一句话介绍你自己"}]
        ):
            # 处理不同类型的事件
            if event.type == "text":
                # 文本内容
                text = event.text if hasattr(event, 'text') else ""
                print(text, end="", flush=True)
                full_response += text
            elif event.type == "tool_use":
                # 工具调用
                print(f"\n[工具调用: {event.name if hasattr(event, 'name') else 'N/A'}]", end="", flush=True)
            elif event.type == "done":
                # 完成
                print()
                print()
                print("✅ 响应完成")
                break
            elif event.type == "error":
                # 错误
                print()
                print(f"❌ 错误: {event.message if hasattr(event, 'message') else 'Unknown'}")
                break
        
        print()
        print(f"完整响应长度: {len(full_response)} 字符")
        
    except Exception as e:
        print(f"错误: {e}")
    
    print()


# ==================== 示例 3: 订阅特定会话的事件 ====================
async def example_subscribe_session():
    """订阅特定会话的事件。"""
    print("示例 3: 订阅特定会话的事件")
    print("-" * 60)
    
    try:
        # 获取第一个会话
        sessions = client.sessions.list()
        if not sessions:
            print("没有可用的会话")
            return
        
        session_id = sessions[0].id
        print(f"监听会话: {session_id}")
        print()
        
        # 订阅会话事件
        event_count = 0
        async for event in client.events.subscribe(session_id=session_id):
            event_count += 1
            print(f"[{event_count}] 会话事件: {event.type}")
            
            # 限制显示数量
            if event_count >= 5:
                print()
                print("已接收 5 个事件，停止监听")
                break
                
    except Exception as e:
        print(f"错误: {e}")
    
    print()


# ==================== 示例 4: 处理多种事件类型 ====================
async def example_handle_multiple_events():
    """处理多种事件类型。"""
    print("示例 4: 处理多种事件类型")
    print("-" * 60)
    
    try:
        # 创建会话
        session = client.sessions.create(
            name="多事件测试",
            provider_id="anthropic",
            model_id="claude-3-5-sonnet-20241022"
        )
        print(f"✅ 创建会话: {session.id}")
        print()
        
        # 发送一个可能触发多种事件的消息
        print("发送消息: '列出当前目录的文件'")
        print()
        
        async for event in client.sessions.prompt_async(
            session.id,
            parts=[{"type": "text", "text": "列出当前目录的文件"}]
        ):
            # 根据事件类型处理
            if event.type == "text":
                print(f"📝 文本: {event.text if hasattr(event, 'text') else ''}", end="")
            elif event.type == "tool_use":
                print(f"\n🔧 工具调用: {event.name if hasattr(event, 'name') else 'N/A'}")
                if hasattr(event, 'input'):
                    print(f"   参数: {event.input}")
            elif event.type == "tool_result":
                print(f"✅ 工具结果: {event.content if hasattr(event, 'content') else 'N/A'}")
            elif event.type == "thinking":
                print(f"\n💭 思考中...")
            elif event.type == "done":
                print()
                print()
                print("✅ 完成")
                break
            elif event.type == "error":
                print()
                print(f"❌ 错误: {event.message if hasattr(event, 'message') else 'Unknown'}")
                break
                
    except Exception as e:
        print(f"错误: {e}")
    
    print()


# ==================== 示例 5: 错误处理 ====================
async def example_error_handling():
    """演示错误处理。"""
    print("示例 5: 错误处理")
    print("-" * 60)
    
    try:
        # 尝试订阅不存在的会话
        print("尝试订阅不存在的会话...")
        
        async for event in client.events.subscribe(session_id="invalid_session_id"):
            print(f"收到事件: {event.type}")
            break
            
    except Exception as e:
        print(f"✅ 捕获到预期的错误: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
    
    print()


# ==================== 主函数 ====================
async def main():
    """主函数。"""
    print("注意: 这些示例需要 OpenCode 服务器正在运行")
    print()
    
    # 运行示例（根据需要取消注释）
    
    # 示例 1: 订阅全局事件（会持续运行）
    # await example_subscribe_global()
    
    # 示例 2: 异步发送消息
    # await example_prompt_async()
    
    # 示例 3: 订阅会话事件
    # await example_subscribe_session()
    
    # 示例 4: 处理多种事件类型
    # await example_handle_multiple_events()
    
    # 示例 5: 错误处理
    # await example_error_handling()
    
    print("=" * 60)
    print("提示:")
    print("- 取消注释上面的示例函数来运行")
    print("- 确保 OpenCode 服务器正在运行")
    print("- 某些示例需要有效的会话")
    print("=" * 60)


# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
