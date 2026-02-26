"""核心资源使用示例。

演示 Project、Config、Provider、File 和 Find 资源的使用。
"""

from opencode_sdk import OpencodeClient

# 创建客户端
client = OpencodeClient(
    base_url="http://localhost:8000",
    directory="/path/to/your/project"
)

print("=" * 60)
print("OpenCode Python SDK - 核心资源使用示例")
print("=" * 60)
print()

# ==================== 1. Project 资源 ====================
print("1. Project 资源 - 项目管理")
print("-" * 60)

try:
    # 列出所有项目
    projects = client.projects.list()
    print(f"找到 {len(projects)} 个项目:")
    for project in projects[:3]:  # 只显示前3个
        print(f"  - {project.get('name', 'N/A')}: {project.get('path', 'N/A')}")
    
    # 获取当前项目
    current_project = client.projects.current()
    print(f"\n当前项目:")
    print(f"  名称: {current_project.get('name', 'N/A')}")
    print(f"  路径: {current_project.get('path', 'N/A')}")
    
except Exception as e:
    print(f"错误: {e}")

print()

# ==================== 2. Config 资源 ====================
print("2. Config 资源 - 配置管理")
print("-" * 60)

try:
    # 获取配置
    config = client.config.get()
    print(f"当前配置:")
    print(f"  默认提供商: {config.default_provider_id}")
    print(f"  默认模型: {config.default_model_id}")
    print(f"  代理: {config.agent_id if config.agent_id else '未设置'}")
    
    # 列出提供商配置
    providers_config = client.config.providers()
    print(f"\n已配置的提供商: {len(providers_config)} 个")
    for provider in providers_config[:3]:
        print(f"  - {provider.get('id', 'N/A')}: {provider.get('name', 'N/A')}")
    
    # 更新配置（示例，取消注释以执行）
    # updated_config = client.config.update(
    #     default_provider_id="anthropic",
    #     default_model_id="claude-3-5-sonnet-20241022"
    # )
    # print(f"\n✅ 配置已更新")
    
except Exception as e:
    print(f"错误: {e}")

print()

# ==================== 3. Provider 资源 ====================
print("3. Provider 资源 - 提供商管理")
print("-" * 60)

try:
    # 列出所有提供商
    providers = client.providers.list()
    print(f"可用的提供商: {len(providers)} 个")
    for provider in providers:
        print(f"\n  📦 {provider.id}: {provider.name}")
        print(f"     模型数量: {len(provider.models)}")
        # 显示前3个模型
        for model in provider.models[:3]:
            print(f"       - {model.id}")
    
    # 获取认证方法
    auth_methods = client.providers.auth()
    print(f"\n认证方法:")
    for provider_id, methods in list(auth_methods.items())[:3]:
        print(f"  {provider_id}:")
        for method in methods:
            print(f"    - {method.type}")
    
except Exception as e:
    print(f"错误: {e}")

print()

# ==================== 4. File 资源 ====================
print("4. File 资源 - 文件操作")
print("-" * 60)

try:
    # 列出当前目录的文件
    files = client.files.list(path=".")
    print(f"当前目录的文件: {len(files)} 个")
    for file in files[:5]:  # 只显示前5个
        file_type = "📁" if file.is_directory else "📄"
        print(f"  {file_type} {file.name}")
    
    # 读取文件（示例）
    # content = client.files.read("README.md")
    # print(f"\nREADME.md 内容:")
    # print(content.content[:200] + "...")
    
    # 获取文件状态
    status = client.files.status()
    print(f"\n文件状态:")
    print(f"  修改的文件: {len(status.get('modified', []))} 个")
    print(f"  未跟踪的文件: {len(status.get('untracked', []))} 个")
    
except Exception as e:
    print(f"错误: {e}")

print()

# ==================== 5. Find 资源 ====================
print("5. Find 资源 - 搜索功能")
print("-" * 60)

try:
    # 搜索文本
    print("搜索 'TODO':")
    results = client.find.text("TODO", max_results=5)
    print(f"找到 {len(results)} 个结果:")
    for result in results[:3]:
        print(f"  📄 {result.get('path', 'N/A')}:{result.get('line', 'N/A')}")
        print(f"     {result.get('text', 'N/A')[:60]}...")
    
    # 搜索文件
    print(f"\n搜索文件 '*.py':")
    files = client.find.files("*.py", max_results=5)
    print(f"找到 {len(files)} 个文件:")
    for file in files[:3]:
        print(f"  📄 {file.get('path', 'N/A')}")
    
    # 搜索符号
    print(f"\n搜索符号 'main':")
    symbols = client.find.symbols("main", max_results=5)
    print(f"找到 {len(symbols)} 个符号:")
    for symbol in symbols[:3]:
        print(f"  🔧 {symbol.get('name', 'N/A')} ({symbol.get('kind', 'N/A')})")
        print(f"     位置: {symbol.get('path', 'N/A')}")
    
except Exception as e:
    print(f"错误: {e}")

print()

# ==================== 6. 综合示例：创建会话并使用配置 ====================
print("6. 综合示例：创建会话并使用配置")
print("-" * 60)

try:
    # 获取配置
    config = client.config.get()
    
    # 使用配置创建会话
    session = client.sessions.create(
        name="综合示例会话",
        provider_id=config.default_provider_id,
        model_id=config.default_model_id
    )
    print(f"✅ 创建会话成功:")
    print(f"  会话 ID: {session.id}")
    print(f"  提供商: {session.provider_id}")
    print(f"  模型: {session.model_id}")
    
    # 搜索项目中的文件
    files = client.find.files("*.md", max_results=3)
    if files:
        print(f"\n找到 {len(files)} 个 Markdown 文件:")
        for file in files:
            print(f"  - {file.get('path', 'N/A')}")
    
    # 读取第一个文件（如果存在）
    if files:
        first_file = files[0].get('path')
        content = client.files.read(first_file)
        print(f"\n读取文件: {first_file}")
        print(f"  行数: {len(content.content.splitlines())}")
        print(f"  大小: {len(content.content)} 字节")
    
except Exception as e:
    print(f"错误: {e}")

print()

# ==================== 7. OAuth 认证示例 ====================
print("7. OAuth 认证示例（演示）")
print("-" * 60)

try:
    # 注意：这只是演示，实际使用需要浏览器交互
    print("OAuth 认证流程:")
    print("  1. 调用 client.providers.oauth.authorize(provider_id)")
    print("  2. 用户在浏览器中完成授权")
    print("  3. 调用 client.providers.oauth.callback(provider_id, code)")
    print()
    print("示例代码:")
    print("  # 启动授权")
    print("  result = client.providers.oauth.authorize('github')")
    print("  print(f'请访问: {result[\"url\"]}')")
    print()
    print("  # 处理回调")
    print("  result = client.providers.oauth.callback('github', code='...')")
    
except Exception as e:
    print(f"错误: {e}")

print()

print("=" * 60)
print("✅ 示例完成!")
print("=" * 60)
print()
print("提示:")
print("- 确保 OpenCode 服务器正在运行")
print("- 某些操作可能需要有效的项目和配置")
print("- 查看各个资源的文档了解更多详情")
