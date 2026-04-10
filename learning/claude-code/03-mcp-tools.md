# MCP 工具连接

> ⏱️ 60 分钟 | 📍 第三章

[← 返回导航](README.md) | [上一章：核心概念](02-core-concepts.md) | [下一章：Skills 和 Hooks →](04-skills-hooks.md)

---

## 知识点 1：MCP 是什么？

### 第一步：概念解释（简单语言）

**MCP = Model Context Protocol**，是一个开放标准，让 Claude Code 能连接外部工具和数据源。

简单说：MCP 让 Claude 能"看到"更多东西、操作更多工具。

### 第二步：类比理解（生活例子）

Claude Code 就像一个工作人员，但默认情况下它只能访问你电脑上的文件。MCP 就像是给这个工作人员开通了各种"通道"：
- 连接 Google Drive → 能读取设计文档
- 连接 Jira → 能查看和更新任务
- 连接数据库 → 能查询数据
- 连接 Slack → 能发送消息

### 第三步：代码实践（动手实验）

**MCP 配置文件位置**：
```
~/.claude/.mcp.json          # 全局配置
your-project/.mcp.json       # 项目级配置
```

**基本配置示例**：
```json
{
  "mcpServers": {
    "github": {
      "command": "gh",
      "args": ["mcp", "start"]
    },
    "database": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@host/db"
      }
    }
  }
}
```

### 第四步：知识关联

MCP 服务器类型：
- **HTTP**：通过 HTTP 连接远程服务
- **SSE**：Server-Sent Events，实时推送
- **Stdio**：本地命令行工具

---

## 知识点 2：配置 MCP 服务器

### 第一步：概念解释（简单语言）

每个 MCP 服务器都是一个独立的程序，Claude Code 通过配置文件知道如何启动和连接它们。

### 第二步：类比理解（生活例子）

就像给助手配备不同的工具箱：
- GitHub 工具箱 → 处理 PR、Issues
- 数据库工具箱 → 查询数据
- Slack 工具箱 → 发送消息

### 第三步：代码实践（动手实验）

**示例 1：GitHub MCP**
```json
{
  "mcpServers": {
    "github": {
      "command": "gh",
      "args": ["mcp", "start"]
    }
  }
}
```

**示例 2：PostgreSQL MCP**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

**示例 3：Google Drive MCP**
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-gdrive"]
    }
  }
}
```

### 第四步：知识关联

配置好后，Claude 会自动发现这些工具，并在需要时使用它们。

---

## 知识点 3：使用 MCP 工具

### 第一步：概念解释（简单语言）

配置 MCP 后，Claude 会自动知道有哪些工具可用。你只需要描述需求，Claude 会选择合适的工具。

### 第二步：类比理解（生活例子）

就像告诉助手"帮我查一下上周的销售数据"——助手会自己决定是用数据库查询，还是查 Excel 文件，还是问 API。

### 第三步：代码实践（动手实验）

**让 Claude 使用 MCP 工具**：
```text
> 列出我 GitHub 上所有的 open issues

> 查询数据库中 users 表最近 7 天的新增用户

> 从 Google Drive 读取"产品需求文档.docx"
```

**查看可用的 MCP 工具**：
```bash
claude /mcp
```

### 第四步：知识关联

- Claude 会根据你的请求自动选择工具
- 你也可以明确指定要用的工具
- MCP 工具和内置工具（文件操作、命令执行）可以组合使用

---

## 知识点 4：常见 MCP 服务器

### 第一步：概念解释（简单语言）

社区已经提供了很多现成的 MCP 服务器，覆盖常见需求。

### 第二步：类比理解（生活例子）

就像 App Store 里的应用——你需要什么功能，就"安装"对应的 MCP 服务器。

### 第三步：代码实践（动手实验）

| MCP 服务器 | 功能 | 安装 |
|-----------|------|------|
| **GitHub** | PR、Issues、Repos | `gh mcp start` |
| **PostgreSQL** | 数据库查询 | `@anthropic-ai/mcp-server-postgres` |
| **Google Drive** | 读取文档 | `@anthropic-ai/mcp-server-gdrive` |
| **Slack** | 发送消息 | `@anthropic-ai/mcp-server-slack` |
| **Puppeteer** | 网页操作 | `@anthropic-ai/mcp-server-puppeteer` |
| **Filesystem** | 安全文件操作 | `@anthropic-ai/mcp-server-filesystem` |

### 第四步：知识关联

- [MCP Connectors 目录](https://claude.com/partners/mcp)
- 可以自己开发 MCP 服务器
- MCP 是开放标准，任何人都可以贡献

---

## 知识点 5：开发自定义 MCP

### 第一步：概念解释（简单语言）

如果现成的 MCP 不够用，你可以开发自己的 MCP 服务器，让 Claude 连接任何你想要的工具。

### 第二步：类比理解（生活例子）

就像给助手定制一个专属工具——如果你公司有内部 API，可以开发一个 MCP 让 Claude 直接调用。

### 第三步：代码实践（动手实验）

**MCP 服务器基本结构**：
```typescript
// my-mcp-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// 定义工具
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [{
      name: "my_tool",
      description: "我的自定义工具",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" }
        }
      }
    }]
  };
});

// 处理工具调用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "my_tool") {
    // 执行你的逻辑
    return { content: [{ type: "text", text: "结果" }] };
  }
});

// 启动服务器
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 第四步：知识关联

- MCP SDK 支持 TypeScript 和 Python
- 开发文档：https://modelcontextprotocol.io
- 测试 MCP 服务器：`npx @anthropic-ai/mcp-inspector`

---

## 总结检查清单

完成本章后，你应该能够：

- [ ] 理解 MCP 的作用
- [ ] 配置 MCP 服务器
- [ ] 使用现成的 MCP 工具
- [ ] 知道常见的 MCP 服务器
- [ ] 了解如何开发自定义 MCP

---

## 下一步

[下一章：Skills 和 Hooks →](04-skills-hooks.md)

学习如何创建自定义工作流和自动化脚本。