# 📰 AI 新闻日报生成器

自动化的 AI 新闻日报生成工具，集成 SearXNG 搜索，支持 QQ Bot 推送。

## 功能特点

- 🔍 **隐私搜索**: 使用本地 SearXNG 实例，无需外部 API
- 📱 **多平台推送**: 支持 QQ Bot、Markdown 报告、JSON 数据
- 🗂️ **分类聚合**: AI 科技、互联网、国际新闻、财经、科学
- ⏰ **定时任务**: 支持 cron 定时生成
- 📊 **多种格式**: Markdown、JSON、纯文本 (QQ)

## 快速开始

### 环境要求

- Python 3.11+ (uv 会自动管理)
- SearXNG 服务运行中
- (可选) QQ Bot 已配置

### 安装依赖

```bash
cd ~/.openclaw/workspace/apps/news-daily
uv venv  # 创建虚拟环境
source .venv/bin/activate
uv pip install -r requirements.txt  # 或使用：uv pip install httpx rich python-dateutil
```

### 配置

```bash
# 复制配置示例
cp .env.example .env

# 编辑配置 (如果需要自定义)
vim .env
```

### 基本使用

```bash
# 生成今日日报 (默认保存 Markdown + JSON)
uv run python news_daily.py

# 生成指定日期的日报
uv run python news_daily.py --date 2026-03-11

# 输出 QQ 格式到 stdout (用于推送)
uv run python news_daily.py --format qq

# 输出 JSON 格式 (用于程序处理)
uv run python news_daily.py --format json

# 安静模式 (仅输出结果)
uv run python news_daily.py --quiet
```

### 输出示例

#### QQ 格式
```
📰 AI 新闻日报
日期：2026-03-11
生成时间：2026-03-11 20:00:00

🤖 AI 与科技 (5 条)
──────────────────────────────
1. 标题...
   来源：TechCrunch | 时间：03-11 15:30
   内容摘要...
   https://example.com/...

...
```

#### Markdown 格式
生成美观的 Markdown 报告，包含分类、链接、时间戳。

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SEARXNG_URL` | SearXNG 实例地址 | `http://localhost:8080` |

### 自定义新闻分类

编辑 `news_daily.py` 中的 `NEWS_CATEGORIES` 列表：

```python
NEWS_CATEGORIES = [
    {"name": "🤖 AI 与科技", "query": "artificial intelligence AI technology news"},
    {"name": "📱 互联网", "query": "internet tech startup news"},
    # 添加更多分类...
]
```

## 定时任务

### 使用 cron (推荐)

每天上午 8 点生成并推送：

```bash
# 编辑 crontab
crontab -e

# 添加任务 (每天 8:00)
0 8 * * * cd ~/.openclaw/workspace/apps/news-daily && uv run python news_daily.py --format qq | qqbot-send --to-user YOUR_QQ_ID
```

### 使用 OpenClaw cron

参考 `cron/send_daily_news.py` 脚本。

## QQ Bot 推送

### 方式一：管道推送

```bash
uv run python news_daily.py --format qq | openclaw message send --target qqbot --message -
```

### 方式二：脚本推送

使用 `send_to_qq.py` 脚本：

```bash
uv run python send_to_qq.py --user YOUR_QQ_ID
```

## 输出目录

报告默认保存到 `./reports/`：

```
reports/
├── news_daily_20260311.md    # Markdown 报告
└── news_daily_20260311.json  # JSON 数据
```

## API 使用

```python
from news_daily import generate_daily_news, render_qq_message

# 生成日报
news = generate_daily_news("2026-03-11")

# 渲染为 QQ 消息
msg = render_qq_message(news)

# 保存报告
from news_daily import save_report
save_report(news, "./my-reports")
```

## 故障排除

### SearXNG 连接失败

1. 检查 SearXNG 服务是否运行：`curl http://localhost:8080`
2. 确认 `SEARXNG_URL` 环境变量正确

### 搜索结果少

- 尝试调整 `time_range` 参数 (day/week/month)
- 修改搜索关键词更精确

## 开发计划

- [ ] 支持更多新闻源
- [ ] AI 摘要生成
- [ ] 图片新闻支持
- [ ] 个性化推荐
- [ ] 历史新闻对比

## 许可证

MIT License

---

*由 OpenClaw 生态系统支持*
