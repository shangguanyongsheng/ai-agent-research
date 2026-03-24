# Claude Code 使用手册

> 一份面向开发者的完整指南，帮助你充分发挥 Claude Code 的强大能力

---

## 目录

1. [Claude Code 简介](#1-claude-code-简介)
2. [安装配置](#2-安装配置)
3. [核心功能](#3-核心功能)
4. [使用技巧](#4-使用技巧)
5. [最佳实践](#5-最佳实践)
6. [常见问题](#6-常见问题)

---

## 1. Claude Code 简介

### 1.1 是什么

**Claude Code** 是 Anthropic 推出的官方命令行工具，让 Claude 直接在你的终端中工作。与传统的 AI 聊天工具不同，Claude Code 是一个**代理型编码环境（Agentic Coding Environment）**——它不只是回答问题，还能主动读取文件、执行命令、修改代码，自主地完成复杂的开发任务。

简单来说：
- 不是你写代码让 Claude Review
- 而是你描述需求，Claude 自主探索、规划、实现

### 1.2 核心功能

| 功能 | 描述 |
|------|------|
| **代码生成** | 根据描述自动生成代码，支持多种编程语言 |
| **代码解释** | 分析和理解现有代码库，解释复杂逻辑 |
| **文件操作** | 读取、编辑、创建文件，支持批量操作 |
| **命令执行** | 在终端中执行 shell 命令，如构建、测试、Git 操作 |
| **项目理解** | 自动探索代码库结构，理解架构和依赖关系 |
| **PR 创建** | 自动创建 Git 提交和 Pull Request |
| **扩展能力** | 支持 Skills、Hooks、MCP、Subagents 等扩展机制 |

### 1.3 与 Cursor / Copilot 的区别

| 特性 | Claude Code | Cursor | GitHub Copilot |
|------|-------------|--------|----------------|
| **交互方式** | 终端命令行 | IDE 集成 | IDE 插件 |
| **工作模式** | 代理型（自主执行） | 辅助型（建议+确认） | 补全型（实时建议） |
| **文件操作** | ✅ 自主读写 | ✅ 需确认 | ❌ 仅补全 |
| **命令执行** | ✅ 执行 Shell | ❌ | ❌ |
| **项目探索** | ✅ 自动分析 | ⚠️ 有限 | ❌ |
| **多文件编辑** | ✅ 支持 | ✅ 支持 | ⚠️ 有限 |
| **扩展性** | MCP/Skills/Hooks | MCP | 有限 |
| **上下文理解** | 整个代码库 | 打开文件 | 当前文件 |
| **定价** | Claude 订阅/API | 订阅制 | 订阅制 |

**核心差异**：Claude Code 更像一个"AI 工程师"，能独立完成从需求理解到代码提交的完整流程；而 Cursor/Copilot 更像"AI 助手"，需要你主导开发过程。

---

## 2. 安装配置

### 2.1 安装方式

#### 方式一：官方安装脚本（推荐）

**macOS / Linux：**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell)：**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows (CMD)：**
```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

#### 方式二：包管理器

**macOS (Homebrew)：**
```bash
brew install --cask claude-code
```

**Windows (WinGet)：**
```powershell
winget install Anthropic.ClaudeCode
```

#### 方式三：npm（不推荐）

```bash
npm install -g @anthropic-ai/claude-code
```

> ⚠️ npm 安装版本可能不是最新，建议优先使用官方脚本或包管理器。

### 2.2 API Key 配置

Claude Code 支持多种认证方式：

#### 方式一：OAuth 登录（推荐）

首次运行 `claude` 时，会自动引导你通过浏览器完成 OAuth 登录。支持：
- Claude Pro/Max 订阅用户
- Anthropic Console API 用户

#### 方式二：API Key 环境变量

```bash
# 临时设置
export ANTHROPIC_API_KEY=sk-ant-xxxxx

# 永久设置（添加到 shell 配置文件）
echo 'export ANTHROPIC_API_KEY=sk-ant-xxxxx' >> ~/.zshrc  # macOS
echo 'export ANTHROPIC_API_KEY=sk-ant-xxxxx' >> ~/.bashrc # Linux
```

#### 方式三：第三方 API 提供商

Claude Code 支持通过 Amazon Bedrock 和 Google Vertex AI 调用 Claude 模型：

```bash
# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id
```

### 2.3 代理配置

如果你在公司网络或需要代理访问：

```bash
# 设置代理
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 然后运行 Claude Code
claude
```

#### 针对企业证书问题

如果遇到 TLS/SSL 错误，可能需要配置企业 CA 证书：

```bash
export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
```

### 2.4 验证安装

```bash
# 检查版本
claude --version

# 检查状态
claude /status
```

---

## 3. 核心功能

### 3.1 代码生成

#### 基本用法

```bash
claude
> 实现一个用户登录功能，包含表单验证和错误提示
```

#### 从零创建新项目

```text
> 创建一个 React + TypeScript 项目，使用 Vite 构建，包含以下功能：
> - 用户认证（登录/注册）
> - Dashboard 页面
> - 响应式设计
> 配置 ESLint 和 Prettier
```

#### 按指定模式生成

```text
> 参考 @src/components/Button.tsx 的风格，创建一个 Modal 组件
> 要求：支持自定义标题、内容、关闭按钮，使用相同的样式系统
```

### 3.2 代码解释

#### 理解代码库

```text
> 给我这个项目的整体架构概览
```

```text
> 解释 src/auth 目录下的认证流程是如何工作的
```

#### 追踪代码执行路径

```text
> 从用户点击登录按钮开始，追踪整个登录流程，列出涉及的所有文件和函数
```

#### 理解特定代码

```text
> 解释 @src/utils/parser.ts 中第 45-60 行的复杂正则表达式
```

### 3.3 文件操作

#### 读取文件

```text
> 读取 @package.json 并列出所有依赖项
```

#### 编辑文件

```text
> 在 @src/api/user.ts 中添加一个新的 updateUserProfile 方法
```

#### 批量操作

```text
> 将所有 .js 文件中的 var 声明改为 const/let
> 先预览会修改哪些文件，然后再执行
```

#### 引用文件

使用 `@` 符号快速引用文件：

```text
> 对比 @src/api/v1/user.ts 和 @src/api/v2/user.ts 的差异
```

### 3.4 命令执行

#### 运行构建和测试

```text
> 运行测试套件，修复任何失败的测试
```

```text
> 执行 npm run build 并确保没有错误
```

#### Git 操作

```text
> 查看当前的 Git 状态
```

```text
> 提交当前的更改，使用描述性的 commit message
```

```text
> 创建一个 PR，标题是 "feat: 添加用户认证功能"
```

#### 调试命令

```text
> 运行 npm test 并查看输出，找出失败的原因
```

---

## 4. 使用技巧

### 4.1 如何写好的 Prompt

#### ❌ 模糊的 Prompt

```text
> 修复这个 bug
```

#### ✅ 具体的 Prompt

```text
> 用户报告登录失败后没有显示错误提示。检查 src/auth/login.tsx，
> 找到错误处理逻辑，添加用户友好的错误消息显示。
> 确保错误消息在 UI 上可见至少 3 秒。
```

#### Prompt 结构建议

1. **明确目标**：你想达到什么效果
2. **提供上下文**：相关文件、现有代码风格
3. **约束条件**：不能做什么、必须遵循什么
4. **验证标准**：如何确认任务完成

```text
> 目标：为 API 添加速率限制功能
> 
> 上下文：
> - 参考 @src/middleware/auth.ts 的中间件模式
> - 使用 Redis 存储请求计数
> 
> 约束：
> - 不引入新的依赖库
> - 每个用户每分钟最多 60 次请求
> 
> 验证：
> - 写一个测试用例模拟超限请求
> - 运行测试确保功能正常
```

### 4.2 如何引导 Claude 理解项目

#### 使用 `/init` 初始化

首次进入项目，运行：

```text
> /init
```

Claude 会自动分析项目结构，生成一个 `CLAUDE.md` 文件，包含：
- 构建命令
- 测试命令
- 代码风格约定
- 项目架构说明

#### 手动提供上下文

```text
> 这是一个使用 Next.js 14 的电商项目。
> - 使用 App Router（不是 Pages Router）
> - 数据库用 Prisma + PostgreSQL
> - 样式用 Tailwind CSS
> - 请先阅读 README.md 和 package.json 了解更多信息
```

#### 分阶段探索

对于大型项目，建议分阶段让 Claude 理解：

```text
> 第一阶段：只读取 src/types 目录，理解数据模型
> 
> 第二阶段：读取 src/api 目录，理解 API 结构
> 
> 第三阶段：基于前面的理解，帮我实现一个新的 API 端点
```

### 4.3 多文件协作技巧

#### 使用 Plan Mode

对于涉及多个文件的复杂任务，使用 Plan Mode：

```bash
# 启动时指定 Plan Mode
claude --permission-mode plan
```

或者在会话中按 `Shift+Tab` 切换到 Plan Mode。

Plan Mode 下 Claude 只读取和分析，不修改文件，适合：
- 理解复杂架构
- 规划重构方案
- 探索代码库

#### 使用 Subagents

让子代理处理独立任务：

```text
> 使用 subagent 来分析我们的认证系统是否安全，
> 然后返回一份报告
```

#### 使用 Worktrees 隔离并行任务

```bash
# 创建独立的工作树
claude --worktree feature-auth

# 另一个终端中
claude --worktree bugfix-123
```

两个 Claude 实例可以并行工作而不冲突。

---

## 5. 最佳实践

### 5.1 项目结构建议

#### 推荐的项目结构

```
project/
├── .claude/
│   ├── CLAUDE.md          # 项目级 Claude 配置
│   ├── settings.json      # 项目设置
│   ├── rules/             # 规则文件
│   │   ├── code-style.md
│   │   └── testing.md
│   └── skills/            # 自定义技能
│       └── my-workflow/
│           └── SKILL.md
├── CLAUDE.md              # 根目录 CLAUDE.md（也可以）
├── .mcp.json              # MCP 服务器配置
├── src/
├── tests/
└── ...
```

### 5.2 CLAUDE.md 配置

#### 基本结构

```markdown
# 项目名称

## 构建命令
- 开发：`npm run dev`
- 构建：`npm run build`
- 测试：`npm test`（单个测试：`npm test -- path/to/test.ts`）

## 代码风格
- 使用 ES Modules（import/export），不用 CommonJS
- 使用 2 空格缩进
- 组件使用 PascalCase，函数使用 camelCase
- 优先使用 TypeScript 类型而非接口

## 架构约定
- API 路由在 `src/app/api/` 目录
- 组件在 `src/components/` 目录
- 工具函数在 `src/lib/` 目录

## 测试约定
- 测试文件与源文件同级，命名为 `*.test.ts`
- 使用 Vitest 测试框架
- 每个公开函数至少有一个测试

## 注意事项
- 不要修改 `src/generated/` 目录
- 环境变量在 `.env.local` 中配置
```

#### 大小控制

- **建议**：控制在 200 行以内
- 过长的 CLAUDE.md 会消耗过多上下文，降低 Claude 的遵循度
- 详细内容可拆分到 `.claude/rules/` 目录

#### 导入其他文件

```markdown
# 项目配置

## 参考
- 项目概述：@README.md
- 依赖信息：@package.json
- 详细规范：@docs/conventions.md
```

### 5.3 与 Git 协作

#### 自动提交

```text
> 提交当前更改，commit message 要描述清楚修改了什么和为什么
```

#### 自动创建 PR

```text
> 为当前的更改创建一个 PR，包含：
> - 描述功能/修复的标题
> - 详细说明改动的描述
> - 测试步骤
```

#### 从 PR 恢复会话

```bash
claude --from-pr 123
```

### 5.4 使用 Hooks 自动化

Hooks 可以在特定事件时自动执行脚本：

#### 配置示例

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

### 5.5 使用 MCP 扩展能力

Model Context Protocol (MCP) 让 Claude 能连接外部工具：

```json
// .mcp.json
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
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

---

## 6. 常见问题

### 6.1 常见错误

#### `command not found: claude`

**原因**：安装目录不在 PATH 中。

**解决**：

```bash
# macOS/Linux (Zsh)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# macOS/Linux (Bash)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Windows (PowerShell)
$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
```

#### `syntax error near unexpected token '<'`

**原因**：安装脚本返回 HTML 而非 Shell 脚本，可能是网络问题或地区限制。

**解决**：
1. 检查 Claude Code 是否在你所在地区可用
2. 使用包管理器安装：
   ```bash
   brew install --cask claude-code  # macOS
   winget install Anthropic.ClaudeCode  # Windows
   ```

#### `OAuth error: Invalid code`

**原因**：登录码过期或复制不完整。

**解决**：
1. 按 `c` 复制完整 URL
2. 手动粘贴到浏览器完成登录
3. 快速完成验证流程

#### 403 Forbidden 错误

**原因**：
- 订阅已过期
- API 账户权限不足
- 代理配置问题

**解决**：
1. 检查订阅状态：https://claude.ai/settings
2. 确认账户有 "Claude Code" 或 "Developer" 角色
3. 检查代理配置

### 6.2 性能优化

#### 上下文管理

```text
> /clear    # 清除对话历史，开始新任务
> /compact  # 压缩上下文，保留关键信息
```

#### 使用 Subagents

对于探索性任务，使用子代理避免污染主会话上下文：

```text
> 使用 subagent 来调查数据库连接池的实现细节
```

#### 限制文件读取

```text
> 只在 src/api/ 目录下搜索，不要读取整个项目
```

### 6.3 安全注意事项

#### 权限控制

- 默认情况下，Claude 会请求修改操作的批准
- 使用 `/permissions` 管理允许列表
- 敏感操作使用 sandbox 模式

#### 避免敏感信息泄露

- 不要在代码中硬编码密钥
- 使用环境变量存储敏感配置
- 定期检查 `.claude/` 目录内容

#### Sandbox 模式

启用沙箱隔离：

```bash
claude /sandbox on
```

沙箱模式下，Claude 的操作被限制在隔离环境中。

### 6.4 其他有用命令

```bash
# 检查 Claude Code 状态
claude /status

# 运行诊断
claude /doctor

# 查看配置的 hooks
claude /hooks

# 管理权限
claude /permissions

# 查看内存
claude /memory

# 提供反馈
claude /feedback
```

---

## 附录：常用命令速查

| 命令 | 说明 |
|------|------|
| `claude` | 启动交互式会话 |
| `claude -p "prompt"` | 非交互模式 |
| `claude --continue` | 继续最近会话 |
| `claude --resume` | 选择历史会话 |
| `claude --worktree name` | 在独立工作树中启动 |
| `claude /help` | 查看帮助 |
| `claude /status` | 查看状态 |
| `claude /clear` | 清除上下文 |
| `claude /compact` | 压缩上下文 |
| `claude /init` | 初始化项目配置 |

---

## 7. 高级使用技巧

### 7.1 斜杠命令详解

#### 内置命令分类

**会话管理**：
| 命令 | 说明 |
|------|------|
| `/clear` | 清除对话历史（别名：`/reset`, `/new`） |
| `/compact [instructions]` | 压缩上下文，可选指定重点 |
| `/resume [session]` | 恢复会话（别名：`/continue`） |
| `/rename [name]` | 重命名当前会话 |
| `/branch [name]` | 在当前点创建会话分支（别名：`/fork`） |

**项目管理**：
| 命令 | 说明 |
|------|------|
| `/init` | 初始化项目，生成 CLAUDE.md |
| `/add-dir <path>` | 添加额外工作目录 |
| `/context` | 可视化上下文使用情况 |
| `/diff` | 查看未提交的更改 |

**调试诊断**：
| 命令 | 说明 |
|------|------|
| `/doctor` | 诊断安装和配置问题 |
| `/debug [description]` | 调试当前会话 |
| `/status` | 查看状态信息 |
| `/cost` | 查看 token 使用统计 |

**配置管理**：
| 命令 | 说明 |
|------|------|
| `/config` 或 `/settings` | 打开设置界面 |
| `/model [model]` | 切换模型 |
| `/permissions` | 管理权限设置 |
| `/hooks` | 查看 hooks 配置 |

### 7.2 Skills（技能）高级用法

#### ⚠️ 常见误区：为什么 `/md` 不触发？

**问题**：输入 `/md index.md` 没有触发任何技能。

**原因分析**：
1. **Skills 需要正确创建**：一个有效的 Skill 必须包含 `SKILL.md` 文件
2. **位置要正确**：必须放在正确的目录下
3. **name 字段决定命令名**：`name: md` 才会生成 `/md` 命令

**正确的 Skill 创建步骤**：

```bash
# 1. 创建技能目录
mkdir -p ~/.claude/skills/md/SKILL.md

# 或者项目级技能
mkdir -p .claude/skills/md/SKILL.md
```

```markdown
# ~/.claude/skills/md/SKILL.md
---
name: md
description: 创建 Markdown 文档
---

创建 Markdown 文档：$ARGUMENTS

步骤：
1. 分析文档需求
2. 创建文件
3. 添加标准格式（标题、目录、章节）
```

**验证 Skill 是否生效**：
```bash
# 启动 Claude Code 后输入
/skills

# 应该能看到你的 skill 列表
```

#### Skills 目录位置

| 位置 | 路径 | 适用范围 |
|------|------|----------|
| 个人技能 | `~/.claude/skills/<name>/SKILL.md` | 所有项目 |
| 项目技能 | `.claude/skills/<name>/SKILL.md` | 当前项目 |
| 插件技能 | `<plugin>/skills/<name>/SKILL.md` | 插件启用时 |

#### Skills 触发方式

1. **手动触发**：输入 `/skill-name [args]`
2. **自动触发**：Claude 根据 `description` 判断何时使用

**控制触发行为**：
```markdown
---
name: deploy
description: 部署到生产环境
disable-model-invocation: true  # 禁止 Claude 自动触发
---
```

#### 内置 Skills（Bundled Skills）

| Skill | 用途 |
|-------|------|
| `/batch <instruction>` | 并行批量处理大规模变更 |
| `/debug [description]` | 调试当前会话 |
| `/loop [interval] <prompt>` | 周期性执行提示 |
| `/simplify [focus]` | 代码质量审查和优化 |

### 7.3 CLAUDE.md 高级配置

#### 文件位置优先级

```
1. /Library/Application Support/ClaudeCode/CLAUDE.md  (macOS 管理策略)
   /etc/claude-code/CLAUDE.md                         (Linux 管理策略)
   C:\Program Files\ClaudeCode\CLAUDE.md              (Windows 管理策略)

2. ./CLAUDE.md 或 ./.claude/CLAUDE.md                 (项目级)

3. ~/.claude/CLAUDE.md                                (用户级)
```

**优先级**：管理策略 > 项目级 > 用户级

#### ⚠️ CLAUDE.md 常见问题

**问题 1：Claude 不遵循我的 CLAUDE.md**

**解决方案**：
1. **检查文件大小**：保持在 200 行以内，过长会降低遵循度
2. **使用具体指令**：
   ```markdown
   # ❌ 模糊
   格式化代码
   
   # ✅ 具体
   使用 2 空格缩进，语句末尾不加分号
   ```
3. **检查冲突**：确保没有相互矛盾的规则
4. **验证加载**：运行 `/init` 检查是否有改进建议

**问题 2：`/compact` 后指令丢失**

**原因**：`/compact` 会压缩上下文，可能丢失 CLAUDE.md 中的详细说明。

**解决方案**：
- 将关键指令放在 CLAUDE.md 开头
- 使用 `.claude/rules/` 目录拆分规则
- 重要规则使用简洁的陈述句

#### 使用 Rules 目录组织规则

```
.claude/
├── CLAUDE.md              # 主配置
└── rules/
    ├── code-style.md      # 代码风格
    ├── testing.md         # 测试规范
    └── api-design.md      # API 设计
```

**按文件类型限定规则**：
```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/**/*.test.ts"
---

# API 开发规则
- 所有端点必须包含输入验证
- 使用标准错误响应格式
```

#### 导入外部文件

```markdown
# 项目概述
参见 @README.md

# 依赖信息
参见 @package.json

# Git 工作流
参见 @docs/git-instructions.md
```

### 7.4 Auto Memory（自动记忆）

**是什么**：Claude 自动记录你的偏好和修正。

**启用/禁用**：
```bash
/memory auto on   # 启用
/memory auto off  # 禁用
```

**查看记忆内容**：
```bash
/memory
```

**存储位置**：
```
~/.claude/memory/<project-hash>/AUTO_MEMORY.md
```

---

## 8. 常见问题排查

### 8.1 Skills/命令不触发

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| `/skill` 无响应 | Skill 未正确创建 | 检查 `SKILL.md` 是否存在 |
| 命令不在列表中 | name 字段格式错误 | 使用小写字母、数字、连字符 |
| Claude 不自动使用 | description 缺失或模糊 | 添加清晰的 description |
| Skill 触发太频繁 | description 太宽泛 | 使 description 更具体 |

**诊断步骤**：
```bash
# 1. 检查 Skill 是否被发现
/skills

# 2. 检查文件结构
ls -la ~/.claude/skills/md/

# 3. 验证 SKILL.md 格式
head -20 ~/.claude/skills/md/SKILL.md
```

### 8.2 CLAUDE.md 不生效

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| 规则被忽略 | 文件过长 | 精简到 200 行以内 |
| 部分规则无效 | 规则冲突 | 检查并移除矛盾规则 |
| 新规则不生效 | 缓存问题 | 重启 Claude Code |
| 特定目录规则无效 | paths 配置错误 | 检查 glob 模式语法 |

### 8.3 性能问题

**上下文过大**：
```bash
# 查看上下文使用
/context

# 压缩上下文
/compact

# 或清除重新开始
/clear
```

**搜索缓慢（WSL）**：
```bash
# 在 WSL 中添加项目到 Windows 索引
# 或使用 /plan 模式减少搜索
```

### 8.4 认证问题

| 错误 | 解决方案 |
|------|----------|
| `OAuth error: Invalid code` | 快速完成验证，或按 `c` 复制完整 URL |
| `403 Forbidden` | 检查订阅状态，确认有 Claude Code 权限 |
| `Not logged in` | 运行 `/login` 重新认证 |
| WSL OAuth 失败 | 使用 `claude auth login --console` |

### 8.5 安装问题速查表

| 错误信息 | 解决方案 |
|----------|----------|
| `command not found: claude` | [将 `~/.local/bin` 添加到 PATH](#61-常见错误) |
| `syntax error near unexpected token '<'` | 使用包管理器安装 |
| `curl: (56) Failure writing output` | 先下载脚本，再执行 |
| `TLS/SSL error` | 更新 CA 证书或配置代理 |
| `Killed` on Linux | 添加 swap 空间 |

---

## 9. 最佳实践总结

### 9.1 写好 Prompt 的公式

```
[目标] + [上下文] + [约束] + [验证标准]
```

**示例**：
```text
目标：为 API 添加速率限制
上下文：参考 @src/middleware/auth.ts 的模式，使用 Redis
约束：不引入新依赖，每用户每分钟 60 次
验证：写测试用例模拟超限请求
```

### 9.2 CLAUDE.md 编写原则

1. **简洁**：200 行以内
2. **具体**：`npm test` 而非 "运行测试"
3. **结构化**：使用标题和列表
4. **无冲突**：定期审查删除过时规则

### 9.3 使用 Skills 还是 CLAUDE.md？

| 场景 | 推荐方式 |
|------|----------|
| 项目构建命令、代码风格 | CLAUDE.md |
| 特定任务工作流（部署、PR） | Skills |
| 按文件类型限定规则 | `.claude/rules/` |
| 团队共享指令 | 项目级 CLAUDE.md 或 Skills |
| 个人偏好 | `~/.claude/CLAUDE.md` |

### 9.4 效率提升技巧

1. **使用 Plan Mode**：复杂任务先规划再执行
   ```bash
   claude --permission-mode plan
   ```

2. **并行工作**：使用 git worktree
   ```bash
   claude --worktree feature-auth
   ```

3. **子代理隔离**：探索性任务用 subagent
   ```text
   > 使用 subagent 调查数据库连接池实现
   ```

4. **周期性任务**：使用 `/loop` 或 `--schedule`
   ```text
   /loop 5m 检查部署是否完成
   ```

---

## 附录 A：快捷键速查

| 快捷键 | 功能 |
|--------|------|
| `Shift+Tab` | 切换权限模式（Normal → Auto-Accept → Plan） |
| `Ctrl+C` | 取消当前操作 |
| `Ctrl+D` | 退出 Claude Code |
| `↑` / `↓` | 浏览历史命令 |
| `Tab` | 自动补全 |

---

## 附录 B：环境变量速查

| 变量 | 用途 |
|------|------|
| `ANTHROPIC_API_KEY` | API 密钥 |
| `CLAUDE_CODE_USE_BEDROCK` | 使用 Amazon Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | 使用 Google Vertex AI |
| `HTTP_PROXY` / `HTTPS_PROXY` | 代理配置 |
| `NODE_EXTRA_CA_CERTS` | 企业 CA 证书 |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | 加载额外目录的 CLAUDE.md |

---

## 总结

Claude Code 是一个强大的 AI 编程伙伴，掌握它的关键在于：

1. **清晰沟通**：提供具体、明确的指令
2. **善用上下文**：通过 CLAUDE.md 让 Claude 理解项目
3. **掌握 Skills**：创建正确的 SKILL.md 来扩展功能
4. **分步验证**：让 Claude 验证自己的工作
5. **管理上下文**：定期清理，使用 subagents 隔离任务
6. **持续优化**：根据实际使用调整 CLAUDE.md 和配置

祝你编码愉快！🚀