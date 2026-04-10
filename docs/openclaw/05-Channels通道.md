# OpenClaw Channels 通道

> 使用费曼学习法：理解如何连接各种聊天平台。

## 📖 概念解释

**什么是 Channel？**

Channel 是 OpenClaw 与聊天平台之间的连接器。每个 Channel 负责：
1. 接收来自聊天平台的消息
2. 转发给 Gateway 处理
3. 将 AI 回复发送回平台

支持的 Channel 包括：Telegram、WhatsApp、Discord、Slack、Signal、iMessage 等。

## 🎯 类比理解

**把 Channel 想象成"电话线接口"**

- 不同电话系统（聊天平台）需要不同接口
- Channel 是适配各种电话线的"转换器"
- Gateway 是中央交换机，处理所有接口的信号

就像酒店前台有多个电话线（市话、国际、内线），Gateway 通过不同 Channel 连接多种聊天平台。

## 🔧 实践示例

### 支持的通道列表

| 通道 | 设置难度 | 特点 |
|------|----------|------|
| **Telegram** | ⭐ 最简单 | 只需 Bot Token |
| **WhatsApp** | ⭐⭐ 中等 | 需要 QR 配对 |
| **Discord** | ⭐⭐ 中等 | Bot + 服务器配置 |
| **Signal** | ⭐⭐⭐ 较难 | signal-cli |
| **iMessage** | ⭐⭐⭐ 较难 | macOS + BlueBubbles |
| **Slack** | ⭐⭐ 中等 | Bolt SDK |
| **Matrix** | ⭐⭐ 中等 | 插件支持 |
| **WebChat** | ⭐ 最简单 | 内置浏览器界面 |

### 通道配置模式

所有通道共享相同的配置结构：

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",      // 通道特定凭证
      dmPolicy: "pairing",      // 私聊策略
      allowFrom: ["tg:123"],    // 允许列表
      groups: {                 // 群聊配置
        "*": { requireMention: true }
      },
    },
  },
}
```

### 私聊策略 (dmPolicy)

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `pairing` | 未知用户收到配对码 | **默认，推荐** |
| `allowlist` | 只有列表中用户可对话 | 严格限制 |
| `open` | 允许所有人 | 公开服务 |
| `disabled` | 禁止私聊 | 只在群聊使用 |

### 快速设置示例

#### Telegram（最快）

1. 创建 Bot：
   - 打开 Telegram，找 @BotFather
   - 发送 `/newbot`
   - 获取 Bot Token

2. 配置：
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123456:ABC-DEF",
    },
  },
}
```

3. 重启 Gateway：
```bash
openclaw gateway restart
```

#### WhatsApp

1. 启动 Gateway：
```bash
openclaw gateway
```

2. 获取 QR 码：
```bash
openclaw qr whatsapp
# 或在控制面板查看
```

3. 用 WhatsApp 扫码配对

4. 配置访问控制：
```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      allowFrom: ["wa:+15555550123"],
    },
  },
}
```

#### Discord

1. 创建 Discord Bot：
   - Discord Developer Portal
   - New Application → Bot
   - 获取 Token

2. 添加 Bot 到服务器：
   - OAuth2 → URL Generator
   - 选择权限（Send Messages, Read Messages）
   - 邀请链接加入服务器

3. 配置：
```json5
{
  channels: {
    discord: {
      enabled: true,
      botToken: "your-bot-token",
      servers: {
        "your-server-id": {
          channels: ["channel-1", "channel-2"],
        },
      },
    },
  },
}
```

### 群聊行为

#### 提及规则

群聊默认需要提及才回复：

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },  // 所有群都需要提及
        "family-group": { requireMention: false },  // 特定群不需要
      },
    },
  },
}
```

#### 提及模式

```json5
{
  agents: {
    list: [{
      id: "main",
      groupChat: {
        mentionPatterns: ["@openclaw", "openclaw", "助手"],
      },
    }],
  },
}
```

**提及类型：**
- **元数据提及**：平台原生 @mention（WhatsApp 点选、Telegram @bot）
- **文本模式**：消息中的文本匹配（如 "openclaw")

### 多通道同时运行

```json5
{
  channels: {
    telegram: { enabled: true, botToken: "..." },
    whatsapp: { enabled: true },
    discord: { enabled: true, botToken: "..." },
  },
}
```

Gateway 自动路由：
- 消息从哪个通道来，回复到哪个通道
- 每个通道独立会话

### 通道状态检查

```bash
# 检查所有通道状态
openclaw channels status

# 详细探测（需要 Gateway 运行）
openclaw channels status --probe
```

## 🔗 知识关联

### Channels 与其他概念

| 概念 | 与 Channels 的关系 |
|------|---------------------|
| Gateway | Gateway 管理 Channel 连接 |
| Session | 每个 Channel 有独立会话 |
| dmPolicy | 访问控制策略 |
| Pairing | 配对流程管理用户访问 |

### 内置 vs 插件通道

| 类型 | 说明 | 例子 |
|------|------|------|
| 内置 | OpenClaw 核心支持 | Telegram, WhatsApp, Discord |
| 插件 | 扩展包支持 | Matrix, IRC, Nostr, QQ Bot |

插件通道安装：
```bash
openclaw plugins install matrix
```

### WebChat（内置浏览器界面）

WebChat 是内置通道，无需额外配置：

```bash
openclaw dashboard
# 打开 http://127.0.0.1:18789
```

适合：
- 本地测试
- 不想配置外部通道
- 开发调试

## ⚠️ 注意事项

### WhatsApp 特别说明

- 需要 QR 配对（类似手机登录）
- 存储会话状态在磁盘
- 不要频繁切换设备（可能被封）

### iMessage 选项

**推荐：BlueBubbles**
- 全功能支持
- REST API 接口
- 编辑、撤回、特效等

**遗留：imsg CLI**
- 已废弃
- 不推荐新安装

### 安全建议

1. **使用 pairing 策略**：防止未知用户滥用
2. **配置 allowFrom**：限制访问范围
3. **群聊启用 requireMention**：避免群内过度活跃
4. **定期检查通道状态**：`channels status --probe`

## 📝 总结

Channel 是"电话线接口"：
- 连接各种聊天平台
- 每个平台需要特定配置
- 统一的访问控制策略

快速上手：
- Telegram 最简单（Bot Token）
- WhatsApp 需要 QR 配对
- Discord 需要服务器配置

关键配置：
- `dmPolicy`：私聊策略
- `groups`：群聊规则
- `allowFrom`：访问列表

下一步：[Gateway 网关](./06-Gateway网关.md) → 学习运维与监控。

---

*费曼学习法：概念解释 → 类比理解 → 实践示例 → 知识关联*