# 🐙 GitHub Agent 学习型方案

**目标**: 通过学习 GitHub 技能，构建一套可复用的 Agent 学习模式

---

## 📋 方案概述

### 阶段划分

```
┌─────────────────────────────────────────────────────────────┐
│  阶段 1: 环境准备                                              │
│  ├── 安装 GitHub CLI (gh)                                    │
│  ├── 配置认证                                                 │
│  └── 验证技能就绪                                             │
├─────────────────────────────────────────────────────────────┤
│  阶段 2: 创建专用 Agent                                        │
│  ├── 创建 github-dev Agent                                   │
│  ├── 配置身份和性格                                           │
│  └── 绑定 GitHub 技能                                         │
├─────────────────────────────────────────────────────────────┤
│  阶段 3: 学习与实践                                            │
│  ├── 基础操作: 查看仓库、PR、Issue                             │
│  ├── 中级操作: 创建 PR、合并代码                               │
│  └── 高级操作: CI/CD、自动化工作流                             │
├─────────────────────────────────────────────────────────────┤
│  阶段 4: 能力输出                                              │
│  ├── 记录学习日志                                             │
│  ├── 发布基因胶囊到 EvoMap                                    │
│  └── 形成可复用的学习模板                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 阶段 1: 环境准备

### 1.1 安装 GitHub CLI

```bash
# 方法 1: 使用 apt (推荐)
sudo apt update
sudo apt install gh -y

# 方法 2: 使用 brew
brew install gh

# 验证安装
gh --version
```

### 1.2 配置认证

```bash
# 交互式登录
gh auth login

# 选择:
# - GitHub.com
# - HTTPS
# - Login with a web browser

# 验证认证
gh auth status
```

### 1.3 验证技能就绪

```bash
# 检查技能状态
openclaw skills info github

# 期望输出: ✓ ready
```

---

## 🤖 阶段 2: 创建专用 Agent

### 2.1 创建 Agent

```bash
# 创建 GitHub 专用 Agent
openclaw agents add github-dev

# 设置身份
openclaw agents set-identity github-dev \
  --name "GitHub 助手" \
  --emoji "🐙" \
  --theme "技术专家"
```

### 2.2 Agent 配置结构

```
/home/admin/.openclaw/agents/github-dev/
├── identity.json       # 身份配置
├── memory/
│   └── MEMORY.md       # GitHub 专用记忆
├── sessions/           # 会话记录
└── workspace/
    ├── .learnings/     # 学习日志
    │   ├── ERRORS.md
    │   └── LEARNINGS.md
    └── skills/         # 专用技能
        └── github-operations/
```

### 2.3 绑定技能

```bash
# GitHub Agent 自动继承全局技能
# 可以添加更多专用技能

openclaw agents bind github-dev \
  --skill github \
  --skill gh-issues
```

---

## 📚 阶段 3: 学习与实践

### 3.1 基础操作 (Level 1)

| 技能 | 命令 | 学习目标 |
|------|------|----------|
| 查看仓库 | `gh repo view owner/repo` | 了解仓库结构 |
| 列出 PR | `gh pr list --repo owner/repo` | 查看 PR 列表 |
| 列出 Issue | `gh issue list --repo owner/repo` | 查看 Issue 列表 |
| 查看 PR 详情 | `gh pr view 123` | 理解 PR 结构 |

**学习输出**: `LEARNINGS.md` 记录基础操作笔记

### 3.2 中级操作 (Level 2)

| 技能 | 命令 | 学习目标 |
|------|------|----------|
| 创建 Issue | `gh issue create` | 问题追踪 |
| 创建 PR | `gh pr create` | 代码贡献流程 |
| 检查 CI | `gh pr checks 123` | CI/CD 理解 |
| 合并 PR | `gh pr merge 123` | 代码合并流程 |

**学习输出**: 创建实际 PR/Issue，记录流程

### 3.3 高级操作 (Level 3)

| 技能 | 命令 | 学习目标 |
|------|------|----------|
| 查看 CI 日志 | `gh run view` | CI 排错能力 |
| 创建 Release | `gh release create` | 发布流程 |
| API 查询 | `gh api repos/owner/repo` | API 使用 |
| 自动化脚本 | 编写 shell 脚本 | 自动化能力 |

**学习输出**: 发布自动化脚本到 EvoMap

---

## 📤 阶段 4: 能力输出

### 4.1 学习日志结构

```markdown
# GitHub 操作学习日志

## [LRN-20260316-001] gh_pr_workflow

### 学习内容
- 如何创建 PR
- 如何检查 CI 状态
- 如何合并 PR

### 最佳实践
1. 创建 PR 前先检查 CI
2. 合并前确保 review 通过
3. 使用 squash merge 保持历史整洁

### 常见错误
- ❌ 未配置 gh auth
- ❌ 没有仓库权限
- ❌ PR 标题不规范

### 可复用命令
\`\`\`bash
# 一键检查 PR 状态
gh pr view $PR_NUMBER --json title,state,mergeable,statusCheckRollup

# 批量关闭过期 Issue
gh issue list --state open --label stale | xargs -I {} gh issue close {}
\`\`\`
```

### 4.2 发布到 EvoMap

```bash
# 使用 evomap-connector 技能
cd ~/.openclaw/workspace/skills/evomap-connector

# 发布学习胶囊
node scripts/publish.js \
  --category learning \
  --signals "github,gh-cli,pr-workflow" \
  --gene-summary "GitHub CLI 操作最佳实践" \
  --capsule-summary "从零学习 GitHub CLI 的完整路径" \
  --confidence 0.85
```

### 4.3 形成学习模板

将此次学习过程抽象为模板，用于未来学习其他技能：

```
学习模板 = {
  阶段1: 环境准备 → 安装工具 + 配置认证
  阶段2: 创建Agent → 专用身份 + 技能绑定
  阶段3: 学习实践 → 基础/中级/高级 操作
  阶段4: 能力输出 → 学习日志 + EvoMap发布
}
```

---

## 🎯 预期成果

| 成果 | 描述 | 文件位置 |
|------|------|----------|
| **GitHub Agent** | 专用于 GitHub 操作的 Agent | `~/.openclaw/agents/github-dev/` |
| **学习日志** | GitHub 操作学习笔记 | `~/.openclaw/workspace/.learnings/` |
| **技能就绪** | GitHub 技能可用 | `openclaw skills info github` |
| **EvoMap 胶囊** | 可被其他 Agent 继承的能力 | EvoMap 网络 |
| **学习模板** | 可复用的学习流程 | `docs/agent-learning-template.md` |

---

## 📊 时间规划

| 阶段 | 预计时间 | 里程碑 |
|------|----------|--------|
| 阶段 1 | 10 分钟 | `gh auth status` 通过 |
| 阶段 2 | 5 分钟 | Agent 创建成功 |
| 阶段 3 | 30-60 分钟 | 完成 Level 1-2 操作 |
| 阶段 4 | 15 分钟 | 发布学习胶囊 |

**总计**: 约 1 小时

---

## ❓ 需要确认

在开始执行之前，请确认：

1. **GitHub 账号**: 你有 GitHub 账号吗？
2. **仓库访问**: 有想要操作的特定仓库吗？
3. **学习深度**: 想学到哪个 Level？(1/2/3)
4. **发布意愿**: 是否愿意将学习成果发布到 EvoMap？

---

**准备好了吗？告诉我你的选择！** 🦞