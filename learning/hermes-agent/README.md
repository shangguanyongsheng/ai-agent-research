# Hermes Agent 学习路径总览

> Hermes Agent 是由 Nous Research 开发的自我改进型 AI Agent，具有内置学习闭环，能够从经验中创建技能、在使用中改进技能、主动持久化知识，并在跨会话中建立对用户的深度建模。

---

## 📚 核心特性

| 特性 | 说明 |
|------|------|
| **学习闭环** | Agent 自主创建技能、改进技能、持久化记忆，无需人工干预 |
| **跨平台支持** | CLI + 15+ 消息平台（Telegram/Discord/Slack/WhatsApp/Signal 等） |
| **多模型支持** | 18+ Provider（Nous Portal/OpenRouter/OpenAI/Claude/GLM/DeepSeek 等） |
| **终端后端** | 6 种后端（local/Docker/SSH/Daytona/Modal/Singularity） |
| **Cron 调度** | 自然语言定义定时任务，自动执行 |
| **子 Agent 并行** | spawn subagents，RPC 调用，并行处理 |
| **Skills Hub** | 兼容 agentskills.io 标准，社区技能共享 |

---

## 🎯 学习路径

### 阶段一：快速入门（1-2 天）

| 文档 | 内容 | 适合人群 |
|------|------|----------|
| [01-快速上手](01-快速上手.md) | 安装、配置、第一次对话 | 新用户必读 |
| [02-核心概念](02-核心概念.md) | 学习闭环、技能系统、记忆机制 | 理解架构 |

### 阶段二：深入理解（3-5 天）

| 文档 | 内容 | 适合人群 |
|------|------|----------|
| [03-架构详解](03-架构详解.md) | 多模型、多平台、终端后端 | 开发者 |
| [04-Skills系统](04-Skills系统.md) | 技能创建、改进、Skills Hub | 进阶用户 |
| [05-记忆与用户建模](05-记忆与用户建模.md) | Honcho、FTS5搜索、跨会话召回 | 理解记忆 |

### 阶段三：实战应用（5-7 天）

| 文档 | 内容 | 适合人群 |
|------|------|----------|
| [06-多平台网关](06-多平台网关.md) | Telegram/Discord/Slack/CLI 配置 | 消息集成 |
| [07-Cron调度](07-Cron调度.md) | 自动化任务、自然语言定义 | 自动化 |
| [08-子Agent并行](08-子Agent并行.md) | spawn subagents、RPC调用 | 并行处理 |

### 阶段四：高级部署（7-10 天）

| 文档 | 内容 | 适合人群 |
|------|------|----------|
| [09-Serverless部署](09-Serverless部署.md) | Daytona/Modal 空闲免费模式 | 成本优化 |
| [10-研究特性](10-研究特性.md) | RL训练、轨迹生成、Atropos | 研究者 |
| [11-OpenClaw迁移](11-OpenClaw迁移.md) | 一键迁移、迁移内容详解 | OpenClaw 用户 |
| [12-最佳实践](12-最佳实践.md) | 使用技巧、常见问题 | 所有用户 |

---

## 🔗 官方资源

- **GitHub**: https://github.com/NousResearch/hermes-agent
- **文档**: https://hermes-agent.nousresearch.com/docs/
- **Skills Hub**: https://agentskills.io
- **Discord**: https://discord.gg/NousResearch

---

## 💡 费曼学习法模板

每个知识点遵循以下结构：

```markdown
## 第一步：概念解释
用最简单的语言解释，像教给小孩。

## 第二步：类比理解
用生活中的例子类比。

## 第三步：代码/实践
动手实验或代码示例。

## 第四步：知识关联
与其他概念的关系，建立知识网络。
```

---

## 🚀 快速命令参考

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 启动对话
hermes

# 选择模型
hermes model

# 配置工具
hermes tools

# 启动网关
hermes gateway start

# Cron 管理
hermes cron list

# Skills 搜索
hermes skills search kubernetes
```

---

## 📊 与 OpenClaw 的关系

Hermes Agent 由 Nous Research 开发，OpenClaw 是一个类似的开源 AI Agent 项目。两者有以下关系：

- **兼容性**: Hermes 支持一键从 OpenClaw 迁移
- **Skills 标准**: 都支持 agentskills.io 标准
- **架构相似**: CLI + Gateway + Skills + Memory

---

*文档整理时间: 2026-04-11*
*来源: Hermes Agent 官方文档*