# OpenClaw 学习文档

> 本文档使用费曼学习法整理，帮助你快速理解 OpenClaw 的核心概念。

## 🦞 什么是 OpenClaw？

**概念解释：**
OpenClaw 是一个自托管的 AI 网关，将你常用的聊天应用（Discord、WhatsApp、Telegram、Slack 等）连接到 AI 编程助手。你在自己的机器上运行一个 Gateway 进程，它成为消息应用和 AI 助手之间的桥梁。

**类比理解：**
想象 OpenClaw 就像一个"翻译中心"——你从 WhatsApp 发消息，翻译中心接收并转发给 AI，AI 回复后再翻译回来发送到你的聊天应用。不管你用什么聊天软件，翻译中心都能处理。

**核心特点：**
- **自托管**：运行在你的设备上，你的规则
- **多通道**：一个 Gateway 同时服务多个聊天应用
- **Agent 原生**：专为编程 Agent 设计，支持工具调用、会话、记忆和多 Agent 路由
- **开源**：MIT 许可证，社区驱动

## 📚 文档目录

### 基础入门
1. [安装指南](./01-安装指南.md) - 5 分钟快速上手
2. [配置指南](./02-配置指南.md) - 理解配置文件结构

### 核心功能
3. [Skills 技能系统](./03-Skills技能.md) - 扩展 Agent 能力
4. [MCP 协议](./04-MCP协议.md) - Model Context Protocol 支持
5. [Channels 通道](./05-Channels通道.md) - 支持的聊天平台
6. [Gateway 网关](./06-Gateway网关.md) - 运维与监控

## 🚀 快速开始

```bash
# 1. 安装 OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. 运行引导程序
openclaw onboard --install-daemon

# 3. 打开控制面板
openclaw dashboard
```

## 🔄 工作原理

```
聊天应用 → Gateway → AI Agent
          ↑         ↓
     控制面板 ← 回复
```

Gateway 是单一的真实来源，负责：
- 会话管理
- 路由决策
- 通道连接

## 💡 关键概念速查

| 概念 | 说明 |
|------|------|
| **Gateway** | 中央服务进程，协调一切 |
| **Channel** | 连接的聊天平台（如 Telegram） |
| **Skill** | Agent 能力扩展包 |
| **Session** | 对话上下文容器 |
| **Agent** | AI 助手实例 |

## 🔗 官方资源

- 官方文档：https://docs.openclaw.ai
- 技能市场：https://clawhub.ai
- GitHub：社区驱动开发

---

*使用费曼学习法整理：概念解释 → 类比理解 → 实践示例 → 知识关联*