# Gateway 网关

> 🏠 Gateway 是 OpenClaw 的核心枢纽

---

## 第一步：概念解释

**Gateway 是什么？**
- 就像「电话总机」
- 单一进程，监听所有通道
- 协调 Agent、通道、用户之间的通信

**类比**：
- Gateway = 电话总机
- 通道插件 = 电话线路
- Agent = 接线员
- 用户 = 打电话的人

**Gateway 职责**：
- 接收各通道消息
- 路由到对应 Agent
- 管理 Session（会话）
- 处理工具调用
- 发送回复到通道

---

## 第二步：类比理解

| Gateway 功能 | 类比 |
|--------------|------|
| 监听端口 | 总机开机 |
| 连接通道 | 接入电话线路 |
| Session 管理 | 记录通话记录 |
| Agent 路由 | 分配接线员 |
| 工具调用 | 查询资料库 |
| 配置热重载 | 调整总机设置 |

**Gateway 架构**：
```
┌─────────────┐
│  Gateway    │ ← 单进程，端口 18789
│  (Node.js)  │
└─────┬───────┤
      │       │
  ┌───┴───┬───┴───┬───┐
  │       │       │   │
通道1   通道2   通道3  WebUI
(Discord WhatsApp Telegram Control)
      │       │       │
      └───────┴───────┘
              │
         Agent Session
```

---

## 第三步：动手实践

### Gateway 基础命令

```bash
# 启动 Gateway
openclaw gateway start

# 停止 Gateway
openclaw gateway stop

# 重启 Gateway
openclaw gateway restart

# 查看状态
openclaw gateway status

# 查看日志
openclaw logs

# 健康检查
openclaw doctor
```

### Gateway 配置

```json5
{
  gateway: {
    port: 18789,               // 监听端口
    bind: "127.0.0.1",         // 绑定地址
    auth: {
      token: "your-token",     // Gateway Token
    },
    reload: {
      mode: "hybrid",          // 配置重载模式
    },
    controlUi: {
      enabled: true,           // 控制面板
    },
  },
}
```

### Gateway 状态查看

```bash
openclaw gateway status
```

输出示例：
```
Gateway Status: running
Port: 18789
Uptime: 2h 30m
Active Channels: 3
  - telegram: connected
  - whatsapp: connected
  - discord: connected
Active Sessions: 5
```

---

## Gateway 核心组件

### Session 管理

**Session = 会话 = 对话历史**

```json5
{
  session: {
    dmScope: "per-channel-peer",  // 会话隔离
    reset: {
      mode: "daily",              // 重置策略
      atHour: 4,
    },
    threadBindings: {
      enabled: true,              // Thread 绑定
      idleHours: 24,
    },
  },
}
```

**dmScope 选项**：

| 值 | 说明 |
|----|------|
| `main` | 所有用户共享会话 |
| `per-peer` | 每用户独立会话 |
| `per-channel-peer` | 每通道每用户独立 |
| `per-account-channel-peer` | 最细粒度隔离 |

### Agent 路由

**bindings = 路由规则**

```json5
{
  bindings: [
    { agentId: "home", match: { channel: "whatsapp" } },
    { agentId: "work", match: { channel: "slack" } },
  ],
}
```

**路由匹配顺序**：
1. 匹配 channel + accountId
2. 匹配 channel only
3. 使用 default agent

### 消息处理流程

```
通道收到消息
    ↓
Gateway 接收
    ↓
路由匹配 Agent
    ↓
查找/创建 Session
    ↓
发送给 Agent
    ↓
Agent 处理（模型+工具）
    ↓
返回回复
    ↓
Gateway 发送到通道
```

---

## Gateway 网络

### 本地访问

默认绑定 `127.0.0.1:18789`

```bash
# 打开控制面板
openclaw dashboard

# 或直接访问
http://127.0.0.1:18789
```

### 远程访问

**方式一：Tailscale**

```json5
{
  gateway: {
    tailscale: {
      enabled: true,
      hostname: "openclaw",
    },
  },
}
```

**方式二：SSH 隧道**

```bash
# 本地执行
ssh -L 18789:127.0.0.1:18789 user@server

# 然后访问
http://localhost:18789
```

**方式三：公开端口（需安全配置）**

```json5
{
  gateway: {
    bind: "0.0.0.0",
    auth: { token: "strong-token" },
    cors: { origins: ["https://your-app.com"] },
  },
}
```

---

## 第四步：知识关联

### Gateway 协议

Gateway 使用 RPC 协议：
- Agent ↔ Gateway: JSON-RPC over WebSocket/stdin
- 通道 ↔ Gateway: 插件协议
- WebUI ↔ Gateway: HTTP + WebSocket

### Gateway 资源

| 资源 | 位置 |
|------|------|
| 配置文件 | `~/.openclaw/openclaw.json` |
| 会话记录 | `~/.openclaw/sessions.json` |
| 日志 | `~/.openclaw/logs/` |
| 运行状态 | `~/.openclaw/daemon/` |

### 多 Gateway

```json5
// 第一台机器
{ gateway: { port: 18789, bind: "0.0.0.0" } }

// 第二台机器（负载分担）
{ gateway: { port: 18789, bind: "0.0.0.0" } }
```

通过 `bindings` 分布式路由。

---

## Gateway 命令速查

```bash
# 基础管理
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status

# 日志查看
openclaw logs
openclaw logs --follow
openclaw logs --filter channel:telegram

# 健康诊断
openclaw doctor
openclaw doctor --fix

# RPC 调用
openclaw gateway call config.get
openclaw gateway call sessions.list
```

---

## 下一步

- [07-子Agent系统](./07-subagents.md) - 多 Agent 路由
- [09-安全最佳实践](./09-security.md) - Gateway 安全
- [10-故障排查](./10-troubleshooting.md) - Gateway 故障排查

---

> ✅ Gateway 是 OpenClaw 的心脏，理解它就是理解整个系统。