# 子 Agent 系统

> 🤖 多 Agent 路由与隔离

---

## 第一步：概念解释

**子 Agent 是什么？**
- 就像「多个接线员」
- 不同 Agent 处理不同任务
- 每个 Agent 有独立的工作目录和会话

**类比**：
- Gateway = 电话总机
- Agent = 接线员
- 子 Agent = 不同专长的接线员
  - 家务接线员（home）
  - 工作接线员（work）
  - 开发接线员（dev）

**为什么需要多 Agent？**
- 隔离不同场景（工作 vs 生活）
- 不同模型配置（便宜模型 vs 强力模型）
- 不同权限（公开 Agent vs 私密 Agent）

---

## 第二步：类比理解

| 场景 | 子 Agent 配置 |
|------|---------------|
| 工作用 Slack，生活用 WhatsApp | 两个 Agent，分别绑定通道 |
| 简单问题用便宜模型，复杂问题用强力模型 | 多模型 Agent |
| 临时任务用隔离沙箱 | 子 Agent + sandbox |
| 长时间代码任务 | coding-agent 子 Agent |

**Agent 路由流程**：
```
消息到达 Gateway
    ↓
匹配 bindings 规则
    ↓
选择对应 Agent
    ↓
Agent 在独立 Session 中处理
    ↓
返回结果
```

---

## 第三步：动手实践

### 配置多 Agent

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "anthropic/claude-sonnet-4-6" },
    },
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
      { id: "dev", workspace: "~/.openclaw/workspace-dev", skills: ["coding-agent"] },
    ],
  },
}
```

### 配置路由规则

```json5
{
  bindings: [
    // WhatsApp 消息 → home Agent
    { agentId: "home", match: { channel: "whatsapp" } },
    // Slack 消息 → work Agent
    { agentId: "work", match: { channel: "slack" } },
    // Discord dev 频道 → dev Agent
    { agentId: "dev", match: { channel: "discord", channelId: "dev-channel-id" } },
  ],
}
```

### 路由匹配规则

**匹配顺序**（优先级从高到低）：

1. 精确匹配：`channel + accountId + channelId + threadId`
2. 通道匹配：`channel + accountId`
3. 通道默认：`channel`
4. 全局默认：`default: true` 的 Agent

### Agent 配置差异

**不同模型**：
```json5
{
  agents: {
    list: [
      {
        id: "cheap",
        model: { primary: "openai/gpt-4o-mini" },
      },
      {
        id: "powerful",
        model: { primary: "anthropic/claude-opus-4-6" },
      },
    ],
  },
}
```

**不同 Skills**：
```json5
{
  agents: {
    list: [
      { id: "general", skills: ["weather", "github"] },
      { id: "coding", skills: ["coding-agent", "github"] },
      { id: "minimal", skills: [] },
    ],
  },
}
```

**不同沙箱**：
```json5
{
  agents: {
    list: [
      { id: "trusted", sandbox: { mode: "off" } },
      { id: "sandboxed", sandbox: { mode: "session" } },
    ],
  },
}
```

---

## 子 Agent 执行模式

### ACP Harness（子 Agent 会话）

当主 Agent 需要执行长时间任务：

```
主 Agent 收到复杂代码任务
    ↓
使用 sessions_spawn 创建子 Agent
    ↓
子 Agent 在独立 Session 中运行
    ↓
完成后自动报告结果回主 Agent
    ↓
主 Agent 继续处理
```

**Skills 中的子 Agent**：
- `coding-agent` Skill：启动 Codex/Claude Code 子 Agent
- `gh-issues` Skill：创建子 Agent 处理 GitHub Issues

### 会话隔离

| 模式 | 说明 |
|------|------|
| `session` | 每个子 Agent 任务独立 Session |
| `agent` | 每个 Agent 持久 Session |
| `shared` | 共享 Session |

---

## 第四步：知识关联

### 主 Agent vs 子 Agent

| 角色 | 职责 |
|------|------|
| 主 Agent | 处理用户消息，路由任务 |
| 子 Agent | 执行特定任务，独立运行 |
| Gateway | 协调所有 Agent |

### Agent 工作目录

每个 Agent 有独立的 `workspace`：
- 文件操作隔离
- 工具执行隔离
- 避免误删其他 Agent 文件

### Agent 状态查看

```bash
# 查看所有 Agent
openclaw agents list

# 查看特定 Agent Session
openclaw sessions list --agent home

# 查看 Agent 日志
openclaw logs --agent dev
```

---

## 子 Agent 最佳实践

### 分离工作/生活

```json5
{
  agents: {
    list: [
      { id: "personal", default: true },
      { id: "professional" },
    ],
  },
  bindings: [
    { agentId: "personal", match: { channel: "whatsapp" } },
    { agentId: "professional", match: { channel: "slack" } },
  ],
}
```

### 任务隔离

```json5
{
  agents: {
    list: [
      { id: "main", sandbox: { mode: "off" } },
      { id: "sandboxed", sandbox: { mode: "session" } },
    ],
  },
}
```

危险任务（执行未知代码）用 sandboxed Agent。

### 成本控制

```json5
{
  agents: {
    list: [
      { id: "simple", model: { primary: "openai/gpt-4o-mini" } },
      { id: "complex", model: { primary: "anthropic/claude-opus-4-6" } },
    ],
  },
}
```

简单问题用便宜模型。

---

## 子 Agent 命令速查

```bash
# 查看 Agent 列表
openclaw agents list

# 查看 Agent 状态
openclaw agent status --agent home

# 手动路由到特定 Agent
# 在消息中指定：@dev 写一个函数

# 查看 Sessions
openclaw sessions list
```

---

## 下一步

- [06-Gateway网关](./06-gateway.md) - 网关架构
- [09-安全最佳实践](./09-security.md) - 沙箱与权限
- [13-高级模式](./13-advanced-patterns.md) - 分布式 Agent

---

> ✅ 多 Agent 让你可以分离不同场景，就像雇佣不同专长的员工。