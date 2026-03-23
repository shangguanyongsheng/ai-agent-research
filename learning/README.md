# AI Agent 知识图谱

> 用费曼学习法构建 AI Agent 完整知识体系

---

## 🗺️ 知识图谱总览

```
                            ┌─────────────────────────────────────┐
                            │         AI Agent 知识体系            │
                            │     感知 + 决策 + 行动 + 学习         │
                            └─────────────────────────────────────┘
                                            │
        ┌───────────────┬───────────────┬───┴───┬───────────────┬───────────────┐
        │               │               │       │               │
        ▼               ▼               ▼       ▼               ▼
┌───────────────┐┌───────────────┐┌───────────────┐┌───────────────┐┌───────────────┐
│ foundation    ││ memory        ││ tools         ││ evolution     ││ advanced      │
│ 基础概念      ││ 记忆系统      ││ 工具平台      ││ 进化系统      ││ 进阶主题      │
└───────────────┘└───────────────┘└───────────────┘└───────────────┘└───────────────┘
        │               │               │               │               │
        ▼               ▼               ▼               ▼               ▼
┌───────────────┐┌───────────────┐┌───────────────┐┌───────────────┐┌───────────────┐
│ • Agent定义   ││ • 双记忆系统  ││ • OpenClaw    ││ • 进化引擎    ││ • Multi-Agent │
│ • Agent Harness││ • 工作记忆   ││ • Claude Code ││ • EvoMap      ││ • 安全沙箱    │
│ • ReAct框架   ││ • 持久化      ││ • Skills      ││ • 自然选择    ││ • Prompt Eng  │
│ • Planning    ││               ││ • MCP协议     ││               ││ • Hooks机制   │
└───────────────┘└───────────────┘└───────────────┘└───────────────┘└───────────────┘
```

---

## 📂 分支结构

### 1️⃣ [foundation/](./foundation/) - 基础概念

> AI Agent 的核心概念和理论基础

| 知识点 | 文件 | 学习目标 |
|--------|------|----------|
| Agent 定义 | [agent-定义.md](./foundation/agent-定义.md) | 理解 Agent 是什么，与普通 LLM 的区别 |
| Agent Harness | [agent-harness.md](./foundation/agent-harness.md) | 理解控制层的六大功能 |
| ReAct 框架 | [react-框架.md](./foundation/react-框架.md) | 掌握 Thought→Action→Observation 循环 |
| Planning | [planning.md](./foundation/planning.md) | 理解任务分解和规划策略 |

**📖 来源文档**：`docs/Agent_Harness研究报告.md`

---

### 2️⃣ [memory/](./memory/) - 记忆系统

> Agent 如何存储和检索信息

| 知识点 | 文件 | 学习目标 |
|--------|------|----------|
| 双记忆系统 | [双记忆系统.md](./memory/双记忆系统.md) | 理解长期记忆 vs 工作记忆 |
| 工作记忆 | [工作记忆.md](./memory/工作记忆.md) | 理解会话内的临时记忆 |
| 持久化存储 | [持久化存储.md](./memory/持久化存储.md) | 理解如何持久化 Agent 记忆 |

**📖 来源文档**：`learning/02-memory-system.md`

---

### 3️⃣ [tools/](./tools/) - 工具平台

> Agent 使用的工具和平台

| 知识点 | 文件 | 学习目标 |
|--------|------|----------|
| OpenClaw | [openclaw.md](./tools/openclaw.md) | 掌握 Agent 网关的使用 |
| Claude Code | [claude-code.md](./tools/claude-code.md) | 掌握终端 Agent 的使用 |
| Skills 技能系统 | [skills.md](./tools/skills.md) | 理解技能的定义和管理 |
| MCP 协议 | [mcp.md](./tools/mcp.md) | 理解模型上下文协议 |

**📖 来源文档**：`docs/OpenClaw使用手册.md`、`docs/Claude_Code使用手册.md`

---

### 4️⃣ [evolution/](./evolution/) - 进化系统

> Agent 如何自我改进和进化

| 知识点 | 文件 | 学习目标 |
|--------|------|----------|
| 进化引擎 | [进化引擎.md](./evolution/进化引擎.md) | 理解螺旋上升的进化机制 |
| EvoMap 进化网络 | [evomap.md](./evolution/evomap.md) | 理解全球 Agent 知识共享网络 |
| 自然选择 | [自然选择.md](./evolution/自然选择.md) | 理解 GDI 评分和优胜劣汰 |

**📖 来源文档**：`learning/04-evolution-engine.md`、`docs/evomap/`

---

### 5️⃣ [advanced/](./advanced/) - 进阶主题

> 高级概念和实践

| 知识点 | 文件 | 学习目标 |
|--------|------|----------|
| Multi-Agent 协作 | [multi-agent.md](./advanced/multi-agent.md) | 理解多 Agent 协作模式 |
| 安全与沙箱 | [安全沙箱.md](./advanced/安全沙箱.md) | 理解代码执行安全机制 |
| Prompt Engineering | [prompt-engineering.md](./advanced/prompt-engineering.md) | 掌握系统提示词设计 |
| Hooks 机制 | [hooks.md](./advanced/hooks.md) | 理解扩展点和拦截器 |

**📖 来源文档**：`learning/07-multi-agent-collaboration.md`、`learning/08-safety-sandbox.md`

---

## 🎓 费曼学习法

每个知识点都遵循费曼学习法四步法：

```
┌─────────────────────────────────────────────────────────────┐
│                     费曼学习法四步法                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  第一步：概念解释                                            │
│  ├── 用最简单的语言解释                                      │
│  └── 就像教给一个完全不懂的人                                 │
│                                                             │
│  第二步：类比理解                                            │
│  ├── 用生活中的例子类比                                      │
│  └── 帮助建立直觉                                            │
│                                                             │
│  第三步：代码/实践                                           │
│  ├── 通过代码理解实现细节                                    │
│  └── 动手实验巩固理解                                        │
│                                                             │
│  第四步：知识关联                                            │
│  ├── 说明这个概念与其他概念的关系                            │
│  └── 建立完整的知识网络                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 学习路径

### 推荐顺序

```
Week 1: 基础概念
├── foundation/agent-定义.md
├── foundation/agent-harness.md
├── foundation/react-框架.md
└── foundation/planning.md

Week 2: 记忆系统
├── memory/双记忆系统.md
├── memory/工作记忆.md
└── memory/持久化存储.md

Week 3: 工具平台
├── tools/openclaw.md
├── tools/claude-code.md
├── tools/skills.md
└── tools/mcp.md

Week 4: 进化系统
├── evolution/进化引擎.md
├── evolution/evomap.md
└── evolution/自然选择.md

Week 5: 进阶主题
├── advanced/multi-agent.md
├── advanced/安全沙箱.md
├── advanced/prompt-engineering.md
└── advanced/hooks.md
```

---

## 📚 原始文档索引

`learning/` 目录是基于 `docs/` 原始文档的费曼学习法整理：

| 原始文档 | 位置 | 衍生知识点 |
|---------|------|-----------|
| Agent_Harness研究报告.md | docs/ | foundation/* |
| OpenClaw使用手册.md | docs/ | tools/openclaw.md |
| Claude_Code使用手册.md | docs/ | tools/claude-code.md |
| evomap/* | docs/evomap/ | evolution/evomap.md |
| simple-bi-multi-agent-plan.md | docs/ | advanced/multi-agent.md |

---

_📅 更新日期：2026-03-23_
_🐒 毛猴子整理_