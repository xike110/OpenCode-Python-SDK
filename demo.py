"""
OpenCode SDK 异步演示脚本

这个脚本演示了如何使用 OpenCode Python SDK 的异步功能。
"""

import json
import httpx
from opencode_sdk import OpencodeClient


class AsyncOpencodeClient:
    """
    异步版本的 OpenCode 客户端包装器
    """
    def __init__(self, base_url: str = "http://192.168.77.28:8001", directory: str = "/path/to/your/project"):
        self.sync_client = OpencodeClient(base_url=base_url, directory=directory)
        self.http_client = self.sync_client._http_client.client  # 使用底层的httpx客户端

    async def _make_request(self, method: str, path: str, **kwargs):
        """异步发起请求并返回原始JSON响应"""
        url = self.sync_client._http_client._build_url(path)
        
        # 执行异步请求
        async with httpx.AsyncClient(base_url=self.sync_client._http_client.base_url) as client:
            response = await client.request(method, path, **kwargs)
            
            # 打印原始JSON响应
            print(f"原始响应 ({method} {path}): {response.status_code}")
            try:
                raw_json = response.json()
                print(f"JSON响应: {json.dumps(raw_json, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"非JSON响应: {response.text}")
            
            # 处理响应
            return self.sync_client._http_client._handle_response(response)

    async def health_check(self):
        """异步健康检查"""
        response = await self._make_request("GET", "/global/health")
        return response

    async def sessions_create(self, title: str):
        """异步创建会话"""
        response = await self._make_request("POST", "/session", json={"title": title})
        from opencode_sdk.models.session import Session
        return Session(**response)

    async def sessions_list(self):
        """异步列出所有会话"""
        response = await self._make_request("GET", "/session")
        from opencode_sdk.models.session import Session
        return [Session(**item) for item in response]

    async def sessions_get(self, session_id: str):
        """异步获取会话详情"""
        response = await self._make_request("GET", f"/session/{session_id}")
        from opencode_sdk.models.session import Session
        return Session(**response)

    async def sessions_update(self, session_id: str, **kwargs):
        """异步更新会话"""
        response = await self._make_request("PATCH", f"/session/{session_id}", json=kwargs)
        from opencode_sdk.models.session import Session
        return Session(**response)

    async def sessions_delete(self, session_id: str):
        """异步删除会话"""
        await self._make_request("DELETE", f"/session/{session_id}")


async def main():
    # 创建异步客户端
    print("📝 初始化异步客户端...")
    client = AsyncOpencodeClient(
        base_url="http://192.168.77.28:8001",
        directory="/path/to/your/project"
    )
    print("✅ 客户端已初始化\n")

    try:
        # 0. 健康检查
        print("测试 0: 健康检查")
        health = await client.health_check()
        print(f"✅ 服务器健康状态: {health}\n")

        # 1. 创建会话
        print("测试 1: 创建会话")
        session = await client.sessions_create(title="SDK 异步测试会话")
        print(f"✅ 会话已创建 - ID: {session.id}, 标题: {session.title}\n")

        # 2. 列出所有会话
        print("测试 2: 列出所有会话")
        sessions = await client.sessions_list()
        print(f"✅ 共有 {len(sessions)} 个会话")
        for i, s in enumerate(sessions[:5], 1):
            print(f"   {i}. {s.title} (ID: {s.id})")
        if len(sessions) > 5:
            print(f"   ... 还有 {len(sessions) - 5} 个会话\n")

        # 3. 获取会话详情
        print("测试 3: 获取会话详情")
        session_detail = await client.sessions_get(session.id)
        print(f"✅ 会话详情 - ID: {session_detail.id}, 标题: {session_detail.title}\n")

        # 4. 更新会话
        print("测试 4: 更新会话标题")
        updated_session = await client.sessions_update(
            session_id=session.id,
            title="更新后的 SDK 异步测试会话"
        )
        print(f"✅ 会话已更新 - 新标题: {updated_session.title}\n")

        # 5. 删除会话
        print("测试 5: 删除会话")
        await client.sessions_delete(session.id)
        print(f"✅ 会话已删除\n")

        print("🎉 所有测试完成！")

    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())