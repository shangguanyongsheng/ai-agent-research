# OpenClaw

> 知识分支：tools（工具平台）

---

## 🎯 学习目标

掌握 OpenClaw 的使用，理解它如何作为 Agent 网关工作。

---

## 第一步：概念解释

### OpenClaw 是什么？

**给小孩解释**：
> OpenClaw 是一个桥梁，连接你的聊天软件（WhatsApp、Telegram、Discord）和 AI Agent。你在手机上发消息，Agent 就能在电脑上帮你干活。

**一句话定义**：
> OpenClaw 是自托管的 AI Agent 网关，让 Agent 通过聊天应用与你交互。

### 架构图

```
┌─────────────────────────────────────────────────────┐
│                    你的设备                          │
│    📱 手机（WhatsApp/Telegram/Discord）             │
└─────────────────────────────────────────────────────┘
                        ↕ 消息
┌─────────────────────────────────────────────────────┐
│                OpenClaw Gateway                      │
│    🏠 运行在你自己的服务器/电脑上                     │
│    ├── 接收消息                                      │
│    ├── 调用 AI 模型                                  │
│    ├── 执行 Agent 任务                               │
│    └── 返回结果                                      │
└─────────────────────────────────────────────────────┘
                        ↕ API
┌─────────────────────────────────────────────────────┐
│                   AI 模型                            │
│    🤖 Claude / GPT-4 / Gemini 等                    │
└─────────────────────────────────────────────────────┘
```

### 核心能力

| 能力 | 说明 |
|------|------|
| 多渠道 | WhatsApp、Telegram、Discord、iMessage |
| 多模型 | 35+ 模型提供商 |
| 自动化 | Cron 定时任务、Heartbeat 检查 |
| 移动端 | iOS/Android 节点配对 |
| 技能系统 | 可扩展的 Skills |

---

## 第二步：类比理解

### 类比：智能客服系统

| OpenClaw 组件 | 智能客服对应 |
|--------------|-------------|
| Gateway | 客服系统后台 |
| 渠道（Telegram 等） | 电话、网页聊天 |
| Agent | 客服 AI |
| Skills | 客服话术库 |

### 类比：家庭中控

| OpenClaw | 家庭中控 |
|----------|---------|
| 多渠道接入 | 手机 App、语音、面板 |
| Agent | 智能助手 |
| Skills | 控制灯光、空调等 |

---

## 第三步：常用命令

### 基本操作

```bash
# 检查 Gateway 状态
openclaw gateway status

# 启动 Gateway
openclaw gateway start

# 停止 Gateway
openclaw gateway stop

# 打开控制面板
openclaw dashboard
```

### 技能管理

```bash
# 安装技能
openclaw skills install <skill-name>

# 列出已安装技能
openclaw skills list

# 更新技能
openclaw skills update
```

### 配置

```bash
# 初始化配置
openclaw onboard

# 设置模型
openclaw config set model claude-sonnet-4
```

---

## 第四步：知识关联

### OpenClaw 在知识体系中的位置

```
AI Agent 知识体系
│
├── tools（工具平台）◄── 你在这里
│   ├── OpenClaw
│   ├── Claude Code
│   ├── Skills
│   └── MCP
│
├── foundation
│   └── Agent 通过 OpenClaw 与用户交互
│
└── advanced
    └── Hooks 可以扩展 OpenClaw
```

---

## 🧪 动手实验

### 实验：检查 OpenClaw 状态

```bash
# 检查 Gateway 是否运行
openclaw gateway status

# 应该看到类似：
# Runtime: running
# RPC probe: ok
# Uptime: 2h 30m
```

---

## ❓ 思考题

1. OpenClaw 和 Claude Code 有什么区别？
2. 为什么 OpenClaw 需要自托管？有什么好处？
3. OpenClaw 支持哪些渠道？你常用哪个？

---

## 📚 延伸阅读

- [Claude Code](./claude-code.md) - 终端 Agent 工具
- [Skills](./skills.md) - 技能系统
- [原始文档](../../docs/OpenClaw使用手册.md) - 完整使用手册

---

_📅 更新日期：2026-03-23_
_🐒 毛猴子整理_