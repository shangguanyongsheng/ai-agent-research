# OpenClaw 知识库

> 📝 **费曼学习法整理** - 用最简单的语言理解 OpenClaw

---

## 什么是 OpenClaw？

**一句话解释**：OpenClaw 是一个自托管网关，让你在 Discord、WhatsApp、Telegram、Slack 等聊天应用中与 AI 对话。

**类比理解**：
- 就像一个「翻译官」，连接你的聊天软件和 AI 大脑
- 你在 WhatsApp 发消息 → OpenClaw 收到 → 转给 AI → AI 回复 → OpenClaw 送回 WhatsApp

**核心特点**：
- 🔐 **自托管** - 运行在你自己的机器上，数据不外流
- 📱 **多通道** - 一个网关支持所有主流聊天应用
- 🤖 **Agent原生** - 专为 AI Agent 设计，支持工具调用、记忆、多 Agent 路由
- 📖 **开源** - MIT 许可证，社区驱动

---

## 知识库导航

| 文档 | 内容 | 适合人群 |
|------|------|----------|
| [00-快速上手](./00-quickstart.md) | 5分钟完成安装和首次对话 | 新手必看 |
| [01-安装指南](./01-installation.md) | 各平台安装方法详解 | 部署用户 |
| [02-配置详解](./02-configuration.md) | openclaw.json 配置全解 | 配置调优 |
| [03-Skills系统](./03-skills.md) | 技能扩展机制 | 扩展开发者 |
| [04-MCP协议](./04-mcp.md) | Model Context Protocol | 工具集成 |
| [05-通道集成](./05-channels.md) | Discord/WhatsApp/Telegram等 | 通道配置 |
| [06-Gateway网关](./06-gateway.md) | 网关架构与原理 | 架构理解 |
| [07-子Agent系统](./07-subagents.md) | 多 Agent 路由与隔离 | 多用户场景 |
| [08-定时任务](./08-cron.md) | Cron/Hooks 自动化 | 自动化场景 |
| [09-安全最佳实践](./09-security.md) | 认证、权限、沙箱 | 安全配置 |
| [10-故障排查](./10-troubleshooting.md) | 常见问题与解决方案 | 运维必看 |
| [11-社区资源](./11-community.md) | GitHub/Discord 资源 | 社区参与 |
| [12-ClawHub Skills](./12-clawhub-skills.md) | Skills 市场推荐 | Skills使用 |
| [13-高级模式](./13-advanced-patterns.md) | 多网关、远程部署等 | 高级用户 |

---

## 学习路径

### 🌱 新手入门（Day 1）
```
00-快速上手 → 01-安装指南 → 02-配置详解 → 05-通道集成
```
目标：能从手机聊天软件与 AI 对话

### 🚀 进阶配置（Day 2-3）
```
03-Skills系统 → 04-MCP协议 → 07-子Agent系统 → 09-安全最佳实践
```
目标：配置多 Agent、扩展技能、确保安全

### 🏆 高级运维（Day 4+）
```
06-Gateway网关 → 08-定时任务 → 10-故障排查 → 13-高级模式
```
目标：生产部署、自动化、故障恢复

---

## 架构图解

```
┌─────────────────┐
│  聊天应用层      │  Discord, WhatsApp, Telegram, Slack...
│  (Channels)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gateway 网关    │  ← 核心枢纽
│  (单进程服务)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Agent       │  Pi / Claude Code / Codex
│  (模型+工具)     │
└─────────────────┘
```

**核心组件**：
- **Gateway** - 单进程服务，监听 18789 端口
- **Channels** - 通道插件，连接各聊天平台
- **Agent** - AI 模型 + 工具集 + Skills
- **Session** - 会话管理，隔离不同用户对话

---

## 官方资源

| 资源 | 链接 | 说明 |
|------|------|------|
| 官方文档 | https://docs.openclaw.ai | 最权威的参考 |
| GitHub仓库 | https://github.com/openclaw/openclaw | 源码与 Issue |
| ClawHub | https://clawhub.ai | Skills 市场 |
| Discord社区 | https://discord.gg/clawd | 实时讨论 |

---

## 快速命令参考

```bash
# 安装
curl -fsSL https://openclaw.ai/install.sh | bash

# 初始化
openclaw onboard --install-daemon

# 查看状态
openclaw gateway status

# 打开控制面板
openclaw dashboard

# 查看日志
openclaw logs

# 健康检查
openclaw doctor
```

---

> 💡 **提示**：建议按顺序阅读，每个文档都采用费曼学习法编写，循序渐进。