#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
定时任务脚本 - 用于 OpenClaw cron 或系统 cron
每天上午 8 点自动生成并推送新闻日报
"""

import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from news_daily import generate_daily_news, render_qq_message, save_report
from send_to_qq import send_via_openclaw


def main():
    """定时任务入口"""
    # 配置
    target_qq = os.getenv("NEWS_TARGET_QQ", "")  # 可选：指定 QQ 用户/群 ID
    output_dir = os.getenv("NEWS_OUTPUT_DIR", "./reports")
    
    print("📰 AI 新闻日报 - 定时任务启动")
    print("=" * 50)
    
    try:
        # 生成日报
        daily_news = generate_daily_news()
        
        # 渲染消息
        qq_message = render_qq_message(daily_news)
        
        # 保存报告
        md_path, json_path = save_report(daily_news, output_dir)
        
        # 推送消息
        if target_qq:
            print(f"\n📤 推送到 QQ: {target_qq}")
            send_via_openclaw(qq_message, target_qq)
        else:
            print("\n⚠️ 未配置 NEWS_TARGET_QQ，跳过推送")
            print("消息内容预览:")
            print(qq_message[:500] + "..." if len(qq_message) > 500 else qq_message)
        
        print("\n✅ 定时任务完成")
        return 0
        
    except Exception as e:
        print(f"\n❌ 定时任务失败：{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
