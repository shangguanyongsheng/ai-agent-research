# 07-Cron调度

> 用自然语言定义定时任务，让 Hermes 自动执行日常任务、监控、报告。

---

## 第一步：概念解释

### Hermes 的 Cron 系统

Hermes 的 Cron 是 **Agent 级任务**，不是 Shell 脚本任务：

- 自然语言定义任务
- Agent 在独立会话中执行
- 自动交付结果到指定平台
- 可附加 Skills 提供上下文

---

### Cron 能做什么？

| 类型 | 示例 |
|------|------|
| 定时提醒 | "每天 9AM 提醒我开会" |
| 自动报告 | "每小时检查服务器状态并报告" |
| 监控任务 | "每 5 分钟检查服务是否在线" |
| 数据处理 | "每天凌晨整理日志文件" |
| 信息聚合 | "每早晨汇总 Hacker News AI 新闻" |

---

## 第二步：类比理解

### Cron = 自动化助手

传统 Cron → Shell 脚本，硬编码命令
Hermes Cron → Agent 任务，自然语言定义

**类比：**

```
传统 Cron：
# 每天早上运行脚本
0 9 * * * /home/user/check-server.sh

Hermes Cron：
# 每天早上让 Agent 检查服务器
"每天 9AM 检查服务器状态并发送 Telegram 报告"
```

**优势：**
- 自然语言定义，无需写脚本
- Agent 有完整工具能力（终端/Web/文件）
- 可以附加 Skills 提供专业知识
- 自动交付结果到平台

---

### Skill-backed Cron = 专业助手

```
普通 Cron：
Agent 按任务描述执行，可能需要多次尝试

Skill-backed Cron：
Agent 加载 blogwatcher 技能
→ 有专门的 RSS 监控流程
→ 按技能指导高效完成
```

---

## 第三步：代码/实践

### 创建定时任务

#### 在对话中

```bash
/cron add 30m "Remind me to check the build"
/cron add "every 2h" "Check server status"
/cron add "every 1h" "Summarize new feed items" --skill blogwatcher
/cron add "every 1h" "Use both skills" --skill blogwatcher --skill find-nearby
```

#### 自然对话

```bash
❯ Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram.
```

#### CLI 命令

```bash
hermes cron create "every 2h" "Check server status"
hermes cron create "every 1h" "Summarize feed items" --skill blogwatcher
hermes cron create "every 1h" "Combo task" \
  --skill blogwatcher \
  --skill find-nearby \
  --name "Skill combo"
```

---

### Schedule 格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 相对延迟 | `30m`, `2h`, `1d` | 一次性，N 分钟/小时/天后 |
| Interval | `every 30m`, `every 2h` | 循环执行 |
| Cron 表达式 | `0 9 * * *` | 每天 9AM |
| Cron 表达式 | `0 9 * * 1-5` | 工作日 9AM |
| Cron 表达式 | `0 */6 * * *` | 每 6 小时 |
| ISO 时间戳 | `2026-03-15T09:00:00` | 特定时间一次性 |

---

### Skill-backed Cron

```python
# 单技能
cronjob(
    action="create",
    skill="blogwatcher",
    prompt="Check feeds and summarize new items.",
    schedule="0 9 * * *",
    name="Morning feeds",
)

# 多技能（按顺序加载）
cronjob(
    action="create",
    skills=["blogwatcher", "find-nearby"],
    prompt="Combine local events and nearby places into brief.",
    schedule="every 6h",
    name="Local brief",
)
```

---

### 编辑任务

```bash
# 对话中
/cron edit <job_id> --schedule "every 4h"
/cron edit <job_id> --prompt "New task description"
/cron edit <job_id> --skill newskill
/cron edit <job_id> --remove-skill oldskill
/cron edit <job_id> --clear-skills

# CLI
hermes cron edit <job_id> --schedule "every 4h"
hermes cron edit <job_id> --add-skill newskill
```

---

### 任务生命周期

```bash
/cron list                  # 列出所有任务
/cron pause <job_id>        # 暂停（保留但不执行）
/cron resume <job_id>       # 恢复
/cron run <job_id>          # 手动触发（下次 tick 执行）
/cron remove <job_id>       # 删除

# CLI
hermes cron list
hermes cron pause <job_id>
hermes cron resume <job_id>
hermes cron run <job_id>
hermes cron remove <job_id>
hermes cron status
hermes cron tick            # 手动触发调度器 tick
```

---

### 交付选项

