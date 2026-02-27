"""
只监听事件流的测试

这个脚本只订阅 /event 端点，监听所有事件，不发送任何消息。
适用于：
1. 监控系统事件
2. 调试事件流
3. 观察其他会话的活动
"""

import asyncio
import httpx
import json
from datetime import datetime

async def listen_events_only():
    """只监听事件流"""
    base_url = "http://192.168.77.28:8001"
    
    print("OpenCode 事件监听器")
    print("=" * 60)
    print("开始监听所有事件...")
    print("按 Ctrl+C 停止监听")
    print("=" * 60)
    print()
    
    async with httpx.AsyncClient(base_url=base_url, timeout=None) as client:
        try:
            async with client.stream(
                "GET",
                "/event",
                headers={"Accept": "text/event-stream"}
            ) as response:
                print(f"✅ 已连接到事件流 (状态码: {response.status_code})")
                print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 60)
                print()
                
                event_count = 0
                
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    
                    event_count += 1
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    
                    # 解析事件
                    if line.startswith("event:"):
                        event_type = line[6:].strip()
                        print(f"[{timestamp}] 事件类型: {event_type}")
                    
                    elif line.startswith("data:"):
                        data_str = line[5:].strip()
                        try:
                            data = json.loads(data_str)
                            event_type = data.get("type", "unknown")
                            # print(data)
                            # 根据事件类型显示不同的信息
                            if event_type == "server.connected":
                                print(f"[{timestamp}] 🔌 服务器已连接")
                            
                            # elif event_type == "session.created":
                            #     session_id = data.get("properties", {}).get("info", {}).get("id")
                            #     title = data.get("properties", {}).get("info", {}).get("title")
                            #     print(f"[{timestamp}] 📝 会话已创建: {title} ({session_id})")
                            
                            # elif event_type == "session.updated":
                            #     session_id = data.get("properties", {}).get("info", {}).get("id")
                            #     print(f"[{timestamp}] 🔄 会话已更新: {session_id}")
                            
                            # elif event_type == "session.deleted":
                            #     session_id = data.get("properties", {}).get("info", {}).get("id")
                            #     print(f"[{timestamp}] 🗑️  会话已删除: {session_id}")
                            
                            # elif event_type == "session.status":
                            #     session_id = data.get("properties", {}).get("sessionID")
                            #     status = data.get("properties", {}).get("status", {}).get("type")
                            #     print(f"[{timestamp}] 📊 会话状态: {session_id} -> {status}")
                            
                            # elif event_type == "session.idle":
                            #     session_id = data.get("properties", {}).get("sessionID")
                            #     print(f"[{timestamp}] 💤 会话空闲: {session_id}")
                            
                            # elif event_type == "message.created":
                            #     msg_id = data.get("properties", {}).get("info", {}).get("id")
                            #     role = data.get("properties", {}).get("info", {}).get("role")
                            #     print(f"[{timestamp}] 💬 消息已创建: {role} ({msg_id})")
                            
                            # elif event_type == "message.updated":
                            #     msg_id = data.get("properties", {}).get("info", {}).get("id")
                            #     print(f"[{timestamp}] 🔄 消息已更新: {msg_id}")
                            
                            elif event_type == "message.part.updated":
                                part = data.get("properties", {}).get("part", {})
                                part_type = part.get("type")
                                part_id = part.get("id")
                                
                                if part_type == "text":
                                    text = part.get("text", "")
                                    text_preview = text
                                    print(f"[{timestamp}] 📝 文本内容: {text_preview}")
                                elif part_type == "tool":
                                    tool_name = part.get("tool")
                                    state = part.get("state", {}).get("status")
                                    print(f"[{timestamp}] 🔧 工具调用: {tool_name} ({state})")
                                elif part_type == "reasoning":
                                    reasoning = part.get("text", "")
                                    reasoning_preview = reasoning[:50] + "..." if len(reasoning) > 50 else reasoning
                                    print(f"[{timestamp}] 🤔 推理过程: {reasoning_preview}")
                                else:
                                    print(f"[{timestamp}] 📦 消息部分: {part_type} ({part_id})")
                            
                            # elif event_type == "message.completed":
                            #     msg_id = data.get("properties", {}).get("info", {}).get("id")
                            #     print(f"[{timestamp}] ✅ 消息完成: {msg_id}")
                            
                            # else:
                            #     # 其他事件类型
                            #     print(f"[{timestamp}] 📌 事件: {event_type}")
                            
                            # 显示原始数据（可选，用于调试）
                            # print(f"    数据: {json.dumps(data, ensure_ascii=False)[:100]}...")
                        
                        except json.JSONDecodeError:
                            print(f"[{timestamp}] ⚠️  无法解析 JSON: {data_str[:100]}...")
                    
                    else:
                        # 其他行
                        print(f"[{timestamp}] {line}")
                    
                    print()  # 空行分隔
                    
                    # 每100个事件显示一次统计
                    if event_count % 100 == 0:
                        print(f"📊 已接收 {event_count} 个事件")
                        print()
        
        except KeyboardInterrupt:
            print()
            print("-" * 60)
            print(f"⏹️  监听已停止")
            print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📊 总共接收 {event_count} 个事件")
            print("=" * 60)
        
        except Exception as e:
            print()
            print("-" * 60)
            print(f"❌ 错误: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

async def main():
    try:
        await listen_events_only()
    except KeyboardInterrupt:
        print("\n👋 再见！")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 再见！")
