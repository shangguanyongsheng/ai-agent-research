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

## 第三步：核心功能

### 3.1 Skills（技能）— 扩展能力

**⚠️ 常见问题：为什么 `/md` 不触发？**

**原因**：Skills 需要正确创建，不是随便写个命令就能用。

**正确创建步骤**：
```bash
# 1. 创建目录
mkdir -p ~/.claude/skills/md

# 2. 创建 SKILL.md（必须有这个文件名！）
cat > ~/.claude/skills/md/SKILL.md << 'EOF'
---
name: md
description: 创建 Markdown 文档
---

创建 Markdown 文档：$ARGUMENTS

步骤：
1. 分析文档需求
2. 创建文件
3. 添加标准格式
EOF
```

**验证**：启动后输入 `/skills` 查看是否出现。

**Skills 目录位置**：
| 位置 | 路径 | 适用范围 |
|------|------|----------|
| 个人技能 | `~/.claude/skills/<name>/SKILL.md` | 所有项目 |
| 项目技能 | `.claude/skills/<name>/SKILL.md` | 当前项目 |

**关键点**：
- 文件名必须是 `SKILL.md`（不是 `skill.md` 或其他）
- `name` 字段决定命令名（`name: md` → `/md`）
- `description` 帮助 Claude 判断何时自动使用

### 3.2 CLAUDE.md — 项目记忆

**作用**：让 Claude 记住项目规则、命令、约定。

**位置**：
- 项目级：`./CLAUDE.md` 或 `./.claude/CLAUDE.md`
- 用户级：`~/.claude/CLAUDE.md`

**常见问题：Claude 不遵循我的规则**

**解决方案**：
1. **文件大小**：保持在 200 行以内
2. **具体化**：
   ```markdown
   # ❌ 模糊
   格式化代码
   
   # ✅ 具体
   使用 2 空格缩进，语句末尾不加分号
   ```
3. **结构化**：使用标题和列表

### 3.3 斜杠命令速查

**会话管理**：
- `/clear` - 清除历史
- `/compact` - 压缩上下文
- `/resume` - 恢复会话

**项目管理**：
- `/init` - 初始化项目配置
- `/status` - 查看状态
- `/context` - 上下文使用情况

**调试**：
- `/doctor` - 诊断问题
- `/debug` - 调试会话
- `/skills` - 查看可用技能

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

### Skills vs CLAUDE.md 选择

| 场景 | 推荐方式 |
|------|----------|
| 构建命令、代码风格 | CLAUDE.md |
| 特定任务工作流 | Skills |
| 按文件类型限定 | `.claude/rules/` |
| 团队共享 | 项目级 CLAUDE.md |

---

## 🧪 动手实验

### 实验 1：创建你的第一个 Skill

```bash
mkdir -p ~/.claude/skills/hello
cat > ~/.claude/skills/hello/SKILL.md << 'EOF'
---
name: hello
description: 向用户打招呼
---

你好！我是 Claude Code 的技能演示。
你传入了参数：$ARGUMENTS
EOF
```

然后启动 Claude Code，输入 `/hello 世界`。

### 实验 2：优化 CLAUDE.md

检查你项目的 CLAUDE.md：
1. 是否超过 200 行？
2. 规则是否具体可验证？
3. 有无矛盾的规则？

---

## ❓ 思考题

1. Claude Code 和 OpenClaw 有什么区别？各自适合什么场景？
2. 什么时候用 Skills，什么时候用 CLAUDE.md？
3. Skill 不触发时应该如何排查？

---

## 📚 延伸阅读

- [完整使用手册](../../docs/Claude_Code使用手册.md)
- [OpenClaw](./openclaw.md) - 聊天渠道 Agent
- [Skills](./skills.md) - 技能系统

---

_📅 更新日期：2026-03-24_
_🐒 毛猴子整理_