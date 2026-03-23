# Skills 技能系统

> 知识分支：tools（工具平台）

---

## 🎯 学习目标

理解 Skills 是什么，如何定义和管理 Agent 的能力。

---

## 第一步：概念解释

### Skills 是什么？

**给小孩解释**：
> Skills 就像 Agent 的技能包。每个 Skill 教会 Agent 一个特定的本领，比如查天气、搜 GitHub、生成报告。需要什么本领，就装什么技能包。

**一句话定义**：
> Skills 是预定义的任务模板，让 Agent 具备特定领域的能力。

### 技能类型

```
┌─────────────────────────────────────────────────────┐
│                   Skills 分类                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  内置技能（系统自带）                                │
│  ├── github - GitHub 操作                          │
│  ├── weather - 天气查询                            │
│  └── healthcheck - 安全检查                        │
│                                                     │
│  托管技能（~/.openclaw/skills/）                    │
│  ├── agent-reach - 多平台搜索                       │
│  └── evomap-connector - 进化网络                   │
│                                                     │
│  工作空间技能（workspace/skills/）                  │
│  └── 自定义技能                                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 第二步：类比理解

### 类比：手机 App

| Skills | 手机 App |
|--------|---------|
| 内置技能 | 系统自带 App |
| 安装技能 | 从应用商店下载 |
| 自定义技能 | 自己开发的 App |
| SKILL.md | App 的使用说明 |

### 类比：游戏技能

| Skills | 游戏技能 |
|--------|---------|
| 安装技能 | 学习技能 |
| 调用技能 | 释放技能 |
| Skills 列表 | 技能栏 |
| SKILL.md | 技能说明 |

---

## 第三步：技能文件结构

### SKILL.md 示例

```markdown
---
name: weather
description: 获取天气和预报信息
---

# Weather Skill

## 功能
- 获取当前天气
- 获取未来天气预报

## 使用方法
当用户询问天气时，调用天气 API 获取信息。

## 参数
- location: 地理位置
- days: 预报天数（可选）
```

### 安装技能

```bash
# 从 ClawHub 安装
npx skills add <owner/repo@skill>

# 或使用 OpenClaw CLI
openclaw skills install <skill-name>

# 列出已安装技能
openclaw skills list
```

---

## 第四步：知识关联

### Skills 在知识体系中的位置

```
AI Agent 知识体系
│
├── foundation
│   └── Agent Harness 管理的工具
│
├── tools ◄── 你在这里
│   ├── OpenClaw
│   ├── Claude Code
│   └── Skills（Agent 的能力）
│
└── evolution
    └── 进化引擎可以生成新 Skill
```

---

## 🧪 动手实验

### 实验：查看已安装技能

```bash
# 查看系统技能
ls ~/.openclaw/skills/

# 查看工作空间技能
ls ~/.openclaw/workspace/skills/

# 阅读技能说明
cat ~/.openclaw/workspace/skills/evomap-connector/SKILL.md
```

---

## ❓ 思考题

1. Skills 和 Tools 有什么区别？
2. 什么情况下需要自定义 Skill？
3. 如何设计一个好的 Skill？

---

## 📚 延伸阅读

- [OpenClaw](./openclaw.md) - Agent 平台
- [进化引擎](../evolution/进化引擎.md) - 自动生成 Skill
- [原始文档](../../learning/03-skills-system.md) - 完整技术文档

---

_📅 更新日期：2026-03-23_
_🐒 毛猴子整理_