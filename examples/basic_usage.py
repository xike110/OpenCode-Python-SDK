"""OpenCode SDK 基础使用示例。"""

from opencode_sdk import OpencodeClient

# 创建客户端
client = OpencodeClient(
    base_url="http://localhost:8000",
    directory="/path/to/your/project"
)

print("OpenCode Python SDK - 基础使用示例")
print("=" * 50)
print(f"基础 URL: {client._http_client.base_url}")
print(f"目录: {client._http_client.directory}")
print()

# 注意：实际的 API 调用将在后续步骤中实现
# 这只是客户端初始化的演示

# 使用上下文管理器
with OpencodeClient(base_url="http://localhost:8000") as client:
    print("使用上下文管理器创建客户端")
    # 客户端将在退出上下文时自动关闭

print()
print("✅ 客户端初始化成功！")
print()
print("下一步：")
print("- 实现 Session 资源用于创建和管理会话")
print("- 实现 Event 资源用于订阅实时事件")
print("- 实现 File 资源用于文件操作")
