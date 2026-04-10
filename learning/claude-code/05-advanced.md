# 高级功能

> ⏱️ 60 分钟 | 📍 第五章

[← 返回导航](README.md) | [上一章：Skills 和 Hooks](04-skills-hooks.md) | [下一章：最佳实践 →](06-best-practices.md)

---

## 知识点 1：调度任务（Scheduled Tasks）

### 第一步：概念解释（简单语言）

让 Claude 定时执行任务——每天早上检查 PR、每周分析依赖更新、每小时检查 CI 状态。

### 第二步：类比理解（生活例子）

就像设置闹钟——不同的是这个闹钟不是叫醒你，而是叫醒 Claude 去干活。

### 第三步：代码实践（动手实验）

**方式一：Cloud Scheduled Tasks**
```text
> /schedule

# 创建云端调度任务
Claude 会在 Anthropic 的服务器上定时运行，即使你电脑关机也能执行。
```

**方式二：Desktop Scheduled Tasks**
```bash
# Desktop 应用中设置
# 任务在你的电脑上运行，可以访问本地文件
```

**方式三：/loop 命令**
```text
> /loop 5m 检查部署是否完成

# 每 5 分钟执行一次
# 用于会话内的快速轮询
```

**常见调度场景**：

| 场景 | 间隔 | 示例 |
|------|------|------|
| CI 失败分析 | 每小时 | `分析最近的 CI 失败并报告` |
| PR 审查 | 每天早上 | `审查 overnight 的 PR` |
| 依赖检查 | 每周 | `检查过期的依赖包` |
| 文档同步 | PR 合并后 | `更新文档网站` |

### 第四步：知识关联

- Cloud 任务适合长时间运行、不需要本地资源的任务
- Desktop 任务适合需要本地文件、数据库的任务
- `/loop` 适合快速轮询场景

---

## 知识点 2：远程控制（Remote Control）

### 第一步：概念解释（简单语言）

从手机或其他设备控制本地正在运行的 Claude Code 会话。离开电脑后还能继续工作。

### 第二步：类比理解（生活例子）

就像远程桌面——你在手机上操作，家里的电脑在执行。去开会路上还能让 Claude 继续干活。

### 第三步：代码实践（动手实验）

**启动远程控制**：
```bash
claude /remote on
```

**使用方式**：
1. 在手机浏览器打开提供的链接
2. 或者使用 Claude iOS App
3. 发送命令，本地 Claude 执行

**典型场景**：
```text
手机发送：> 检查测试结果，如果全部通过就合并 PR

Claude 在你的电脑上执行，你继续开会。
```

### 第四步：知识关联

- Remote Control 与 `/teleport` 配合可以在设备间转移会话
- 安全性：只有你能访问远程控制链接
- 网络要求：电脑需要在线

---

## 知识点 3：Channels（消息通道）

### 第一步：概念解释（简单语言）

让外部服务（Telegram、Discord、iMessage、Webhook）向 Claude 会话发送消息。Claude 可以响应这些消息并执行任务。

### 第二步：类比理解（生活例子）

就像给 Claude 分配了一个"公用电话号码"——任何人（或服务）都可以通过这个号码联系 Claude，请求它做事。

### 第三步：代码实践（动手实验）

**配置 Channel**：
```bash
claude /channel create telegram
# 获得一个 Telegram Bot Token
# 用户可以通过 Telegram 发送命令给 Claude
```

**使用场景**：

| Channel | 场景 |
|---------|------|
| Telegram | 团队协作，发送任务 |
| Discord | 社区管理，自动化任务 |
| iMessage | 个人快速任务 |
| Webhook | CI/CD 集成，自动化触发 |

**示例流程**：
```
用户在 Telegram 发送：
"帮我检查今天的 CI 失败原因"

Claude 执行任务并回复结果到 Telegram
```

### 第四步：知识关联

- Channels 可以与 MCP、Skills 组合
- 支持多用户同时使用
- 可以设置权限控制

---

## 知识点 4：Agent SDK

### 第一步：概念解释（简单语言）

**Agent SDK** 让开发者构建自己的 AI Agent，使用 Claude Code 的工具和能力，但有完全的控制权。

### 第二步：类比理解（生活例子）

如果说 Claude Code 是一个"现成的助手"，Agent SDK 就是"助手工具箱"——你可以用这些工具组装出任何你想要的助手。

### 第三步：代码实践（动手实验）

**Agent SDK 基本用法**：
```typescript
import { Agent } from "@anthropic-ai/agent-sdk";

const agent = new Agent({
  model: "claude-sonnet-4-20250514",
  tools: [
    // 使用 Claude Code 的工具
    "bash",
    "edit",
    "read",
    // 添加自定义工具
    myCustomTool
  ]
});

// 执行任务
const result = await agent.run("帮我分析这个项目的依赖关系");
```

**适用场景**：
- 构建自定义工作流
- 集成到现有系统
- 创建专用 Agent（如测试 Agent、部署 Agent）

### 第四步：知识关联

- Agent SDK 文档：https://platform.claude.com/docs/en/agent-sdk/overview
- 可以使用 MCP 工具
- 完全控制权限、工具访问、执行流程

---

## 知识点 5：Subagents（子代理）

### 第一步：概念解释（简单语言）

让 Claude 创建"分身"——多个子代理并行处理不同任务，最后汇总结果。

### 第二步：类比理解（生活例子）

就像项目经理分配任务给多个团队成员——每个人负责一块，最后汇总成果。

### 第三步：代码实践（动手实验）

**使用 Subagents**：
```text
> 使用 subagents 并行处理：
> 1. 分析前端代码质量
> 2. 分析后端 API 设计
> 3. 检查数据库查询性能
> 最后汇总报告
```

**适用场景**：
- 大型项目分析
- 并行测试执行
- 多模块独立任务

### 第四步：知识关联

- Subagents 隔离上下文，避免污染主会话
- 可以并行执行，提高效率
- 适合探索性任务

---

## 知识点 6：跨平台工作流

### 第一步：概念解释（简单语言）

Claude Code 会话不绑定单一平台——你可以在终端开始，转到手机继续，最后在 Desktop 完成。

### 第二步：类比理解（生活例子）

就像接力赛——终端跑第一棒，手机跑第二棒，Desktop 冲刺。

### 第三步：代码实践（动手实验）

**转移会话**：

| 命令 | 说明 |
|------|------|
| `/teleport` | 从 Web/iOS 拉取会话到本地 |
| `/desktop` | 从终端转移到 Desktop 应用 |
| `/remote` | 启用远程控制 |

**典型工作流**：
```
1. 早上在电脑终端启动 Claude，开始分析代码
2. 出门开会，打开手机继续监控进度
3. 回到办公室，在 Desktop 上查看差异、完成合并
```

### 第四步：知识关联

- 会话状态保存在云端
- CLAUDE.md、MCP 配置自动同步
- 支持设备间无缝切换

---

## 总结检查清单

完成本章后，你应该能够：

- [ ] 创建调度任务
- [ ] 使用远程控制
- [ ] 配置 Channels
- [ ] 了解 Agent SDK
- [ ] 使用 Subagents
- [ ] 跨平台工作流

---

## 下一步

[下一章：最佳实践 →](06-best-practices.md)

学习如何写好 Prompt、配置 CLAUDE.md、提升效率。