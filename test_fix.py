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
