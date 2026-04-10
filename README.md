# AI Agent Research

> AI Agent 研究与实践文档仓库，由**文档 Agent** 驱动

---

## 🤖 文档 Agent 能力

这是一个**文档 Agent** 项目，不是代码项目。Agent 的核心能力是：

### 🔍 调研学习

输入一个名词或 URL，Agent 会：
- 搜索多个来源
- 阅读并理解内容
- 提取核心概念

### 📄 生成报告

调研后自动生成研究报告到 `docs/`：
- 概念定义
- 技术原理
- 应用场景
- 相关技术

### 📚 知识图谱

将知识整理到 `learning/`，按费曼学习法组织：

```
learning/
├── foundation/    # 基础概念（Agent、ReAct、Harness）
├── memory/        # 记忆系统
├── tools/         # 工具平台（OpenClaw、Claude Code、Skills）
├── evolution/     # 进化系统（进化引擎、EvoMap）
└── advanced/      # 进阶主题（Multi-Agent、安全沙箱）
```

### 💬 如何使用

在 OpenClaw Web UI 中直接说：

```
调研 MCP 协议
```

或：

```
帮我了解 https://xxx.com/xxx
```

Agent 会自动完成：**调研 → 生成报告 → 整理知识图谱 → 提交 GitHub**

---

## 📂 目录结构

```
ai-agent-research/
├── .claude/              # Claude Code 配置
│   ├── CLAUDE.md         # 文档 Agent 指令
│   └── skills/           # Agent 技能
│
├── docs/                 # 研究报告（原始文档）
│   ├── Agent_Harness研究报告.md
│   ├── OpenClaw使用手册.md
│   ├── Claude_Code使用手册.md
│   ├── evomap/          # EvoMap 相关文档
│   └── market-research/ # 市场研究
│
├── learning/             # 知识图谱（费曼学习法）
│   ├── README.md        # 知识图谱入口
│   ├── foundation/      # 基础概念分支
│   ├── memory/          # 记忆系统分支
│   ├── tools/           # 工具平台分支
│   ├── evolution/       # 进化系统分支
│   └── advanced/        # 进阶主题分支
│
├── skills/               # OpenClaw Skills
│   └── research-to-graph/  # 调研到知识图谱
│
├── daily/                # 日报
├── monthly/              # 月报
└── apps/                 # 应用
```

---

## 📚 文档索引

### 使用手册

| 文档 | 说明 |
|------|------|
| [OpenClaw使用手册](docs/OpenClaw使用手册.md) | 完整的 OpenClaw 安装配置指南 |
| [Claude_Code使用手册](docs/Claude_Code使用手册.md) | Claude Code 开发者指南 |

### 研究报告

| 文档 | 说明 |
|------|------|
| [Agent_Harness研究报告](docs/Agent_Harness研究报告.md) | Agent 框架深度研究 |
| [EvoMap 概览](docs/evomap/EvoMap概览.md) | 全球 AI Agent 进化网络 |
| [Gene 和 Capsule 详解](docs/evomap/Gene和Capsule详解.md) | EvoMap 核心数据结构 |
| [GDI 评分流程](docs/evomap/GDI评分和验证流程.md) | 质量保证机制 |

### 项目规划

| 文档 | 说明 |
|------|------|
| [Simple BI 多Agent 计划](docs/simple-bi-multi-agent-plan.md) | 多 Agent 协作方案 |

---

## 🗺️ 知识图谱

### 入口

[learning/README.md](learning/README.md) - 完整的知识图谱导航

### 分支

| 分支 | 内容 | 知识点 |
|------|------|--------|
| `foundation/` | 基础概念 | Agent 定义、Harness、ReAct 框架 |
| `memory/` | 记忆系统 | 双记忆系统 |
| `tools/` | 工具平台 | OpenClaw、Claude Code、Skills |
| `evolution/` | 进化系统 | 进化引擎、EvoMap |
| `advanced/` | 进阶主题 | Multi-Agent、安全沙箱、Prompt Engineering |

### 学习路径

1. **Week 1**: 基础概念（foundation/）
2. **Week 2**: 记忆系统（memory/）
3. **Week 3**: 工具平台（tools/）
4. **Week 4**: 进化系统（evolution/）
5. **Week 5**: 进阶主题（advanced/）

---

## 🎓 费曼学习法

每个知识点都遵循四步法：

| 步骤 | 内容 |
|------|------|
| 第一步 | **概念解释** - 用简单语言解释 |
| 第二步 | **类比理解** - 用生活例子类比 |
| 第三步 | **代码/实践** - 动手实验 |
| 第四步 | **知识关联** - 建立概念关系 |

---

## 🛠️ 应用

### news-daily

AI 新闻日报生成器 v3.2
- 数据源：Hacker News + 硅谷媒体
- 支持定时推送到 QQ Bot

---

## 📅 日报

每日 AI Agent 研究日报存放在 [daily/](daily/) 目录

---

## 🔗 相关链接

- **OpenClaw 文档**: https://docs.openclaw.ai
- **ClawHub 技能市场**: https://clawhub.com
- **EvoMap 进化网络**: https://evomap.ai

---

_🐒 文档 Agent v1.0 · 让知识体系化_