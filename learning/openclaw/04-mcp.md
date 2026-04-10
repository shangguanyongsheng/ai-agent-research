# MCP 协议

> 🔌 Model Context Protocol - AI 与工具的标准接口

---

## 第一步：概念解释

**MCP 是什么？**
- 就像「USB 接口」标准
- AI 模型（Claude/GPT）通过 MCP 与工具通信
- 标准化的工具调用协议

**类比**：
- USB = MCP 协议
- USB 设备 = MCP Server（提供工具）
- 电脑 = AI Agent
- 数据传输 = 工具调用

**为什么需要 MCP？**
- 不同 AI 模型工具接口不同
- MCP 提供统一标准
- 工具开发者只需遵循 MCP，所有模型都能用

---

## 第二步：类比理解

| MCP 概念 | 类比 |
|----------|------|
| MCP Server | USB 设备（键盘/鼠标） |
| MCP Client | USB 主机（电脑） |
| Tool | 设备功能（键盘按键） |
| Resource | 设备数据（鼠标位置） |
| Prompt | 设备预设（快捷键） |

**MCP 架构**：
```
AI Agent (Client)
    ↓ MCP 协议
MCP Server (工具提供者)
    ↓
实际工具（文件/数据库/API）
```

---

## 第三步：动手实践

### OpenClaw 中的 MCP

OpenClaw 内置 MCP 客户端，可以：
- 连接任意 MCP Server
- 将 MCP 工具暴露给 Agent

**配置 MCP Server**：

```json5
{
  plugins: {
    entries: {
      "filesystem": {
        type: "mcp",
        command: "npx -y @anthropic-ai/mcp-server-filesystem",
        args: ["/path/to/allowed/dir"],
      },
      "github": {
        type: "mcp",
        command: "npx -y @anthropic-ai/mcp-server-github",
        env: { GITHUB_TOKEN: "${GITHUB_TOKEN}" },
      },
    },
  },
}
```

### 常用 MCP Servers

| Server | 提供的工具 | 安装 |
|--------|------------|------|
| filesystem | 文件读写 | `@anthropic-ai/mcp-server-filesystem` |
| github | GitHub API | `@anthropic-ai/mcp-server-github` |
| brave-search | 网页搜索 | `@anthropic-ai/mcp-server-brave-search` |
| puppeteer | 浏览器控制 | `@anthropic-ai/mcp-server-puppeteer` |
| slack | Slack API | `@anthropic-ai/mcp-server-slack` |

### MCP CLI 操作

使用 `mcporter` CLI：

```bash
# 列出已配置的 MCP servers
mcporter list

# 调用 MCP 工具
mcporter call filesystem read_file --params '{"path": "/tmp/test.txt"}'

# 查看工具 schema
mcporter schema github
```

### 自定义 MCP Server

**创建 MCP Server**（Node.js）：

```typescript
import { Server } from "@anthropic-ai/mcp";

const server = new Server({
  name: "my-server",
  version: "1.0.0",
});

// 定义工具
server.tool("my-tool", {
  description: "My custom tool",
  parameters: { type: "object", properties: { input: { type: "string" } } },
}, async (params) => {
  return { content: [{ type: "text", text: `Result: ${params.input}` }] };
});

server.start();
```

---

## 第四步：知识关联

### MCP vs Skills

| 区别 | Skills | MCP |
|------|--------|-----|
| 定义 | Agent 指导包 | 工具协议 |
| 内容 | SKILL.md + 脚本 | 标准化工具接口 |
| 灵活性 | 高度定制 | 标准化 |
| 兼容性 | OpenClaw 专用 | 跨模型通用 |

**关系**：
- Skill 可以调用 MCP 工具
- Skill 提供使用指导
- MCP 提供工具实现

### MCP 工具类型

**Tools**（工具）：
- 可执行的操作
- 输入参数 → 输出结果

**Resources**（资源）：
- 可读取的数据
- 文件、数据库记录

**Prompts**（预设）：
- 预定义的提示模板
- 快速调用常用功能

---

## MCP 配置详解

### stdio MCP Server

```json5
{
  plugins: {
    entries: {
      "my-server": {
        type: "mcp",
        command: "node",
        args: ["./my-mcp-server.js"],
        env: { MY_API_KEY: "xxx" },
      },
    },
  },
}
```

### HTTP MCP Server

```json5
{
  plugins: {
    entries: {
      "http-server": {
        type: "mcp-http",
        url: "https://mcp-server.example.com",
        headers: { Authorization: "Bearer xxx" },
      },
    },
  },
}
```

### 多 MCP Servers

```json5
{
  plugins: {
    entries: {
      "filesystem": { type: "mcp", command: "npx -y @anthropic-ai/mcp-server-filesystem", args: ["~"] },
      "github": { type: "mcp", command: "npx -y @anthropic-ai/mcp-server-github" },
      "slack": { type: "mcp", command: "npx -y @anthropic-ai/mcp-server-slack" },
    },
  },
}
```

---

## MCP 资源链接

| 资源 | 链接 |
|------|------|
| MCP 规范 | https://anthropic.com/mcp |
| MCP Servers 列表 | https://github.com/anthropics/anthropic-cookbook/tree/main/mcp |
| OpenClaw MCP 文档 | https://docs.openclaw.ai/cli/mcp |
| mcporter CLI | https://docs.openclaw.ai/skills/mcporter |

---

## 下一步

- [03-Skills系统](./03-skills.md) - Skills 使用详解
- [MCP CLI](https://docs.openclaw.ai/cli/mcp) - MCP 命令行操作
- [创建 MCP Server](https://anthropic.com/mcp/docs/server) - 开发教程

---

> ✅ MCP 是 AI 工具的标准接口，让工具能被所有模型使用。