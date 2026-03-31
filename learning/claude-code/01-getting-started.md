# Claude Code 快速开始

> ⏱️ 30 分钟 | 📍 第一步

[← 返回导航](README.md) | [下一章：核心概念 →](02-core-concepts.md)

---

## 知识点 1：安装 Claude Code

### 第一步：概念解释（简单语言）

Claude Code 是一个可以在终端里运行的 AI 编程助手。你只需要安装一次，然后在任何项目目录里运行 `claude` 命令就能启动它。

### 第二步：类比理解（生活例子）

想象 Claude Code 就像一个智能助手住进了你的电脑。安装过程就像是给这个助手分配一个办公桌——一旦安装完成，它就随时待命，你喊一声"claude"它就开始工作。

### 第三步：代码实践（动手实验）

**macOS / Linux / WSL：**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell：**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**验证安装：**
```bash
claude --version
```

### 第四步：知识关联

安装完成后：
- 需要配置认证 → 见 [知识点 2：登录认证](#知识点-2登录认证)
- 可以选择不同平台 → Terminal、VS Code、Desktop、Web、JetBrains

---

## 知识点 2：登录认证

### 第一步：概念解释（简单语言）

Claude Code 需要知道你是谁才能为你工作。登录方式有两种：通过浏览器登录（推荐），或者使用 API Key。

### 第二步：类比理解（生活例子）

就像登录任何网站一样——你可以用账号密码登录，也可以用专门的通行证（API Key）。浏览器登录更方便，API Key 更适合自动化场景。

### 第三步：代码实践（动手实验）

**方式一：OAuth 登录（推荐）**
```bash
claude
# 第一次运行会自动引导你通过浏览器登录
```

**方式二：API Key**
```bash
export ANTHROPIC_API_KEY=sk-ant-xxxxx
claude
```

**检查登录状态：**
```bash
claude /status
```

### 第四步：知识关联

- OAuth 登录支持 Pro/Max/Team/Enterprise 订阅
- API Key 来自 [Anthropic Console](https://console.anthropic.com/)
- Team/Enterprise 用户可能需要管理员启用某些功能

---

## 知识点 3：第一个任务

### 第一步：概念解释（简单语言）

安装并登录后，你可以让 Claude 帮你做任何编程任务——生成代码、解释代码、运行命令、修改文件。

### 第二步：类比理解（生活例子）

就像和一个程序员同事对话——你描述需求，他理解后开始工作，边做边向你确认重要决定。

### 第三步：代码实践（动手实验）

**启动 Claude Code：**
```bash
cd your-project
claude
```

**第一个任务示例：**
```text
> 给我这个项目的整体架构概览
```

```text
> 找出 src/auth 目录下的认证流程是如何工作的
```

```text
> 在 src/utils/date.ts 中添加一个 formatDate 函数
```

### 第四步：知识关联

- Claude 会先读取你的项目文件
- 重要操作会请求你的批准
- 可以用 `@filename` 快速引用文件

---

## 知识点 4：多平台支持

### 第一步：概念解释（简单语言）

Claude Code 不只是终端工具——你可以在 VS Code、Desktop 应用、浏览器、JetBrains IDE 中使用它。同一个引擎，不同的入口。

### 第二步：类比理解（生活例子）

就像同一个助手可以从不同的房间找到你——终端是命令室，VS Code 是设计室，Desktop 是会议室，Web 是远程办公室。

### 第三步：代码实践（动手实验）

| 平台 | 安装方式 |
|------|----------|
| **Terminal** | `curl -fsSL https://claude.ai/install.sh | bash` |
| **VS Code** | 安装扩展 [anthropic.claude-code](vscode:extension/anthropic.claude-code) |
| **Desktop** | 下载 [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect) 或 [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect) |
| **Web** | 访问 [claude.ai/code](https://claude.ai/code) |
| **JetBrains** | 安装插件 [Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) |

### 第四步：知识关联

- 所有平台共享同一个引擎
- CLAUDE.md、设置、MCP 配置在所有平台生效
- 选择平台取决于你的工作场景

---

## 知识点 5：斜杠命令速查

### 第一步：概念解释（简单语言）

斜杠命令是 Claude Code 的快捷指令——输入 `/command` 就能执行特定功能。

### 第二步：类比理解（生活例子）

就像手机上的快捷手势——滑一下就能拍照，点两下就能截图。斜杠命令让你快速执行常见操作。

### 第三步：代码实践（动手实验）

**最常用的命令：**

| 命令 | 说明 |
|------|------|
| `/clear` | 清除对话历史，开始新任务 |
| `/compact` | 压缩上下文，保留关键信息 |
| `/status` | 查看状态信息 |
| `/init` | 初始化项目，生成 CLAUDE.md |
| `/help` | 查看帮助 |

**示例：**
```text
> /clear     # 开始新任务
> /status    # 检查状态
> /init      # 初始化项目配置
```

### 第四步：知识关联

- 斜杠命令在所有平台都可用
- 可以创建自定义 Skills 来扩展命令
- 见 [04-skills-hooks.md](04-skills-hooks.md) 学习创建自定义命令

---

## 总结检查清单

完成本章后，你应该能够：

- [x] 安装 Claude Code
- [x] 使用 OAuth 登录
- [x] 运行第一个任务
- [x] 知道有哪些平台可用
- [x] 使用基本斜杠命令

---

## 下一步

[下一章：核心概念 →](02-core-concepts.md)

学习 Claude Code 的核心理念：代理型编码、权限模式、会话管理。