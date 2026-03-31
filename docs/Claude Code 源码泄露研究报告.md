# Claude Code 源码泄露研究报告

> 研究时间：2026-03-31
> 来源：npm registry sourcemap 泄露事件

---

## 一、事件概述

### 1.1 泄露发生

**时间**：2026年3月31日

**发现者**：安全研究员 Chaofan Shou ([@shoucccc](https://x.com/shoucccc))

**泄露原因**：Anthropic 在发布 Claude Code npm 包时，意外包含了 **sourcemap（源码映射）文件**，导致完整的 TypeScript 源码暴露。

**影响规模**：
- ~1,900 个 TypeScript 文件
- 512,000+ 行代码
- ~40 个内置工具
- ~50 个斜杠命令

### 1.2 泄露原理

**什么是 Sourcemap？**

Sourcemap（源码映射）是一种调试工具，用于将打包/压缩后的代码映射回原始源码。开发时很有用，但如果在生产发布时包含，就相当于把整个源码公开。

**发生过程**：
1. Anthropic 工程师构建 Claude Code npm 包
2. 打包配置未正确排除 `.map` 文件
3. 包发布到 npm registry 时携带了完整 sourcemap
4. 研究员下载包后，通过 sourcemap 还原出原始 TypeScript 源码

**教训**：检查构建流水线，确保 `.npmignore` 或 `package.json` 的 `files` 字段正确排除 sourcemap 文件。

---

## 二、核心架构分析

### 2.1 项目整体结构

```
claude-code-main/
└── src/
    ├── assistant/              # 助手模式（Kairos）
    ├── bridge/                 # 远程控制桥接
    ├── buddy/                  # 伴侣角色系统（UI精灵）
    ├── cli/                    # 命令行界面
    ├── commands/               # 70+ 斜杠命令
    ├── components/             # React UI 组件
    ├── constants/              # 常量配置
    ├── entrypoints/            # 应用入口
    ├── hooks/                  # React Hooks
    ├── ink/                    # Ink 终端渲染框架
    ├── services/               # 核心服务层
    ├── skills/                 # 技能系统
    ├── state/                  # 状态管理
    ├── tools/                  # 25+ 工具实现
    └── utils/                  # 工具函数
```

### 2.2 技术栈选择

| 技术 | 用途 | 说明 |
|------|------|------|
| **Bun** | 运行时 | 不是 Node.js，使用 Bun 运行 JS/TS |
| **React 19** | UI 框架 | 组件化架构 |
| **Ink** | 终端渲染 | React 风格的终端 UI |
| **Zod v4** | Schema 验证 | 所有输入/输出都有类型校验 |
| **@anthropic-ai/sdk** | API 通信 | Anthropic 官方 SDK |
| **@modelcontextprotocol/sdk** | MCP 协议 | 工具扩展协议 |

### 2.3 五大核心子系统

#### 1️⃣ 工具系统（Tool System）~40 个工具

每个能力（读文件、执行命令、Web 搜索等）都是独立、权限可控的工具。

**核心工具列表**：

| 工具 | 功能 |
|------|------|
| `BashTool` | 执行 Shell 命令，支持后台任务、沙箱模式 |
| `FileReadTool` | 读取文件（支持图片、PDF、Jupyter） |
| `FileEditTool` | 编辑文件，精确字符串替换 |
| `FileWriteTool` | 创建或覆盖文件 |
| `GlobTool` | 文件模式匹配搜索 |
| `GrepTool` | 正则内容搜索 |
| `AgentTool` | 多代理系统，支持子代理 |
| `WebFetchTool` | 获取网页内容 |
| `WebSearchTool` | Web 搜索 |
| `LSPTool` | LSP 语言服务集成 |
| `MCPTool` | MCP 工具调用桥接 |
| `SkillTool` | 调用预定义技能 |

#### 2️⃣ 查询引擎（Query Engine）46K 行

这是系统的"大脑"，负责：
- LLM API 调用
- 流式响应处理
- 缓存管理
- 多轮对话编排

#### 3️⃣ 多代理编排（Multi-Agent Orchestration）

Claude Code 可以启动"子代理"（称为 swarms），每个代理有独立的上下文和权限，用于并行处理复杂任务。

#### 4️⃣ IDE 桥接系统（IDE Bridge）

双向通信层，连接 VS Code/JetBrains 扩展与 CLI，通过 JWT 认证通道实现"编辑器中的 Claude"体验。

#### 5️⃣ 持久化记忆系统（Persistent Memory）

基于文件的记忆目录，存储：
- 用户偏好
- 项目上下文
- 跨会话记忆

---

## 三、隐藏功能揭秘

### 3.1 BUDDY（伴侣角色系统）

一个 **Tamagotchi（电子宠物）风格** 的 UI 精灵系统！
- 类似桌面宠物
- 与用户互动
- 增加趣味性

### 3.2 KAIROS（主动式助手）

"始终在线"的主动式 AI 助手模式：
- 不需要用户显式调用
- 主动监控和提醒
- 类似"隐形助手"

### 3.3 ULTRAPLAN（远程编排模式）

30 分钟远程编排模式：
- 用于复杂规划任务
- 远程会话管理

### 3.4 Undercover Mode（内部模式）

Anthropic 内部使用的特殊模式：
- 额外的测试功能
- 内部模型变体

### 3.5 模型代号

泄露代码中发现内部模型代号：
- **Tengu**（天狗）
- **Fennec**（耳廓狐）

### 3.6 cch 认证机制

Claude Code 使用自定义的 Bun 运行时：
- Zig 编译的 token 生成
- 特殊的 attestation（认证）机制

---

## 四、安全与隐私相关发现

### 4.1 情感检测

代码中发现使用 **正则表达式** 检测用户情感，而不是用 AI 模型分析。

### 4.2 反蒸馏防御

API 请求中包含反蒸馏（anti-distillation）防御机制，防止模型输出被用于训练竞争对手的模型。

### 4.3 挫败遥测

收集用户"挫败"情况的遥测数据，用于产品优化。

### 4.4 权限系统

每个工具都有独立的权限检查：
```typescript
type PermissionResult = 
  | { behavior: 'allow' }
  | { behavior: 'deny'; message: string }
  | { behavior: 'ask'; message: string; options: PermissionOption[] }
```

---

## 五、工程启示

### 5.1 构建安全教训

**必须检查 npm 发布内容**：
```bash
npm pack --dry-run  # 查看即将发布的文件列表
```

**确保 `.npmignore` 正确配置**：
```
# .npmignore
*.map
*.ts
src/
test/
```

### 5.2 架构学习价值

即使不看泄露代码，从公开信息也能学到：
1. **工具化设计**：每个能力都是独立、可组合的工具
2. **权限控制**：细粒度的执行权限检查
3. **多代理编排**：子代理处理并行任务
4. **持久化记忆**：跨会话保持上下文
5. **React 终端 UI**：Ink 实现组件化 CLI

---

## 六、相关资源

### GitHub 仓库

| 仓库 | 说明 |
|------|------|
| [instructkr/claude-code](https://github.com/instructkr/claude-code) | 源码镜像（原始泄露） |
| [CnOxx1/claude-code](https://github.com/CnOxx1/claude-code) | 中文技术分析文档 |
| [nblintao/awesome-claude-code-postleak-insights](https://github.com/nblintao/awesome-claude-code-postleak-insights) | 精选分析文章列表 |

### 社区讨论

- [Hacker News 讨论](https://news.ycombinator.com/item?id=47584540)
- [r/LocalLLaMA 讨论](https://www.reddit.com/r/LocalLLaMA/comments/1s8ijfb/)
- [r/ClaudeAI 讨论](https://www.reddit.com/r/ClaudeAI/comments/1s8ifm6/)

### 分析文章

- [Claude Code's Entire Source Code Was Just Leaked via npm Source Maps](https://dev.to/gabrielanhaia/claude-codes-entire-source-code-was-just-leaked-via-npm-source-maps-heres-whats-inside-cjo) — 架构深度分析
- [TheHuman2AI 博客](https://thehuman2ai.com/blog/claude-code-source-leak) — 时间线和观点

---

## 七、总结

这次泄露事件暴露了 Anthropic Claude Code 的完整工程架构，揭示了：
1. 一个生产级 AI 编程助手的技术深度
2. sourcemap 发布配置的安全风险
3. AI 工具领域的技术标杆水平

对于开发者而言，这是一次难得的学习机会——可以研究顶级 AI 工具的架构设计，同时警醒构建流程的安全配置。

> **免责声明**：本报告仅用于研究和教育目的，所有源码为 Anthropic 知识财产，不鼓励未经授权分发。