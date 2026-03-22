#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "rich", "python-dateutil", "beautifulsoup4"]
# ///
"""
AI 新闻日报 QQ Bot 推送脚本 v3.0
- 接入 xix.ai 高质量新闻源
- 支持直接输出到 stdout（供 cron 使用）
- 支持 dry-run 预览
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from news_daily import generate_daily_report, render_qq_message, save_report


def main():
    parser = argparse.ArgumentParser(description="AI 新闻日报 QQ Bot 推送 v3.0")
    parser.add_argument("--target", "-t", help="目标 QQ 用户 ID 或群 ID")
    parser.add_argument("--date", "-d", help="指定日期 (YYYY-MM-DD)，默认为今天")
    parser.add_argument("--output", "-o", default="./reports", help="报告保存目录")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际发送")
    parser.add_argument("--stdout", action="store_true", help="输出到 stdout（供 cron 使用）")
    args = parser.parse_args()
    
    print("📰 正在生成 AI 新闻日报 v3.0...\n", file=sys.stderr)
    
    # 生成日报
    report = generate_daily_report()
    
    # 渲染为 QQ 消息
    qq_message = render_qq_message(report)
    
    # 保存报告
    md_path, json_path = save_report(report, args.output)
    
    # 输出模式
    if args.dry_run:
        print("\n" + "="*60, file=sys.stderr)
        print("【预览模式 - 未实际发送】", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(qq_message)
        print("="*60, file=sys.stderr)
        return
    
    if args.stdout:
        # 直接输出到 stdout，供 cron 捕获
        print(qq_message)
        print(f"\n✅ 日报已生成，报告保存: {md_path}", file=sys.stderr)
        return
    
    # 通过 OpenClaw 发送
    print(f"\n📤 正在推送到：{args.target or '默认渠道'}\n", file=sys.stderr)
    
    cmd = ["openclaw", "message", "send", "--message", qq_message]
    if args.target:
        cmd.extend(["--target", args.target])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"\n✅ 推送完成！", file=sys.stderr)
            print(f"📄 报告已保存：{md_path}", file=sys.stderr)
        else:
            print(f"\n❌ 推送失败：{result.stderr}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 推送异常：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()