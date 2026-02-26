"""Session 资源使用示例。"""

from opencode_sdk import OpencodeClient

# 创建客户端
client = OpencodeClient(
    base_url="http://localhost:8000",
    directory="/path/to/your/project"
)

print("=" * 60)
print("OpenCode Python SDK - Session 资源使用示例")
print("=" * 60)
print()

# ==================== 1. 列出所有会话 ====================
print("1. 列出所有会话")
print("-" * 60)
try:
    sessions = client.sessions.list()
    print(f"找到 {len(sessions)} 个会话:")
    for session in sessions[:5]:  # 只显示前5个
        print(f"  - {session.id}: {session.name}")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 2. 创建新会话 ====================
print("2. 创建新会话")
print("-" * 60)
try:
    new_session = client.sessions.create(
        name="Python SDK 测试会话",
        provider_id="anthropic",
        model_id="claude-3-5-sonnet-20241022"
    )
    print(f"✅ 创建成功!")
    print(f"  会话 ID: {new_session.id}")
    print(f"  会话名称: {new_session.name}")
    print(f"  提供商: {new_session.provider_id}")
    print(f"  模型: {new_session.model_id}")
    
    # 保存会话 ID 供后续使用
    session_id = new_session.id
except Exception as e:
    print(f"错误: {e}")
    # 如果创建失败，使用一个示例 ID
    session_id = "example_session_id"
print()

# ==================== 3. 获取会话详情 ====================
print("3. 获取会话详情")
print("-" * 60)
try:
    session = client.sessions.get(session_id)
    print(f"会话信息:")
    print(f"  ID: {session.id}")
    print(f"  名称: {session.name}")
    print(f"  创建时间: {session.created_at}")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 4. 发送消息 ====================
print("4. 发送消息到会话")
print("-" * 60)
try:
    response = client.sessions.prompt(
        session_id,
        parts=[{
            "type": "text",
            "text": "你好！请简单介绍一下你自己。"
        }]
    )
    print(f"✅ 消息发送成功!")
    print(f"  消息 ID: {response.id}")
    print(f"  角色: {response.role}")
    if response.parts and len(response.parts) > 0:
        print(f"  回复: {response.parts[0].text[:100]}...")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 5. 获取消息列表 ====================
print("5. 获取消息列表")
print("-" * 60)
try:
    messages = client.sessions.messages(session_id, limit=5)
    print(f"最近 {len(messages)} 条消息:")
    for msg in messages:
        role_emoji = "👤" if msg.role == "user" else "🤖"
        text_preview = msg.parts[0].text[:50] if msg.parts else ""
        print(f"  {role_emoji} {msg.role}: {text_preview}...")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 6. 执行命令 ====================
print("6. 执行命令")
print("-" * 60)
try:
    result = client.sessions.command(
        session_id,
        name="search",
        args={"query": "TODO"}
    )
    print(f"✅ 命令执行成功!")
    print(f"  结果: {result.parts[0].text[:100] if result.parts else 'N/A'}...")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 7. 获取会话状态 ====================
print("7. 获取会话状态")
print("-" * 60)
try:
    statuses = client.sessions.status(session_id)
    if session_id in statuses:
        status = statuses[session_id]
        print(f"会话状态:")
        print(f"  状态: {status.status}")
        print(f"  消息数量: {status.message_count}")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 8. 获取文件差异 ====================
print("8. 获取文件差异")
print("-" * 60)
try:
    diffs = client.sessions.diff(session_id)
    if diffs:
        print(f"找到 {len(diffs)} 个文件差异:")
        for diff in diffs[:3]:  # 只显示前3个
            print(f"  📄 {diff.path}")
            print(f"     +{diff.additions} -{diff.deletions}")
    else:
        print("  没有文件差异")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 9. 获取待办事项 ====================
print("9. 获取待办事项")
print("-" * 60)
try:
    todos = client.sessions.todo(session_id)
    if todos:
        print(f"找到 {len(todos)} 个待办事项:")
        for todo in todos:
            checkbox = "☑" if todo.completed else "☐"
            print(f"  {checkbox} {todo.text}")
    else:
        print("  没有待办事项")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 10. 分享会话 ====================
print("10. 分享会话")
print("-" * 60)
try:
    shared_session = client.sessions.share(session_id)
    print(f"✅ 会话已分享!")
    if hasattr(shared_session, 'share_url'):
        print(f"  分享链接: {shared_session.share_url}")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 11. 获取子会话 ====================
print("11. 获取子会话")
print("-" * 60)
try:
    children = client.sessions.children(session_id)
    if children:
        print(f"找到 {len(children)} 个子会话:")
        for child in children:
            print(f"  - {child.id}: {child.name}")
    else:
        print("  没有子会话")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 12. 更新会话 ====================
print("12. 更新会话")
print("-" * 60)
try:
    updated_session = client.sessions.update(
        session_id,
        name="Python SDK 测试会话（已更新）"
    )
    print(f"✅ 会话已更新!")
    print(f"  新名称: {updated_session.name}")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 13. 总结会话 ====================
print("13. 总结会话")
print("-" * 60)
try:
    summary = client.sessions.summarize(session_id)
    print(f"✅ 会话摘要:")
    print(f"  {summary.summary}")
except Exception as e:
    print(f"错误: {e}")
print()

# ==================== 14. 删除会话（可选） ====================
print("14. 删除会话（可选）")
print("-" * 60)
# 取消注释以下代码来删除会话
# try:
#     client.sessions.delete(session_id)
#     print(f"✅ 会话已删除!")
# except Exception as e:
#     print(f"错误: {e}")
print("  （已跳过删除操作）")
print()

print("=" * 60)
print("✅ 示例完成!")
print("=" * 60)
print()
print("提示:")
print("- 确保 OpenCode 服务器正在运行（http://localhost:8000）")
print("- 某些操作可能需要有效的会话 ID")
print("- 查看 API 文档了解更多详情")
