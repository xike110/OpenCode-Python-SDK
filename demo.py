"""
OpenCode Python SDK - 完整功能演示

这个DEMO展示了OpenCode SDK的主要功能，包括：
1. 客户端初始化和配置
2. 会话管理（创建、列表、更新、删除）
3. 消息发送和响应处理
4. 文件操作（读取、列表、搜索）
5. 流式事件订阅
6. 配置和提供商管理

使用方法：
    python demo.py

前提条件：
    - OpenCode 服务器正在运行（默认 http://localhost:8000）
    - 已安装 opencode_sdk 包
"""

import asyncio
import sys
from typing import Optional

try:
    from opencode_sdk import OpencodeClient
except ImportError:
    print("错误: 未找到 opencode_sdk 包")
    print("请先安装: pip install -e .")
    sys.exit(1)


class OpenCodeDemo:
    """OpenCode SDK 功能演示类"""

    def __init__(self, base_url: str = "http://localhost:8000", directory: Optional[str] = None):
        """
        初始化演示类

        Args:
            base_url: OpenCode 服务器地址
            directory: 项目目录路径
        """
        self.client = OpencodeClient(base_url=base_url, directory=directory)
        self.session_id: Optional[str] = None

    def print_section(self, title: str):
        """打印章节标题"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)

    def print_success(self, message: str):
        """打印成功消息"""
        print(f"✅ {message}")

    def print_info(self, message: str):
        """打印信息消息"""
        print(f"ℹ️  {message}")

    def print_error(self, message: str):
        """打印错误消息"""
        print(f"❌ {message}")

    def demo_client_initialization(self):
        """演示1: 客户端初始化"""
        self.print_section("演示1: 客户端初始化")

        try:
            self.print_info(f"服务器地址: {self.client._http_client.base_url}")
            self.print_info(f"项目目录: {self.client._http_client.directory or '未设置'}")
            self.print_success("客户端初始化成功")
        except Exception as e:
            self.print_error(f"客户端初始化失败: {e}")

    def demo_session_management(self):
        """演示2: 会话管理"""
        self.print_section("演示2: 会话管理")

        try:
            # 列出所有会话
            self.print_info("获取现有会话列表...")
            sessions = self.client.sessions.list()
            self.print_success(f"找到 {len(sessions)} 个现有会话")

            # 创建新会话
            self.print_info("创建新会话...")
            new_session = self.client.sessions.create(
                name="OpenCode SDK 演示会话",
                provider_id="anthropic",
                model_id="claude-3-5-sonnet-20241022"
            )
            self.session_id = new_session.id
            self.print_success(f"会话创建成功 - ID: {new_session.id}")
            self.print_info(f"  名称: {new_session.name}")
            self.print_info(f"  提供商: {new_session.provider_id}")
            self.print_info(f"  模型: {new_session.model_id}")

            # 获取会话详情
            self.print_info("获取会话详情...")
            session_detail = self.client.sessions.get(self.session_id)
            self.print_info(f"  创建时间: {session_detail.created_at}")

            # 更新会话
            self.print_info("更新会话名称...")
            updated_session = self.client.sessions.update(
                self.session_id,
                name="OpenCode SDK 演示会话（已更新）"
            )
            self.print_success(f"会话已更新 - 新名称: {updated_session.name}")

        except Exception as e:
            self.print_error(f"会话管理操作失败: {e}")

    def demo_message_handling(self):
        """演示3: 消息处理"""
        self.print_section("演示3: 消息处理")

        if not self.session_id:
            self.print_error("没有可用的会话 ID")
            return

        try:
            # 发送消息
            self.print_info("发送消息到会话...")
            response = self.client.sessions.prompt(
                self.session_id,
                parts=[{
                    "type": "text",
                    "text": "你好！请用一句话介绍你自己。"
                }]
            )
            self.print_success(f"消息发送成功 - 消息 ID: {response.id}")
            self.print_info(f"  角色: {response.role}")

            # 获取消息列表
            self.print_info("获取会话消息列表...")
            messages = self.client.sessions.messages(self.session_id, limit=5)
            self.print_success(f"找到 {len(messages)} 条消息")

            for i, msg in enumerate(messages[-3:], 1):
                role_emoji = "👤" if msg.role == "user" else "🤖"
                text_preview = msg.parts[0].text[:50] if msg.parts else ""
                print(f"  {i}. {role_emoji} {msg.role}: {text_preview}...")

        except Exception as e:
            self.print_error(f"消息处理操作失败: {e}")

    def demo_file_operations(self):
        """演示4: 文件操作"""
        self.print_section("演示4: 文件操作")

        try:
            # 列出当前目录文件
            self.print_info("列出当前目录文件...")
            files = self.client.files.list(path=".")
            self.print_success(f"找到 {len(files)} 个文件/目录")

            for file in files[:5]:
                file_type = "📁" if file.is_directory else "📄"
                print(f"  {file_type} {file.name}")

            # 获取文件状态
            self.print_info("获取文件状态...")
            status = self.client.files.status()
            modified_count = len(status.get('modified', []))
            untracked_count = len(status.get('untracked', []))
            self.print_info(f"  修改的文件: {modified_count} 个")
            self.print_info(f"  未跟踪的文件: {untracked_count} 个")

        except Exception as e:
            self.print_error(f"文件操作失败: {e}")

    def demo_search_functionality(self):
        """演示5: 搜索功能"""
        self.print_section("演示5: 搜索功能")

        try:
            # 搜索文本
            self.print_info("搜索文本 'TODO'...")
            text_results = self.client.find.text("TODO", max_results=3)
            self.print_success(f"找到 {len(text_results)} 个文本匹配")

            for result in text_results[:3]:
                print(f"  📄 {result.get('path', 'N/A')}:{result.get('line', 'N/A')}")
                preview = result.get('text', 'N/A')[:50]
                print(f"     {preview}...")

            # 搜索文件
            self.print_info("搜索 Python 文件 '*.py'...")
            file_results = self.client.find.files("*.py", max_results=3)
            self.print_success(f"找到 {len(file_results)} 个 Python 文件")

            for file in file_results[:3]:
                print(f"  📄 {file.get('path', 'N/A')}")

        except Exception as e:
            self.print_error(f"搜索功能失败: {e}")

    def demo_config_management(self):
        """演示6: 配置管理"""
        self.print_section("演示6: 配置管理")

        try:
            # 获取配置
            self.print_info("获取系统配置...")
            config = self.client.config.get()
            self.print_success("配置获取成功")
            self.print_info(f"  默认提供商: {config.default_provider_id or '未设置'}")
            self.print_info(f"  默认模型: {config.default_model_id or '未设置'}")

            # 列出提供商
            self.print_info("列出所有提供商...")
            providers = self.client.providers.list()
            self.print_success(f"找到 {len(providers)} 个提供商")

            for provider in providers[:3]:
                print(f"  📦 {provider.id}: {provider.name}")
                print(f"     模型数量: {len(provider.models)}")

        except Exception as e:
            self.print_error(f"配置管理失败: {e}")

    async def demo_streaming_events(self):
        """演示7: 流式事件订阅"""
        self.print_section("演示7: 流式事件订阅")

        if not self.session_id:
            self.print_error("没有可用的会话 ID")
            return

        try:
            self.print_info("订阅流式事件...")
            self.print_info("发送消息并接收实时响应...")

            event_count = 0
            async for event in self.client.events.subscribe_session(
                session_id=self.session_id,
                parts=[{
                    "type": "text",
                    "text": "请用简短的语言说明 Python 的三个主要特性。"
                }]
            ):
                event_count += 1

                if hasattr(event, 'text') and event.text:
                    print(f"  📝 {event.text}", end="", flush=True)

                if event_count > 50:
                    break

            print("\n")
            self.print_success(f"流式事件订阅完成，共接收 {event_count} 个事件")

        except Exception as e:
            self.print_error(f"流式事件订阅失败: {e}")

    def demo_session_status_and_cleanup(self):
        """演示8: 会话状态和清理"""
        self.print_section("演示8: 会话状态和清理")

        if not self.session_id:
            self.print_error("没有可用的会话 ID")
            return

        try:
            # 获取会话状态
            self.print_info("获取会话状态...")
            statuses = self.client.sessions.status(self.session_id)
            if self.session_id in statuses:
                status = statuses[self.session_id]
                self.print_success(f"会话状态: {status.status}")
                self.print_info(f"  消息数量: {status.message_count}")

            # 获取待办事项
            self.print_info("获取待办事项...")
            todos = self.client.sessions.todo(self.session_id)
            if todos:
                self.print_success(f"找到 {len(todos)} 个待办事项")
                for todo in todos[:3]:
                    checkbox = "☑" if todo.completed else "☐"
                    print(f"  {checkbox} {todo.text}")
            else:
                self.print_info("  没有待办事项")

            # 询问是否删除会话
            print("\n是否删除演示会话？(y/n): ", end="")
            try:
                choice = input().strip().lower()
                if choice == 'y':
                    self.client.sessions.delete(self.session_id)
                    self.print_success("会话已删除")
                else:
                    self.print_info("会话已保留")
            except (EOFError, KeyboardInterrupt):
                self.print_info("会话已保留")

        except Exception as e:
            self.print_error(f"会话状态和清理失败: {e}")

    def run_all_demos(self):
        """运行所有演示"""
        print("\n" + "🚀" * 35)
        print("  OpenCode Python SDK - 完整功能演示")
        print("🚀" * 35)

        try:
            # 同步演示
            self.demo_client_initialization()
            self.demo_session_management()
            self.demo_message_handling()
            self.demo_file_operations()
            self.demo_search_functionality()
            self.demo_config_management()

            # 异步演示
            self.print_section("开始异步演示")
            asyncio.run(self.demo_streaming_events())

            # 清理
            self.demo_session_status_and_cleanup()

            self.print_section("演示完成")
            self.print_success("所有演示已完成！")
            print("\n提示:")
            print("  - 查看 examples/ 目录了解更多示例")
            print("  - 阅读 README.md 了解完整文档")
            print("  - 访问 https://opencode.ai 获取更多信息")

        except KeyboardInterrupt:
            self.print_info("\n演示被用户中断")
        except Exception as e:
            self.print_error(f"演示过程中发生错误: {e}")
        finally:
            self.client.close()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="OpenCode Python SDK 功能演示")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="OpenCode 服务器地址 (默认: http://localhost:8000)"
    )
    parser.add_argument(
        "--directory",
        help="项目目录路径"
    )

    args = parser.parse_args()

    demo = OpenCodeDemo(base_url=args.base_url, directory=args.directory)
    demo.run_all_demos()


if __name__ == "__main__":
    main()
