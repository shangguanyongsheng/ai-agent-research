#!/bin/bash
# AI 新闻日报推送脚本
# 用法：./send_news.sh [QQ 用户 ID]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source .venv/bin/activate

# 目标 QQ ID (可选)
TARGET_QQ="${1:-}"

# 生成并推送
if [ -n "$TARGET_QQ" ]; then
    echo "📰 生成新闻日报并推送到 QQ: $TARGET_QQ"
    uv run python send_to_qq.py --target "$TARGET_QQ"
else
    echo "📰 生成新闻日报 (预览模式)"
    uv run python send_to_qq.py --dry-run
fi
