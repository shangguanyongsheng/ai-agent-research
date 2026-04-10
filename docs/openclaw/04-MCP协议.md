# OpenClaw MCP 协议

> 使用费曼学习法：理解 Model Context Protocol 的两种用法。

## 📖 概念解释

**什么是 MCP？**

MCP (Model Context Protocol) 是一个标准协议，用于：
1. AI 应用连接外部工具和数据源
2. 工具/数据源向 AI 应用暴露能力

OpenClaw 支持两种 MCP 角色：
- **作为 MCP 服务器**：让其他 AI 应用（如 Claude Code）连接 OpenClaw
- **作为 MCP 客户端**：连接其他 MCP 服务器获取工具

## 🎯 类比理解

**把 MCP 想象成"通用电源插座"**

- 不同电器（AI 应用）需要插头才能使用电源（工具）
- MCP 定义了标准插头形状
- OpenClaw 可以：
  - 提供"插座"（作为服务器，让其他应用插入）
  - 使用"插头"（作为客户端，插入其他服务器）

就像 USB 是通用接口，MCP 是 AI 工具的通用接口。

## 🔧 实践示例

### OpenClaw 作为 MCP 服务器

**场景：** Claude Code、Codex 等需要访问 OpenClaw 的聊天通道。

#### 启动 MCP 服务器

```bash
# 本地 Gateway
openclaw mcp serve

# 远程 Gateway
openclaw mcp serve --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# 启用 Claude 通道通知
openclaw mcp serve --claude-channel-mode on
```

#### MCP 客户端配置

在 Claude Code 或其他 MCP 客户端的配置中：

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "openclaw",
      "args": [
        "mcp",
        "serve",
        "--url",
        "wss://gateway-host:18789",
        "--token-file",
        "/path/to/gateway.token"
      ]
    }
  }
}
```

#### MCP 工具列表

`openclaw mcp serve` 提供的工具：

| 工具 | 说明 |
|------|------|
| `conversations_list` | 列出最近会话 |
| `conversation_get` | 获取单个会话详情 |
| `messages_read` | 读取消息历史 |
| `attachments_fetch` | 获取附件元数据 |
| `events_poll` | 获取排队事件 |
| `events_wait` | 等待新事件 |
| `messages_send` | 发送消息回复 |
| `permissions_list_open` | 列出待审批请求 |
| `permissions_respond` | 处理审批请求 |

#### Claude 通道模式

当启用 Claude 通道模式：
- 标准 MCP 工具仍可用
- 新消息作为 Claude 特定通知推送
- 支持权限请求通知

**通知类型：**
- `notifications/claude/channel` — 新消息
- `notifications/claude/channel/permission` — 权限请求

### OpenClaw 作为 MCP 客户端

**场景：** OpenClaw Agent 需要使用其他 MCP 服务器提供的工具。

#### 管理 MCP 服务器定义

```bash
# 列出已配置的 MCP 服务器
openclaw mcp list

# 查看某个服务器详情
openclaw mcp show context7 --json

# 添加 MCP 服务器
openclaw mcp set context7 '{"command":"uvx","args":["context7-mcp"]}'
openclaw mcp set docs '{"url":"https://mcp.example.com"}'

# 删除 MCP 服务器
openclaw mcp unset context7
```

#### 配置文件结构

```json5
{
  mcp: {
    servers: {
      "context7": {
        command: "uvx",
        args: ["context7-mcp"],
      },
      "remote-tools": {
        url: "https://mcp.example.com",
        headers: { "Authorization": "Bearer <token>" },
      },
    },
  },
}
```

#### 传输类型

**stdio（本地进程）：**

```json5
{
  command: "uvx",           // 可执行文件
  args: ["context7-mcp"],   // 参数
  env: { "API_KEY": "..." }, // 环境变量
  cwd: "/path/to/work",     // 工作目录
}
```

**SSE（远程 HTTP）：**

```json5
{
  url: "https://mcp.example.com", // 远程服务器
  headers: { "Authorization": "Bearer token" },
  connectionTimeoutMs: 10000,
}
```

**Streamable HTTP：**

```json5
{
  url: "https://mcp.example.com/stream",
  transport: "streamable-http",  // 指定传输类型
  headers: { "Authorization": "Bearer token" },
}
```

### 工作流程

#### 服务器模式流程

```
MCP 客户端 (Claude Code)
      ↓ spawn process
openclaw mcp serve
      ↓ WebSocket
OpenClaw Gateway
      ↓
聊天通道 (WhatsApp/Telegram)
```

1. MCP 客户端启动 `openclaw mcp serve`
2. 桥接连接到 Gateway
3. Gateway 会话变为 MCP 会话
4. 实时事件排队到内存
5. MCP 工具提供访问接口

#### 客户端模式流程

```
OpenClaw Agent
      ↓
Gateway (读取 mcp.servers 配置)
      ↓
连接 MCP 服务器
      ↓
获取工具列表
```

1. Agent 需要外部工具
2. Gateway 读取 MCP 配置
3. 连接配置的服务器
4. 工具暴露给 Agent

## 🔗 知识关联

### MCP 与其他概念

| 概念 | 与 MCP 的关系 |
|------|---------------|
| Skills | Skills 教 Agent 使用 MCP 工具 |
| Gateway | Gateway 管理 MCP 连接 |
| Channels | MCP 服务器暴露 Channel 会话 |
| Tools | MCP 工具是 Tools 的一种来源 |

### MCP vs ACP

| 功能 | MCP | ACP |
|------|-----|-----|
| OpenClaw 托管运行时 | ❌ | ✅ |
| 连接外部通道 | ✅ | ❌ |
| 标准 AI 协议 | ✅ | ✅ |

**使用 MCP：** 其他 AI 应用需要访问 OpenClaw 通道
**使用 ACP：** OpenClaw 托管编码 Agent 运行时

```bash
# MCP：OpenClaw 作为桥梁
openclaw mcp serve

# ACP：OpenClaw 托管 Agent
openclaw acp
```

## ⚠️ 重要限制

### 服务器模式限制

| 限制 | 说明 |
|------|------|
| 会话发现 | 需要 Gateway 已有路由元数据 |
| 事件队列 | 仅连接时存在，断开后消失 |
| 推送 | 仅 Claude 特定模式 |
| 审批列表 | 仅当前连接期间观察到的 |

### 客户端模式限制

- `mcp set/unset` 只修改配置
- 不验证服务器可达性
- 运行时适配器决定支持哪些传输

## 📝 总结

MCP 是 AI 工具的"通用插座"：

**OpenClaw 作为服务器：**
- 让 Claude Code 等访问聊天通道
- 提供 `conversations_list`, `messages_send` 等工具
- 支持 Claude 特定通知模式

**OpenClaw 作为客户端：**
- 连接其他 MCP 服务器获取工具
- 支持 stdio、SSE、streamable-http 传输
- 配置存储在 `mcp.servers`

下一步：[Channels 通道](./05-Channels通道.md) → 学习支持的聊天平台。

---

*费曼学习法：概念解释 → 类比理解 → 实践示例 → 知识关联*