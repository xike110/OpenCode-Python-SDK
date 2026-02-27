"""触发全局事件的测试脚本"""
import asyncio
from opencode_sdk import OpencodeClient


async def main():
    # 创建客户端
    client = OpencodeClient(
        base_url="http://192.168.77.28:8001",
        directory="/data/seo/workspace"
    )
    
    print("创建测试会话以触发全局事件...")
    
    # 创建一个新会话（这会触发 session.created 事件）
    session = client.sessions.create(
        name="测试会话",
        directory="/data/seo/workspace"
    )
    print(f"✓ 创建会话: {session.id}")
    
    await asyncio.sleep(1)
    
    # 更新会话（这会触发 session.updated 事件）
    client.sessions.update(
        session_id=session.id,
        name="更新后的测试会话"
    )
    print(f"✓ 更新会话: {session.id}")
    
    await asyncio.sleep(1)
    
    # 删除会话（这会触发 session.deleted 事件）
    client.sessions.delete(session_id=session.id)
    print(f"✓ 删除会话: {session.id}")
    
    print("\n事件已触发，请查看 event_demo.py 的输出")


if __name__ == "__main__":
    asyncio.run(main())
