# OpenClaw 使用手册

> 让 AI Agent 成为你的个人助手，随时随地通过聊天应用与你交互

---

## 目录

1. [OpenClaw 简介](#1-openclaw-简介)
2. [安装部署](#2-安装部署)
3. [核心概念](#3-核心概念)
4. [常用命令](#4-常用命令)
5. [配置文件](#5-配置文件)
6. [使用技巧](#6-使用技巧)
7. [常见问题](#7-常见问题)

---

## 1. OpenClaw 简介

### 1.1 OpenClaw 是什么？

OpenClaw 是一个**自托管的 AI Agent 网关**，它将你常用的聊天应用（WhatsApp、Telegram、Discord、iMessage 等）连接到 AI 编程助手。你只需在自己的机器或服务器上运行一个 Gateway 进程，就能随时随地通过消息应用与 AI 交互。

**核心特点：**
- 🏠 **自托管**：运行在你自己的硬件上，完全掌控数据
- 📱 **多渠道**：一个 Gateway 同时支持 WhatsApp、Telegram、Discord、iMessage 等多个平台
- 🤖 **Agent 原生**：专为 AI Agent 设计，支持工具调用、会话管理、记忆和多 Agent 路由
- 🔓 **开源**：MIT 许可证，社区驱动

### 1.2 核心功能

| 功能类别 | 具体能力 |
|---------|---------|
| **渠道支持** | WhatsApp、Telegram、Discord、iMessage（内置）；Mattermost、Matrix、Teams 等（插件） |
| **AI 能力** | 嵌入式 Agent 运行时、工具流式处理、多 Agent 路由、会话隔离 |
| **模型支持** | 35+ 模型提供商（Anthropic、OpenAI、Google 等），支持自托管模型 |
| **媒体支持** | 图片、音频、视频、文档的收发，语音转录，文本转语音 |
| **自动化** | Cron 定时任务、Heartbeat 定期检查、Webhook 集成 |
| **移动端** | iOS/Android 节点配对、相机捕获、屏幕录制、语音唤醒 |

### 1.3 适用场景

**开发者场景：**
- 随时随地写代码、调试、审查 PR
- 自动化日常开发任务（定时检查 CI、自动生成报告）
- 远程控制服务器或开发环境

**个人助理场景：**
- 日程提醒、邮件摘要、日历检查
- 信息检索、文档整理、知识管理
- 自动化个人工作流

**团队协作场景：**
- 在群聊中提供技术支持
- 自动化团队报告和通知
- 多 Agent 分工协作

---

## 2. 安装部署

### 2.1 系统要求

**推荐配置：**
- **Node.js**：v24（推荐）或 v22.16+（最低要求）
- **内存**：512MB-1GB（个人使用），2GB+（生产环境）
- **CPU**：1 核心即可，多核更佳
- **磁盘**：约 500MB（不含日志和媒体）

**支持平台：**
- macOS（Intel/Apple Silicon）
- Linux（x64/ARM，支持树莓派）
- Windows（原生 + WSL2）
- Docker / Kubernetes

### 2.2 安装步骤

#### 方式一：一键安装脚本（推荐）

**macOS / Linux：**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows PowerShell：**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

#### 方式二：npm 安装

```bash
npm install -g openclaw@latest
```

#### 方式三：从源码安装（开发者）

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
```

### 2.3 初始化配置

安装完成后，运行引导式配置：

```bash
openclaw onboard --install-daemon
```

引导程序会：
1. 让你选择模型提供商（Anthropic、OpenAI、Google 等）
2. 设置 API 密钥
3. 配置 Gateway 服务
4. 自动安装系统服务

**验证安装：**
```bash
# 检查 Gateway 状态
openclaw gateway status

# 应该看到：Runtime: running，RPC probe: ok

# 打开控制面板
openclaw dashboard
```

---

## 3. 核心概念

### 3.1 Agent（智能体）

**定义：** Agent 是执行任务的核心实体，它理解你的指令并使用工具完成工作。

**关键特性：**
- **工作空间**：Agent 在指定目录下工作，所有文件操作都在此目录进行
- **记忆**：通过 `AGENTS.md`、`MEMORY.md` 等文件持久化记忆
- **工具调用**：可以读写文件、执行命令、浏览网页等
- **会话管理**：每个会话保持对话上下文

**Agent 配置文件：**
```
~/.openclaw/workspace/
├── AGENTS.md        # Agent 行为准则
├── SOUL.md          # 个性设定
├── TOOLS.md         # 工具使用指南
├── MEMORY.md        # 长期记忆
├── USER.md          # 用户信息
└── BOOTSTRAP.md     # 首次运行引导（完成后自动删除）
```

### 3.2 Skills（技能）

**定义：** Skills 是预定义的任务模板，让 Agent 具备特定领域的能力。

**技能类型：**
- **内置技能**：随 OpenClaw 一起安装的核心技能
- **托管技能**：存放在 `~/.openclaw/skills/`
- **工作空间技能**：存放在 `<workspace>/skills/`

**常用技能示例：**
- `github`：GitHub 操作（查看 PR、管理 Issue 等）
- `weather`：天气查询
- `agent-reach`：多平台搜索（Twitter、Reddit、YouTube 等）
- `healthcheck`：安全审计和健康检查

**安装技能：**
```bash
# 使用 ClawHub 安装技能
openclaw skills install <skill-name>
```

### 3.3 Tools（工具）

**定义：** Tools 是 Agent 可以调用的具体能力接口。

**核心工具：**
| 工具名称 | 功能 |
|---------|------|
| `read` | 读取文件内容 |
| `write` | 创建或覆写文件 |
| `edit` | 精确编辑文件（替换特定文本） |
| `exec` | 执行 shell 命令 |
| `browser` | 控制浏览器进行网页操作 |
| `web_search` | 网络搜索（Brave API） |
| `web_fetch` | 抓取网页内容 |
| `message` | 发送消息到各种渠道 |
| `tts` | 文本转语音 |
| `image` | 图像分析 |
| `pdf` | PDF 文档分析 |

**工具策略控制：**
可以通过配置控制哪些工具可用，以及执行权限。

### 3.4 Sessions（会话）

**定义：** Session 是对话的容器，保持上下文连续性。

**会话类型：**
- **main**：主会话，直接对话时共享
- **per-peer**：按发送者隔离的会话
- **per-channel-peer**：按渠道和发送者隔离
- **isolated**：独立会话（用于定时任务等）

**会话配置：**
```json5
{
  session: {
    dmScope: "per-channel-peer",  // DM 会话范围
    reset: {
      mode: "daily",              // 每日重置
      atHour: 4,                   // 凌晨 4 点
    },
  },
}
```

**会话存储位置：**
```
~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl
```

### 3.5 Cron（定时任务）

**定义：** Cron 是 Gateway 内置的调度器，用于定时执行任务。

**任务类型：**
1. **一次性提醒**：在指定时间执行一次
2. **周期性任务**：按 cron 表达式重复执行

**任务配置示例：**

**一次性提醒：**
```bash
openclaw cron add \
  --name "会议提醒" \
  --at "2026-03-23T14:00:00+08:00" \
  --session main \
  --system-event "15分钟后有产品会议" \
  --wake now \
  --delete-after-run
```

**周期性任务：**
```bash
openclaw cron add \
  --name "每日简报" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结昨天的更新" \
  --announce \
  --channel telegram \
  --to "@mychat"
```

**Cron vs Heartbeat：**
| 特性 | Cron | Heartbeat |
|-----|------|-----------|
| 精确时间 | ✅ 支持 | ❌ 约每 30 分钟 |
| 批量检查 | ❌ 单任务 | ✅ 可合并多个检查 |
| 会话隔离 | ✅ 独立会话 | ❌ 主会话 |
| 适用场景 | 定时提醒、报告 | 定期检查邮件、日历等 |

---

## 4. 常用命令

### 4.1 openclaw status

查看系统状态和健康状况。

```bash
# 快速状态
openclaw status

# 详细状态（可分享，已脱敏）
openclaw status --all

# 深度检查（包含健康检查和提供商探测）
openclaw status --deep
```

**输出示例：**
```
OS: macOS 14.3 (arm64)
Node: v24.0.0
Gateway: running on port 18789
Agents: 1 active
Sessions: 3 stored
Provider: anthropic (connected)
```

### 4.2 openclaw gateway

管理 Gateway 服务。

```bash
# 查看状态
openclaw gateway status

# 启动 Gateway
openclaw gateway start

# 停止 Gateway
openclaw gateway stop

# 重启 Gateway
openclaw gateway restart

# 前台运行（调试用）
openclaw gateway

# 指定端口运行
openclaw gateway --port 18789

# 强制启动（杀死占用端口的进程）
openclaw gateway --force
```

### 4.3 openclaw configure

交互式配置向导。

```bash
# 启动配置向导
openclaw configure

# 完整引导流程
openclaw onboard
```

### 4.4 其他常用命令

#### 配置管理
```bash
# 获取配置值
openclaw config get agents.defaults.workspace

# 设置配置值
openclaw config set agents.defaults.heartbeat.every "2h"

# 删除配置值
openclaw config unset plugins.entries.brave.config.webSearch.apiKey
```

#### 模型管理
```bash
# 查看模型状态
openclaw models status

# 查看可用模型
openclaw models list

# 切换模型（在对话中）
# 发送消息：/model claude-sonnet
```

#### 会话管理
```bash
# 列出所有会话
openclaw sessions list

# 查看特定会话
openclaw sessions show <session-id>
```

#### Cron 管理
```bash
# 列出所有任务
openclaw cron list

# 添加任务
openclaw cron add --name "测试" --at "2026-03-23T10:00:00Z" --message "测试消息"

# 运行任务
openclaw cron run <job-id>

# 删除任务
openclaw cron remove <job-id>

# 查看运行历史
openclaw cron runs --id <job-id>
```

#### 渠道管理
```bash
# 查看渠道状态
openclaw channels status

# 带探测的状态检查
openclaw channels status --probe

# 登录渠道（如 WhatsApp）
openclaw channels login whatsapp
```

#### 配对管理
```bash
# 查看待审批请求
openclaw pairing list

# 审批请求
openclaw pairing approve <request-id>
```

#### 日志查看
```bash
# 实时查看日志
openclaw logs --follow

# 查看最近日志
openclaw logs --tail 100
```

#### 诊断工具
```bash
# 运行诊断并自动修复
openclaw doctor

# 仅诊断不修复
openclaw doctor --check

# 生成 Gateway Token
openclaw doctor --generate-gateway-token
```

#### 技能管理
```bash
# 列出已安装技能
openclaw skills list

# 安装技能
openclaw skills install <skill-name>

# 更新技能
openclaw skills update <skill-name>
```

---

## 5. 配置文件

### 5.1 config.yaml（实际为 openclaw.json）

OpenClaw 使用 JSON5 格式的配置文件，位于 `~/.openclaw/openclaw.json`。

**最简配置示例：**
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace"
    }
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"]
    }
  }
}
```

**完整配置结构：**
```json5
{
  // Agent 配置
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "anthropic/claude-sonnet-4-6",
        fallbacks: ["openai/gpt-4o"]
      },
      heartbeat: {
        every: "30m",
        target: "last"
      },
      sandbox: {
        mode: "non-main"  // off | non-main | all
      }
    },
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw"]
        }
      }
    ]
  },

  // 渠道配置
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing"
    },
    whatsapp: {
      enabled: true,
      dmPolicy: "allowlist",
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }
      }
    }
  },

  // 会话配置
  session: {
    dmScope: "per-channel-peer",
    reset: {
      mode: "daily",
      atHour: 4
    }
  },

  // 定时任务配置
  cron: {
    enabled: true,
    maxConcurrentRuns: 2
  },

  // Gateway 配置
  gateway: {
    auth: {
      token: "your-secret-token"
    }
  }
}
```

**配置编辑方式：**
1. **交互式向导**：`openclaw configure`
2. **命令行**：`openclaw config get/set`
3. **Web 控制台**：打开 `http://127.0.0.1:18789`，使用 Config 标签页
4. **直接编辑**：使用文本编辑器修改 `~/.openclaw/openclaw.json`

### 5.2 .env 文件

OpenClaw 也支持通过环境变量配置，通常用于敏感信息。

**常用环境变量：**
```bash
# Gateway 配置
OPENCLAW_HOME=~/.openclaw
OPENCLAW_STATE_DIR=~/.openclaw
OPENCLAW_CONFIG_PATH=~/.openclaw/openclaw.json

# API 密钥
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
GOOGLE_API_KEY=xxx

# Gateway Token
OPENCLAW_GATEWAY_TOKEN=your-secret-token

# Web 搜索
BRAVE_API_KEY=xxx
```

**设置方式：**
```bash
# 临时设置
export ANTHROPIC_API_KEY=sk-ant-xxx

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export ANTHROPIC_API_KEY=sk-ant-xxx' >> ~/.zshrc
```

### 5.3 Skills 配置

每个技能都有自己的配置文件 `SKILL.md`，存放在技能目录下。

**技能目录结构：**
```
~/.openclaw/skills/<skill-name>/
├── SKILL.md        # 技能说明和使用指南
├── scripts/        # 脚本文件
└── templates/      # 模板文件
```

**在工作空间中使用技能：**
技能会在 Agent 会话开始时自动加载。你可以：
1. 直接要求 Agent 使用特定技能
2. 在对话中提及技能相关的任务

**示例：**
```
用户：帮我查一下北京明天的天气
Agent：（自动使用 weather 技能）
```

---

## 6. 使用技巧

### 6.1 如何与 Agent 交互

#### 通过 Web 控制台

1. 打开控制台：
   ```bash
   openclaw dashboard
   ```
2. 在聊天框中输入消息
3. Agent 会回复并执行相应操作

#### 通过聊天应用（以 Telegram 为例）

1. **配置 Telegram Bot：**
   ```bash
   openclaw channels login telegram
   ```
   按提示输入 Bot Token

2. **设置访问控制：**
   ```json5
   {
     channels: {
       telegram: {
         enabled: true,
         botToken: "YOUR_BOT_TOKEN",
         dmPolicy: "allowlist",
         allowFrom: ["tg:YOUR_USER_ID"]
       }
     }
   }
   ```

3. **开始对话：**
   在 Telegram 中找到你的 Bot，发送消息即可

#### 群聊中使用

在群聊中，默认需要 @ 提及 Agent 才会响应：

```
@YourBot 帮我总结一下今天的讨论
```

**配置提及模式：**
```json5
{
  agents: {
    list: [{
      id: "main",
      groupChat: {
        mentionPatterns: ["@YourBot", "YourBot"]
      }
    }]
  },
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true }
      }
    }
  }
}
```

### 6.2 如何安装 Skills

#### 方式一：使用 ClawHub

```bash
# 搜索技能
openclaw skills search <keyword>

# 安装技能
openclaw skills install github

# 更新技能
openclaw skills update github

# 列出已安装技能
openclaw skills list
```

#### 方式二：手动安装

将技能文件夹复制到技能目录：
```bash
cp -r /path/to/skill ~/.openclaw/skills/
```

#### 方式三：工作空间技能

将技能放在工作空间的 `skills` 目录下：
```bash
mkdir -p ~/.openclaw/workspace/skills/my-skill
# 创建 SKILL.md 等文件
```

### 6.3 如何设置定时任务

#### 创建一次性提醒

```bash
# 20 分钟后提醒
openclaw cron add \
  --name "休息提醒" \
  --at "2026-03-22T22:20:00+08:00" \
  --session main \
  --system-event "该休息一下了！" \
  --wake now \
  --delete-after-run
```

#### 创建周期性任务

```bash
# 每天早上 9 点发送简报
openclaw cron add \
  --name "每日简报" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结昨天的 GitHub 活动和重要邮件" \
  --announce \
  --channel telegram \
  --to "@mychat"
```

#### 查看和管理任务

```bash
# 列出所有任务
openclaw cron list

# 查看任务详情
openclaw cron show <job-id>

# 手动运行任务
openclaw cron run <job-id>

# 删除任务
openclaw cron remove <job-id>

# 查看运行历史
openclaw cron runs --id <job-id> --limit 10
```

#### Cron 表达式说明

```
┌───────────── 分钟 (0-59)
│ ┌───────────── 小时 (0-23)
│ │ ┌───────────── 日期 (1-31)
│ │ │ ┌───────────── 月份 (1-12)
│ │ │ │ ┌───────────── 星期 (0-6, 0=周日)
│ │ │ │ │
* * * * *
```

**常用表达式：**
| 表达式 | 含义 |
|-------|------|
| `0 9 * * *` | 每天早上 9:00 |
| `0 */2 * * *` | 每 2 小时 |
| `30 17 * * 1-5` | 工作日下午 5:30 |
| `0 0 1 * *` | 每月 1 日凌晨 |

---

## 7. 常见问题

### 7.1 故障排查流程

**第一步：快速诊断**

```bash
# 查看状态
openclaw status

# 查看 Gateway 状态
openclaw gateway status

# 查看日志
openclaw logs --follow

# 运行诊断
openclaw doctor
```

**第二步：根据问题类型深入排查**

| 问题类型 | 诊断命令 |
|---------|---------|
| Gateway 无法启动 | `openclaw gateway status --deep` |
| 渠道连接问题 | `openclaw channels status --probe` |
| 模型/API 问题 | `openclaw models status` |
| 消息不响应 | `openclaw pairing list` |
| Cron 任务不运行 | `openclaw cron status` |

### 7.2 常见错误解决

#### 问题 1：Gateway 无法启动

**症状：** `openclaw gateway status` 显示 `Runtime: stopped`

**诊断：**
```bash
openclaw logs --follow
openclaw doctor
```

**常见原因及解决：**

1. **端口被占用**
   ```
   Error: EADDRINUSE: address already in use :::18789
   ```
   解决：
   ```bash
   # 找到占用进程
   lsof -i :18789
   # 强制重启
   openclaw gateway --force
   ```

2. **配置文件错误**
   ```
   Config validation failed
   ```
   解决：
   ```bash
   openclaw doctor --fix
   ```

3. **缺少 API 密钥**
   ```
   No API key configured
   ```
   解决：
   ```bash
   openclaw configure
   # 或直接设置环境变量
   export ANTHROPIC_API_KEY=sk-ant-xxx
   ```

#### 问题 2：渠道连接正常但消息无响应

**症状：** 渠道状态显示 connected，但发送消息后无回复

**诊断：**
```bash
openclaw channels status --probe
openclaw pairing list
openclaw config get channels
openclaw logs --follow
```

**常见原因及解决：**

1. **DM 配对未批准**
   ```
   pairing request from +1234567890
   ```
   解决：
   ```bash
   openclaw pairing approve <request-id>
   ```

2. **群聊需要提及**
   ```
   drop guild message (mention required)
   ```
   解决：在消息中 @Agent

3. **不在允许列表**
   ```
   blocked by allowlist
   ```
   解决：添加到 `allowFrom` 或使用 `dmPolicy: "pairing"`

#### 问题 3：API 限流错误

**症状：** `HTTP 429: rate_limit_error`

**诊断：**
```bash
openclaw models status
openclaw config get agents.defaults.models
```

**解决：**
1. 等待限流窗口重置
2. 配置备用模型：
   ```json5
   {
     agents: {
       defaults: {
         model: {
           primary: "anthropic/claude-sonnet",
           fallbacks: ["openai/gpt-4o"]
         }
       }
     }
   }
   ```

#### 问题 4：Dashboard 无法连接

**症状：** 打开 `http://127.0.0.1:18789` 无法访问

**诊断：**
```bash
openclaw gateway status
openclaw health --verbose
```

**常见原因及解决：**

1. **Gateway 未运行**
   ```bash
   openclaw gateway start
   ```

2. **Token 不匹配**
   ```bash
   openclaw config get gateway.auth.token
   # 在 Dashboard 设置中填入正确 token
   ```

3. **远程访问需要配置**
   ```bash
   # 使用 Tailscale
   openclaw gateway --tailscale serve
   # 或创建 SSH 隧道
   ssh -N -L 18789:127.0.0.1:18789 user@host
   ```

#### 问题 5：Cron 任务不执行

**症状：** 定时任务没有按预期运行

**诊断：**
```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <job-id>
```

**常见原因及解决：**

1. **Cron 未启用**
   ```json5
   {
     cron: { enabled: true }
   }
   ```

2. **时区问题**
   确保指定正确的时区：
   ```bash
   openclaw cron add --tz "Asia/Shanghai" ...
   ```

3. **任务执行失败**
   查看运行日志：
   ```bash
   openclaw cron runs --id <job-id> --limit 20
   ```

### 7.3 获取帮助

**官方文档：** https://docs.openclaw.ai

**命令行帮助：**
```bash
openclaw --help
openclaw <command> --help
```

**诊断报告（可分享）：**
```bash
openclaw status --all
```

**GitHub Issues：** https://github.com/openclaw/openclaw/issues

**社区支持：**
- Discord 社区
- GitHub Discussions

---

## 附录

### A. 配置文件完整示例

```json5
// ~/.openclaw/openclaw.json
{
  // Agent 默认配置
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "anthropic/claude-sonnet-4-6",
        fallbacks: ["openai/gpt-4o", "google/gemini-2.0-flash"]
      },
      models: {
        "anthropic/claude-sonnet-4-6": { alias: "Sonnet" },
        "openai/gpt-4o": { alias: "GPT" },
        "google/gemini-2.0-flash": { alias: "Gemini" }
      },
      heartbeat: {
        every: "30m",
        target: "last"
      }
    }
  },

  // 渠道配置
  channels: {
    telegram: {
      enabled: true,
      botToken: "YOUR_BOT_TOKEN",
      dmPolicy: "pairing"
    },
    whatsapp: {
      enabled: true,
      dmPolicy: "allowlist",
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }
      }
    },
    discord: {
      enabled: true,
      botToken: "YOUR_DISCORD_BOT_TOKEN",
      dmPolicy: "pairing"
    }
  },

  // 会话配置
  session: {
    dmScope: "per-channel-peer",
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 120
    }
  },

  // Cron 配置
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h"
  },

  // Gateway 配置
  gateway: {
    auth: {
      token: "your-secure-token-here"
    },
    channelHealthCheckMinutes: 5
  }
}
```

### B. 常用命令速查表

| 命令 | 说明 |
|------|------|
| `openclaw status` | 查看系统状态 |
| `openclaw gateway start/stop/restart` | 管理 Gateway 服务 |
| `openclaw dashboard` | 打开 Web 控制台 |
| `openclaw configure` | 配置向导 |
| `openclaw doctor` | 诊断和修复 |
| `openclaw logs --follow` | 实时日志 |
| `openclaw models status` | 查看模型状态 |
| `openclaw channels status` | 查看渠道状态 |
| `openclaw cron list` | 列出定时任务 |
| `openclaw sessions list` | 列出会话 |
| `openclaw skills list` | 列出技能 |
| `openclaw update` | 更新 OpenClaw |

### C. 相关资源

- **官方网站**：https://openclaw.ai
- **官方文档**：https://docs.openclaw.ai
- **GitHub 仓库**：https://github.com/openclaw/openclaw
- **API 文档**：https://docs.openclaw.ai/gateway/openai-http-api

---

*本手册基于 OpenClaw 官方文档编写，适用于 v24.x 版本*

*最后更新：2026年3月*