# 订阅全局事件
import asyncio
import sys
from datetime import datetime
from opencode_sdk import OpencodeClient


async def main():
    # 创建客户端实例
    client = OpencodeClient(base_url="http://192.168.77.28:8001", directory="/data/seo/workspace")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始订阅全局事件...")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 连接到: http://192.168.77.28:8001/global/event")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 等待事件中... (按 Ctrl+C 退出)")
    print("-" * 60)

    event_count = 0
    
    try:
        # 订阅全局事件
        async for event in client.events.subscribe_global():
            event_count += 1
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            print(f"\n[{timestamp}] 事件 #{event_count}: {event.type}")
            
            # 打印事件的所有属性（用于调试）
            if hasattr(event, '__dict__'):
                for key, value in event.__dict__.items():
                    if key != 'type' and value is not None:
                        print(f"  {key}: {value}")

            # 处理不同类型的事件
            if event.type == "server.connected":
                print(f"  ✓ 服务器已连接")
            elif event.type == "session.created":
                if hasattr(event, 'properties') and hasattr(event.properties, 'info'):
                    info = event.properties.info
                    session_id = info.get('id', 'N/A') if isinstance(info, dict) else getattr(info, 'id', 'N/A')
                    title = info.get('title', 'N/A') if isinstance(info, dict) else getattr(info, 'title', 'N/A')
                    print(f"  → 新会话创建: {title} (ID: {session_id})")
                else:
                    print(f"  → 新会话创建")
            elif event.type == "session.updated":
                print(f"  → 会话更新")
            elif event.type == "session.deleted":
                print(f"  → 会话删除")
            elif event.type == "session.idle":
                print(f"  → 会话空闲")
            elif event.type == "message.part.delta":
                if hasattr(event, 'properties'):
                    props = event.properties
                    delta = getattr(props, 'delta', '')
                    field = getattr(props, 'field', 'unknown')
                    print(f"  → 消息增量 [{field}]: {delta}")
                else:
                    print(f"  → 消息增量")
            elif event.type.startswith("message."):
                print(f"  → 消息事件")
            elif event.type.startswith("file."):
                print(f"  → 文件事件")
            
            sys.stdout.flush()

    except KeyboardInterrupt:
        print(f"\n\n[{datetime.now().strftime('%H:%M:%S')}] 用户中断，共接收 {event_count} 个事件")
    except ConnectionError as e:
        print(f"\n连接失败: {e}")
        print("请检查:")
        print("  1. 服务器是否运行在 http://192.168.77.28:8001")
        print("  2. 网络连接是否正常")
    except TimeoutError as e:
        print(f"\n连接超时: {e}")
    except Exception as e:
        print(f"\n发生错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
