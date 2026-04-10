# 配置详解

> ⚙️ openclaw.json 配置文件全面解析

---

## 第一步：概念解释

**配置文件是什么？**
- 就像「收音机的调频旋钮」
- 告诉 OpenClaw：
  - 用哪个 AI 模型
  - 谁可以和你对话
  - 连接哪些聊天软件
  - 工作目录在哪

**位置**：`~/.openclaw/openclaw.json`

**格式**：JSON5（支持注释和尾逗号）

---

## 第二步：类比理解

| 配置项 | 类比 |
|--------|------|
| `agents.defaults.model` | 选择电台频道 |
| `channels.whatsapp.allowFrom` | 谁能打电话进来 |
| `agents.defaults.workspace` | 工作台位置 |
| `gateway.port` | 收音机天线端口 |

**配置逻辑**：
```
默认配置（安全）
    ↓
你添加配置（定制）
    ↓
Gateway 应用配置（生效）
```

---

## 第三步：动手实践

### 最简配置

```json5
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

### 配置模型

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-6",
        fallbacks: ["openai/gpt-5.4"],
      },
      models: {
        "anthropic/claude-sonnet-4-6": { alias: "Sonnet" },
        "openai/gpt-5.4": { alias: "GPT" },
      },
    },
  },
}
```

**模型格式**：`provider/model-name`

**常见提供商**：
- `anthropic/` - Claude
- `openai/` - GPT
- `google/` - Gemini
- `deepseek/` - DeepSeek

### 配置通道

**Telegram**：
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc...",  // 从 @BotFather 获取
      dmPolicy: "pairing",     // pairing | allowlist | open | disabled
      allowFrom: ["tg:12345"],
    },
  },
}
```

**WhatsApp**：
```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      allowFrom: ["+15555550123"],  // 允许的手机号
      groups: {
        "*": { requireMention: true },  // 群聊需要 @提及
      },
    },
  },
}
```

**Discord**：
```json5
{
  channels: {
    discord: {
      enabled: true,
      botToken: "xxx...",
      clientId: "123...",
      clientSecret: "xxx...",
      guildId: "xxx...",  // 服务器 ID
    },
  },
}
```

### 配置访问控制

**dmPolicy（私聊策略）**：

| 值 | 说明 |
|----|------|
| `pairing` | 需配对码验证（默认） |
| `allowlist` | 只允许 allowFrom 列表 |
| `open` | 允许所有人（需 `allowFrom: ["*"]`） |
| `disabled` | 禁用私聊 |

**群聊配置**：
```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },  // 所有群需 @提及
        "family-group": { requireMention: false },  // 特定群不需
      },
    },
  },
}
```

### 配置 Skills

```json5
{
  agents: {
    defaults: {
      skills: ["github", "weather", "coding-agent"],
    },
  },
}
```

### 配置会话

```json5
{
  session: {
    dmScope: "per-channel-peer",  // 会话隔离方式
    reset: {
      mode: "daily",              // 每日重置
      atHour: 4,                  // 4点重置
    },
  },
}
```

**dmScope 选项**：
- `main` - 共享主会话
- `per-peer` - 每人独立会话
- `per-channel-peer` - 每通道每人独立（推荐）

### 配置沙箱

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",  // off | non-main | all
        scope: "agent",    // session | agent | shared
      },
    },
  },
}
```

---

## 配置编辑方式

### 方式一：交互式配置

```bash
openclaw configure
```

### 方式二：CLI 命令

```bash
# 获取配置值
openclaw config get agents.defaults.workspace

# 设置配置值
openclaw config set agents.defaults.heartbeat.every "2h"

# 删除配置值
openclaw config unset plugins.entries.brave.config.webSearch.apiKey
```

### 方式三：控制面板

打开 http://127.0.0.1:18789 → Config 标签页

### 方式四：直接编辑

用文本编辑器编辑 `~/.openclaw/openclaw.json`

**Gateway 会自动监测并应用更改（热重载）**

---

## 第四步：知识关联

### 热重载机制

Gateway 监听配置文件变化：

| 变更类型 | 行为 |
|----------|------|
| 通道配置 | 热应用，无需重启 |
| 模型配置 | 立即生效 |
| Gateway 配置 | 需重启 |

**配置模式**：
```json5
{
  gateway: {
    reload: {
      mode: "hybrid",  // hybrid | hot | restart | off
    },
  },
}
```

### 环境变量

在配置中引用环境变量：

```json5
{
  models: {
    providers: {
      openai: { apiKey: "${OPENAI_API_KEY}" },
    },
  },
}
```

### 分文件配置

使用 `$include` 分拆配置：

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  channels: { $include: "./channels.json5" },
}
```

---

## 配置验证

```bash
# 检查配置是否有效
openclaw doctor

# 查看完整配置 schema
openclaw config schema
```

**验证失败**：
- Gateway 不启动
- 只有诊断命令可用
- `openclaw doctor` 显示具体问题

---

## 常见配置示例

### 个人助理配置

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "anthropic/claude-sonnet-4-6" },
      skills: ["github", "weather", "coding-agent"],
      heartbeat: { every: "30m" },
    },
  },
  channels: {
    telegram: {
      enabled: true,
      botToken: "xxx",
      dmPolicy: "pairing",
    },
    whatsapp: {
      enabled: true,
      allowFrom: ["+15555550123"],
    },
  },
}
```

### 多 Agent 配置

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp" } },
    { agentId: "work", match: { channel: "slack" } },
  ],
}
```

---

## 下一步

- [05-通道集成](./05-channels.md) - 各通道具体配置
- [09-安全最佳实践](./09-security.md) - 安全配置建议
- [07-子Agent系统](./07-subagents.md) - 多 Agent 配置

---

> ✅ 配置完成！记住：默认配置已经安全可用，你只需添加需要的定制项。