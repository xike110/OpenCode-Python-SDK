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
