# 定时任务

> ⏰ Cron 与 Hooks 自动化

---

## 第一步：概念解释

**定时任务是什么？**
- 就像「闹钟」和「自动提醒」
- 让 Agent 定时执行任务
- 或在特定事件触发时执行

**两种类型**：
- **Cron** - 定时执行（每天 9 点提醒）
- **Hooks** - 事件触发（收到邮件时处理）

**类比**：
- Cron = 闹钟（固定时间响）
- Hooks = 门铃（有人敲门响）
- Agent = 执行者（响铃后行动）

---

## 第二步：类比理解

| 任务类型 | 类比 | 示例 |
|----------|------|------|
| Cron | 闹钟 | 每天 9 点检查邮件 |
| Hook | 门铃 | 收到邮件通知后处理 |
| Standing Order | 常规任务 | 每次对话都记录 |

**自动化流程**：
```
时间到达 / 事件触发
    ↓
Gateway 检测
    ↓
创建独立 Session
    ↓
Agent 执行任务
    ↓
发送结果到目标通道
```

---

## 第三步：动手实践

### 配置 Cron 任务

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
  },
}
```

### 创建 Cron 任务

```bash
# CLI 创建定时任务
openclaw cron add --schedule "0 9 * * *" --message "检查今天的日程" --target whatsapp:+15555550123
```

**schedule 格式**（cron 表达式）：
```
┌───────────── 分钟 (0-59)
│ ┌─────────── 小时 (0-23)
│ │ ┌───────── 日 (1-31)
│ │ │ ┌─────── 月 (1-12)
│ │ │ │ ┌───── 周几 (0-6)
│ │ │ │ │
* * * * *
```

**示例**：
- `0 9 * * *` - 每天 9:00
- `0 9 * * 1-5` - 周一到周五 9:00
- `*/30 * * * *` - 每 30 分钟
- `0 8 1 * *` - 每月 1 号 8:00

### QQ Bot 定时提醒

使用 `qqbot_remind` 工具：

```bash
# 一次性提醒（5分钟后）
qqbot_remind action=add content="喝水" time="5m" to="qqbot:c2c:user_openid"

# 周期提醒（每天 8 点）
qqbot_remind action=add content="晨会" time="0 8 * * *" to="qqbot:group:group_openid"

# 查看提醒列表
qqbot_remind action=list

# 删除提醒
qqbot_remind action=remove jobId=xxx
```

### 配置 Hooks

```json5
{
  hooks: {
    enabled: true,
    token: "hook-secret",
    path: "/hooks",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "main",
        deliver: true,
      },
    ],
  },
}
```

**Hooks 工作原理**：
1. 外部服务发送 HTTP POST 到 `/hooks/{path}`
2. Gateway 验证 token
3. 根据 mapping 路由到 Agent
4. Agent 处理并发送结果

### Gmail Hook 示例

```json5
{
  hooks: {
    enabled: true,
    token: "xxx",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "email-handler",
        allowUnsafeExternalContent: false,
      },
    ],
  },
}
```

外部发送：
```bash
curl -X POST http://gateway:18789/hooks/gmail \
  -H "Authorization: Bearer xxx" \
  -d '{"subject": "New email", "body": "..."}'
```

---

## 第四步：知识关联

### Cron vs Hook vs Standing Order

| 类型 | 触发 | 适用场景 |
|------|------|----------|
| Cron | 定时 | 每日提醒、定期检查 |
| Hook | 事件 | 邮件通知、Webhook |
| Standing Order | 每次对话 | 自动记录、默认行为 |

### Heartbeat（心跳）

**Heartbeat = 定期检查主 Agent 状态**

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",      // 每 30 分钟
        target: "last",    // 发送到最后使用的通道
      },
    },
  },
}
```

**Heartbeat 用途**：
- 检查邮件
- 检查日程
- 主动提醒
- 后台维护

### Cron 运行记录

```bash
# 查看任务列表
openclaw cron list

# 查看运行历史
openclaw cron logs

# 查看特定任务
openclaw cron logs --jobId xxx
```

---

## Cron 任务配置详解

### 时间表达式

**相对时间**（一次性）：
- `5m` - 5 分钟后
- `1h` - 1 小时后
- `2d` - 2 天后

**Cron 表达式**（周期性）：
- `0 8 * * *` - 每天 8:00
- `0 9 * * 1-5` - 工作日 9:00
- `*/15 * * * *` - 每 15 分钟

### 任务参数

| 参数 | 说明 |
|------|------|
| `schedule` | 执行时间 |
| `message` | 发送给 Agent 的内容 |
| `target` | 结果发送到哪个通道 |
| `agentId` | 使用哪个 Agent |
| `timezone` | 时区（默认 Asia/Shanghai） |

---

## Hooks 安全

**重要安全原则**：

1. **使用独立 token** - 不要用 Gateway token
2. **Header-only auth** - `Authorization: Bearer` 或 `x-openclaw-token`
3. **不信任内容** - Hook 内容视为不可信输入
4. **限制 session key** - 设置 `allowedSessionKeyPrefixes`
5. **专用 path** - 不要用 `/` 作为 hooks path

```json5
{
  hooks: {
    enabled: true,
    token: "dedicated-hook-token",  // 专用 token
    path: "/hooks",                 // 专用路径
    allowRequestSessionKey: false,  // 禁止请求指定 session
    allowedSessionKeyPrefixes: ["hook:"],  // 限制前缀
  },
}
```

---

## 定时任务命令速查

```bash
# Cron 管理
openclaw cron list
openclaw cron add --schedule "0 9 * * *" --message "..."
openclaw cron remove --jobId xxx

# QQ Bot 提醒
qqbot_remind action=list
qqbot_remind action=add content="xxx" time="5m"
qqbot_remind action=remove jobId=xxx

# Hooks 配置
openclaw config set hooks.enabled true
openclaw config set hooks.token "xxx"

# Heartbeat
openclaw config set agents.defaults.heartbeat.every "30m"
```

---

## 下一步

- [06-Gateway网关](./06-gateway.md) - Gateway 配置
- [09-安全最佳实践](./09-security.md) - Hooks 安全
- [官方文档](https://docs.openclaw.ai/automation/cron-jobs) - Cron 详细文档

---

> ✅ 定时任务让 Agent 变得主动，不只是被动响应。