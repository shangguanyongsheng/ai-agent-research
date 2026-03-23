# Claude Code

> 知识分支：tools（工具平台）

---

## 🎯 学习目标

掌握 Claude Code 的使用，理解它如何作为终端 Agent 工作。

---

## 第一步：概念解释

### Claude Code 是什么？

**给小孩解释**：
> Claude Code 是一个在电脑终端里运行的 AI 程序员。你告诉它想做什么，它自己会看文件、写代码、运行命令，不用你一步步指导。

**一句话定义**：
> Claude Code 是 Anthropic 官方的命令行工具，让 Claude 在终端中自主完成开发任务。

### 与其他工具的区别

| 特性 | Claude Code | Cursor | Copilot |
|------|-------------|--------|---------|
| 模式 | 代理型（自主执行） | 辅助型 | 补全型 |
| 文件操作 | ✅ 自主读写 | ✅ 需确认 | ❌ |
| 命令执行 | ✅ 执行 Shell | ❌ | ❌ |
| 项目探索 | ✅ 自动分析 | ⚠️ 有限 | ❌ |

---

## 第二步：类比理解

### 类比：程序员 vs 助手

| Claude Code | Cursor/Copilot |
|-------------|---------------|
| 像雇了一个程序员 | 像雇了一个助手 |
| 你说需求，他做完 | 你写代码，他建议 |
| 自主性强 | 需要你主导 |

### 类比：自动驾驶

| Claude Code | Cursor | Copilot |
|-------------|--------|---------|
| 完全自动驾驶 | 辅助驾驶 | 车道保持 |

---

## 第三步：常用命令

### 基本操作

```bash
# 启动 Claude Code
claude

# 检查状态
claude /status

# 切换模型
claude /model claude-sonnet-4

# 查看帮助
claude /help
```

### 常用任务

```bash
# 分析代码库
> 给我这个项目的整体架构概览

# 创建项目
> 创建一个 React + TypeScript 项目

# 修复 Bug
> 修复 src/auth.ts 中的登录 Bug

# 写测试
> 为 src/utils.ts 写单元测试
```

---

## 第四步：知识关联

### Claude Code 在知识体系中的位置

```
AI Agent 知识体系
│
├── tools（工具平台）◄── 你在这里
│   ├── OpenClaw（聊天渠道）
│   ├── Claude Code（终端渠道）
│   ├── Skills
│   └── MCP
│
└── foundation
    └── Claude Code 是 Agent 的一种实现
```

---

## 🧪 动手实验

### 实验：使用 Claude Code

```bash
# 启动
claude

# 尝试任务
> 帮我创建一个简单的 Python 脚本，读取当前目录的文件列表

# 观察它如何：
# 1. 理解需求
# 2. 创建文件
# 3. 写代码
# 4. 测试运行
```

---

## ❓ 思考题

1. Claude Code 和 OpenClaw 有什么区别？各自适合什么场景？
2. 什么时候用代理型工具，什么时候用辅助型工具？
3. Claude Code 的安全性如何保证？

---

## 📚 延伸阅读

- [OpenClaw](./openclaw.md) - 聊天渠道 Agent
- [Skills](./skills.md) - 技能系统
- [原始文档](../../docs/Claude_Code使用手册.md) - 完整使用手册

---

_📅 更新日期：2026-03-23_
_🐒 毛猴子整理_