# 通道集成

> 📱 连接 Discord、WhatsApp、Telegram 等聊天平台

---

## 第一步：概念解释

**Channel 是什么？**
- 就像「电话线路」
- 连接不同的聊天平台
- 让 Agent 在各平台收发消息

**类比**：
- Gateway = 电话总机
- Channel = 电话线路（联通/电信/移动）
- 你在各平台发消息 = 从不同线路打电话
- Agent 收到并回复 = 总机接听并回复

**支持的通道**：
- Discord、WhatsApp、Telegram、Slack
- Signal、iMessage、Matrix
- Microsoft Teams、Google Chat
- Feishu、QQ Bot、Zalo
- 更多...

---

## 第二步：类比理解

| 通道 | 类比 | 特点 |
|------|------|------|
| Telegram | 快速线路 | 最易配置，只需 Bot Token |
| WhatsApp | 家庭线路 | 需手机号验证 |
| Discord | 社区线路 | 支持 Guild/Thread |
| Slack | 办公线路 | 企业级集成 |
| iMessage | 苹果专线 | 需 Mac/Apple ID |

**通道配置共性**：
```
1. 获取通道凭证（Token/账号）
2. 配置到 openclaw.json
3. 设置访问策略（谁能用）
4. 启动/验证连接
```

---

## 第三步：动手实践

### Telegram（最快配置）

**1. 创建 Bot**：
- 打开 Telegram，搜索 @BotFather
- 发送 `/newbot`
- 获取 Bot Token（如 `123456:ABC-DEF...`）

**2. 配置**：
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123456:ABC-DEF...",
      dmPolicy: "pairing",  // 需配对验证
    },
  },
}
```

**3. 测试**：
- 在 Telegram 打开你的 Bot
- 发送消息
- Agent 应回复

### WhatsApp

**方式一：Web API（需商业账号）**
```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      phoneNumberId: "xxx",
      businessAccountId: "xxx",
      accessToken: "xxx",
      allowFrom: ["+15555550123"],
    },
  },
}
```

**方式二：用户模式（个人号）**
```json5
{
  channels: {
    zalouser: {
      enabled: true,
      allowFrom: ["+15555550123"],
    },
  },
}
```

### Discord

**1. 创建 Bot**：
- Discord Developer Portal → Applications → New Application
- Bot → Add Bot → 复制 Token
- OAuth2 → 生成邀请链接

**2. 配置**：
```json5
{
  channels: {
    discord: {
      enabled: true,
      botToken: "xxx",
      clientId: "xxx",
      clientSecret: "xxx",
      guildId: "your-server-id",
    },
  },
}
```

**3. Thread 支持**：
Discord 支持 `/focus` 命令绑定 Thread 到独立会话。

### Slack

**1. 创建 App**：
- Slack API → Create New App
- 添加 Bot Token Scopes
- 安装到 Workspace

**2. 配置**：
```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-xxx",
      appToken: "xapp-xxx",
      signingSecret: "xxx",
    },
  },
}
```

### Signal

```json5
{
  channels: {
    signal: {
      enabled: true,
      number: "+15555550123",
      allowFrom: ["+15555550999"],
    },
  },
}
```

### iMessage (Mac)

```json5
{
  channels: {
    imessage: {
      enabled: true,
      allowFrom: ["+15555550123"],
    },
  },
}
```

### Matrix

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserverUrl: "https://matrix.org",
      userId: "@bot:matrix.org",
      accessToken: "xxx",
    },
  },
}
```

### Microsoft Teams

```json5
{
  channels: {
    msteams: {
      enabled: true,
      tenantId: "xxx",
      clientId: "xxx",
      clientSecret: "xxx",
    },
  },
}
```

---

## 第四步：知识关联

### 访问策略（dmPolicy）

| 值 | 说明 | 安全性 |
|----|------|--------|
| `pairing` | 需配对码验证（默认） | ⭐⭐⭐ |
| `allowlist` | 只允许白名单 | ⭐⭐⭐⭐ |
| `open` | 允许所有人 | ⭐ |
| `disabled` | 禁用私聊 | ⭐⭐⭐⭐⭐ |

### 群聊配置

**requireMention**（需要 @提及）：
```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },  // 所有群需 @
      },
    },
  },
}
```

**mentionPatterns**（自定义触发词）：
```json5
{
  agents: {
    list: [{
      id: "main",
      groupChat: {
        mentionPatterns: ["@openclaw", "bot", "assistant"],
      },
    }],
  },
}
```

### 多账号配置

**同一通道多账号**：
```json5
{
  channels: {
    telegram: {
      accounts: {
        personal: { botToken: "xxx" },
        work: { botToken: "yyy" },
      },
    },
  },
  bindings: [
    { agentId: "home", match: { channel: "telegram", accountId: "personal" } },
    { agentId: "work", match: { channel: "telegram", accountId: "work" } },
  ],
}
```

---

## 通道健康监控

```json5
{
  gateway: {
    channelHealthCheckMinutes: 5,
    channelStaleEventThresholdMinutes: 30,
    channelMaxRestartsPerHour: 10,
  },
}
```

**监控逻辑**：
1. 每 N 分钟检查通道状态
2. 如果 N 分钟无事件，判定为 stale
3. 自动重启通道
4. 每小时最多重启 M 次

---

## 通道故障排查

```bash
# 查看通道状态
openclaw channels status

# 查看日志
openclaw logs --filter channel

# 健康检查
openclaw doctor
```

**常见问题**：

| 问题 | 解决 |
|------|------|
| Token 无效 | 重新获取并配置 |
| 连接超时 | 检查网络防火墙 |
| 权限不足 | 检查 Bot 权限设置 |
| 消息不回复 | 检查 allowFrom 配置 |

---

## 下一步

- [02-配置详解](./02-configuration.md) - 配置文件详解
- [09-安全最佳实践](./09-security.md) - 安全配置建议
- [通道文档](https://docs.openclaw.ai/channels) - 官方通道文档

---

> ✅ 通道配置核心：获取凭证 → 配置 openclaw.json → 设置访问策略。Telegram 最简单，建议新手先用 Telegram。