| 选项 | 说明 |
|------|------|
| `"origin"` | 回到创建任务的对话（默认） |
| `"local"` | 保存本地文件（CLI 默认） |
| `"telegram"` | Telegram Home Channel |
| `"telegram:123456"` | 特定 Telegram Chat |
| `"discord"` | Discord Home Channel |
| `"discord:#engineering"` | 特定 Discord 频道 |
| `"slack"` / `"whatsapp"` / `"signal"` | 其他平台 |

---

### 防止重复发送

Agent 的最终响应自动交付，不需要在 prompt 中调用 `send_message`。

如果 prompt 调用 `send_message` 到同一目标，Hermes 会跳过并告诉模型把内容放在最终响应。

---

### 响应包装

默认交付会添加 Header/Footer：

```
Cronjob Response: Morning feeds
-------------
<agent output here>
```

关闭包装：

```yaml
# ~/.hermes/config.yaml
cron:
  wrap_response: false
```

---

### Silent 模式

如果 Agent 响应以 `[SILENT]` 开头，不会发送消息：

```python
# 监控任务只在有问题时报告
Check if nginx is running. If healthy, respond with only [SILENT].
Otherwise, report the issue.
```

失败任务总是交付（不管 [SILENT]）。

---

### 运行机制

```
Gateway 每 60 秒 tick
    → 从 jobs.json 加载到期任务
    → 创建新 AIAgent（无历史）
    → 注入附加 Skills
    → 运行 prompt
    → 交付响应
    → 更新状态和下次运行时间
```

**重要：**
- Cron 任务运行在完全新的 Agent 会话
- Prompt 必须包含所有必要信息
- 不能递归创建更多 Cron（防止循环）

---

### Provider 容错

Cron 继承你的 fallback Provider 和凭证池轮换：

- 主 API Key 被限流 → 自动切换备用 Provider
- 单个 Key 失败 → 轮换到池中下一个 Key

---

### 重复次数

| Schedule 类型 | 默认重复 | 说明 |
|---------------|----------|------|
| One-shot | 1 | 一次性 |
| Interval | forever | 无限循环 |
| Cron 表达式 | forever | 无限循环 |

覆盖：

```python
cronjob(
    action="create",
    schedule="every 2h",
    repeat=5,  # 只运行 5 次
)
```

---

### 存储

```
~/.hermes/cron/
├── jobs.json          # 任务定义
├── output/
│   └── {job_id}/
│       └── {timestamp}.md  # 运行输出
└── .tick.lock         # 防止重叠 tick
```

---

## 第四步：知识关联

### Cron 与其他系统的关系

```
┌─────────────────┐
│   Gateway       │  ← 运行 Cron Scheduler
│   (每 60秒 tick)│
└─────────────────┘
        ↓
┌─────────────────┐
│   Cron Jobs     │  ← 任务定义
│   (jobs.json)   │
└─────────────────┘
        ↓
┌─────────────────┐
│   Skills        │  ← 可附加到任务
│   (提供上下文)  │
└─────────────────┘
        ↓
┌─────────────────┐
│   AIAgent       │  ← 独立会话执行
│   (无历史)      │
└─────────────────┘
        ↓
┌─────────────────┐
│   Delivery      │  ← 交付到平台
│   (Telegram/Discord/...)
└─────────────────┘
```

### 相关概念

| 概念 | 关系 |
|------|------|
| [Skills](04-Skills系统.md) | Skill-backed Cron |
| [多平台网关](06-多平台网关.md) | Gateway 运行 Cron |
| [架构详解](03-架构详解.md) | cron/ 目录 |

---

## 🎯 关键理解

1. **自然语言定义**：无需写脚本，用对话定义任务
2. **Agent 级任务**：Agent 有完整工具能力
3. **Skill-backed**：附加 Skills 提供专业流程
4. **自动交付**：结果自动发送到平台
5. **独立会话**：无历史，Prompt 必须自包含

---

## 📋 最佳实践

### Prompt 必须自包含

```markdown
❌ 坏："检查服务器问题"（太模糊）

✅ 好："SSH 到 192.168.1.100 作为 'deploy'，
执行 'systemctl status nginx'，
验证 https://example.com 返回 HTTP 200。"
```

### 监控任务用 [SILENT]

```markdown
❌ 坏：每小时都发送消息（即使正常）

✅ 好：检查服务状态。正常时返回 [SILENT]。
异常时报告问题。
```

### 使用 Skills

```markdown
❌ 坏：每个任务都写完整流程

✅ 好：附加 blogwatcher 技能
任务只需写："检查 RSS 汇报新内容"
```

---

*费曼学习法文档 - Hermes Agent*