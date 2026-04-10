# 🚀 AI 新闻日报 - 快速启动指南

## 1 分钟快速测试

```bash
# 进入项目目录
cd ~/.openclaw/workspace/apps/news-daily

# 激活虚拟环境并运行
source .venv/bin/activate
export SEARXNG_URL="http://localhost:8080"
uv run python news_daily.py --format qq
```

## 5 分钟完整配置

### Step 1: 确认环境

```bash
# 检查 SearXNG 是否运行
curl http://localhost:8080

# 检查 Python 和 uv
python3 --version
uv --version
```

### Step 2: 配置

```bash
# 复制配置模板
cp .env.example .env

# (可选) 编辑配置
vim .env
```

### Step 3: 测试运行

```bash
# 运行测试
uv run python test_news_daily.py

# 生成日报
uv run python news_daily.py

# 查看生成的报告
cat reports/news_daily_*.md
```

### Step 4: 配置推送 (可选)

```bash
# 预览推送内容
uv run python send_to_qq.py --dry-run

# 实际推送 (需要 QQ Bot 配置)
uv run python send_to_qq.py --target YOUR_QQ_ID
```

### Step 5: 设置定时任务 (可选)

#### 方式 A: 系统 cron

```bash
crontab -e

# 添加以下行 (每天 8:00 执行)
0 8 * * * cd ~/.openclaw/workspace/apps/news-daily && source .venv/bin/activate && uv run python cron_job.py
```

#### 方式 B: OpenClaw cron

参考 `openclaw-cron.json` 配置。

## 常用命令

```bash
# 生成今日日报
uv run python news_daily.py

# 生成指定日期日报
uv run python news_daily.py --date 2026-03-11

# 仅查看 QQ 格式输出
uv run python news_daily.py --format qq

# 推送到 QQ
uv run python send_to_qq.py --target 123456789

# 查看帮助
uv run python news_daily.py --help
```

## 故障排除

### SearXNG 连接失败

```bash
# 检查服务状态
systemctl status searxng  # 或你的启动方式

# 测试连接
curl http://localhost:8080/search?q=test&format=json
```

### 没有新闻结果

- 检查 SearXNG 搜索引擎配置
- 尝试放宽时间范围：`--time-range week`
- 修改搜索关键词

### QQ 推送失败

- 确认 QQ Bot 已正确配置
- 检查 `openclaw channels list`
- 使用 `--dry-run` 预览内容

## 下一步

- 阅读完整文档：`README.md`
- 查看项目总结：`PROJECT_SUMMARY.md`
- 自定义新闻分类：编辑 `news_daily.py` 中的 `NEWS_CATEGORIES`

---

**有问题？** 查看 `README.md` 或运行 `uv run python news_daily.py --help`
