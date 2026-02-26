"""
OpenCode Python SDK - 快速入门演示

这是一个简化的DEMO，展示最常用的功能：
1. 创建客户端
2. 创建会话
3. 发送消息
4. 获取响应

适合第一次使用SDK的用户快速上手。

使用方法：
    python quick_demo.py
"""

from opencode_sdk import OpencodeClient


def main():
    """快速入门演示"""
    print("=" * 60)
    print("OpenCode Python SDK - 快速入门演示")
    print("=" * 60)
    print()

    # 步骤1: 创建客户端
    print("步骤1: 创建客户端")
    print("-" * 60)
    client = OpencodeClient(
        base_url="http://localhost:8000",
        directory="/path/to/your/project"
    )
    print("✅ 客户端创建成功")
    print(f"   服务器地址: {client._http_client.base_url}")
    print()

    # 步骤2: 创建会话
    print("步骤2: 创建会话")
    print("-" * 60)
    session = client.sessions.create(
        name="快速入门演示",
        provider_id="anthropic",
        model_id="claude-3-5-sonnet-20241022"
    )
    print("✅ 会话创建成功")
    print(f"   会话 ID: {session.id}")
    print(f"   会话名称: {session.name}")
    print()

    # 步骤3: 发送消息
    print("步骤3: 发送消息")
    print("-" * 60)
    response = client.sessions.prompt(
        session.id,
        parts=[{
            "type": "text",
            "text": "你好！请用一句话介绍你自己。"
        }]
    )
    print("✅ 消息发送成功")
    print(f"   消息 ID: {response.id}")
    print(f"   角色: {response.role}")
    if response.parts and len(response.parts) > 0:
        print(f"   回复: {response.parts[0].text}")
    print()

    # 步骤4: 列出所有会话
    print("步骤4: 列出所有会话")
    print("-" * 60)
    sessions = client.sessions.list()
    print(f"✅ 共有 {len(sessions)} 个会话")
    for s in sessions[:5]:
        print(f"   - {s.name} (ID: {s.id})")
    print()

    # 步骤5: 删除会话（可选）
    print("步骤5: 删除会话")
    print("-" * 60)
    client.sessions.delete(session.id)
    print("✅ 会话已删除")
    print()

    # 清理
    client.close()

    print("=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
    print()
    print("下一步：")
    print("  - 运行 python demo.py 查看完整功能演示")
    print("  - 查看 examples/ 目录了解更多示例")
    print("  - 阅读 README.md 了解完整文档")


if __name__ == "__main__":
    main()
