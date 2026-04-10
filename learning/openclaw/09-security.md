# 安全最佳实践

> 🔐 保护你的 Agent 和数据

---

## 第一步：概念解释

**OpenClaw 安全是什么？**
- 就像「家里的锁和门禁」
- 控制：
  - 谁能访问你的 Agent
  - Agent 能做什么
  - 数据如何保护

**类比**：
- Gateway Token = 门锁钥匙
- dmPolicy = 门禁规则（谁能进）
- Sandbox = 保险柜（危险操作隔离）
- allowFrom = 允许名单（白名单）

**安全层次**：

```
1. 访问控制 - 谁能发消息给 Agent
2. 工具权限 - Agent 能用什么工具
3. 沙箱隔离 - 危险操作在哪里执行
4. 数据保护 - API Key、Token 如何存储
```

---

## 第二步：类比理解

| 安全措施 | 类比 | 保护对象 |
|----------|------|----------|
| Gateway Token | 门锁 | Gateway 入口 |
| dmPolicy: pairing | 需要密码进门 | 新用户验证 |
| allowFrom 白名单 | VIP名单 | 已验证用户 |
| requireMention | 需要敲门 | 群聊触发 |
| Sandbox mode | 保险柜 | 危险操作 |
| Secrets 管理 | 密码本 | API Keys |

---

## 第三步：动手实践

### Gateway Token

```json5
{
  gateway: {
    auth: {
      token: "your-strong-random-token",  // 强随机 Token
    },
  },
}
```

**Token 生成**：
```bash
# 生成随机 Token
openssl rand -base64 32
```

### 访问策略（dmPolicy）

| 策略 | 安全性 | 说明 |
|------|--------|------|
| `pairing` | ⭐⭐⭐ | 新用户需配对码验证 |
| `allowlist` | ⭐⭐⭐⭐ | 只允许白名单用户 |
| `open` | ⭐ | 任何人都能用（危险） |
| `disabled` | - | 禁用私聊 |

**推荐配置**：
```json5
{
  channels: {
    telegram: {
      dmPolicy: "pairing",  // 新用户需验证
    },
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15555550123"],  // 只允许自己
    },
  },
}
```

### 群聊安全

**requireMention**（群聊需 @提及）：
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

**为什么？**
- 防止 Agent 响应所有群消息（噪音）
- 防止敏感信息泄露给群成员

### 沙箱配置

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",  // 非主 Agent 使用沙箱
        scope: "agent",
      },
    },
  },
}
```

**mode 选项**：

| 值 | 说明 |
|----|------|
| `off` | 不使用沙箱（信任） |
| `non-main` | 子 Agent 使用沙箱 |
| `all` | 所有 Agent 使用沙箱 |

**构建沙箱镜像**：
```bash
scripts/sandbox-setup.sh
```

### Secrets 管理

**不要直接写入 API Key**：
```json5
// ❌ 不推荐
{
  models: {
    providers: {
      openai: { apiKey: "sk-xxx..." },
    },
  },
}
```

**使用环境变量**：
```json5
// ✅ 推荐
{
  models: {
    providers: {
      openai: { apiKey: "${OPENAI_API_KEY}" },
    },
  },
}
```

**使用 SecretRef**：
```json5
// ✅ 更安全
{
  models: {
    providers: {
      openai: {
        apiKey: {
          source: "env",
          provider: "default",
          id: "OPENAI_API_KEY",
        },
      },
    },
  },
}
```

### 工具权限

**限制 Skills**：
```json5
{
  agents: {
    defaults: {
      skills: ["weather"],  // 只允许天气查询
    },
    list: [
      { id: "trusted", skills: ["github", "browser", "exec"] },
      { id: "restricted", skills: [] },  // 无 Skills
    ],
  },
}
```

---

## 第四步：知识关联

### Pairing 流程

```
新用户发消息
    ↓
Gateway 检查 dmPolicy = pairing
    ↓
用户未配对 → 发送配对码请求
    ↓
用户输入配对码（如从邮件获取）
    ↓
配对成功 → 用户加入允许名单
    ↓
后续消息正常处理
```

### 安全威胁模型

| 威胁 | 防护措施 |
|------|----------|
| 未授权访问 | dmPolicy + allowFrom |
| API Key 泄露 | Secrets 管理 + 环境变量 |
| 恶意代码执行 | Sandbox + 工具权限 |
| 群聊信息泄露 | requireMention |
| 工具滥用 | Skills 白名单 |
| 提示注入 | 不可信输入处理 |

### Tailscale 安全访问

```json5
{
  gateway: {
    tailscale: {
      enabled: true,
      hostname: "openclaw",
    },
    bind: "127.0.0.1",  // 只绑定本地
  },
}
```

**优点**：
- 不暴露公网端口
- 需要 Tailscale 账号才能访问
- 加密传输

---

## 安全检查清单

```bash
# 运行安全检查
openclaw doctor --security

# 检查配置
openclaw config get gateway.auth.token
openclaw config get channels.telegram.dmPolicy
```

**检查项**：

| 项目 | 检查 |
|------|------|
| Gateway Token | 是否设置强 Token |
| dmPolicy | 是否为 open（危险） |
| allowFrom | 是否配置白名单 |
| Sandbox | 是否启用沙箱 |
| Secrets | API Key 是否直接暴露 |
| 群聊 | 是否 requireMention |

---

## Hooks 安全

**Hooks 特殊安全**：

```json5
{
  hooks: {
    enabled: true,
    token: "dedicated-hook-token",  // 专用 Token
    path: "/hooks",                 // 不用 "/"
    allowRequestSessionKey: false,  // 禁止请求指定 session
    allowedSessionKeyPrefixes: ["hook:"],
  },
}
```

**原则**：
1. Hook 内容视为不可信输入
2. 不允许 Hook 指定 Session（防止劫持）
3. 使用专用 Token（不用 Gateway Token）
4. 限制 Session Key 前缀

---

## 下一步

- [02-配置详解](./02-configuration.md) - 配置文件详解
- [10-故障排查](./10-troubleshooting.md) - 安全问题排查
- [安全文档](https://docs.openclaw.ai/gateway/security) - 官方安全指南

---

> ✅ 安全是第一要务。从 dmPolicy 和 allowFrom 开始配置。