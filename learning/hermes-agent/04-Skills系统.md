# 04-Skills系统

> 技能是 Agent 的"操作手册"，可自动创建、改进、共享。理解 Skills 的完整生命周期。

---

## 第一步：概念解释

### 什么是 Skill？

**Skill** 是一个"按需加载的知识文档"，包含：
- 触发条件（什么时候使用）
- 操作步骤（怎么做）
- 常见陷阱（避免的错误）
- 验证方法（确认是否成功）

Skills 存储在 `~/.hermes/skills/`，兼容 [agentskills.io](https://agentskills.io) 标准。

---

### Skills 的三个来源

| 来源 | 说明 | 信任级别 |
|------|------|----------|
| **内置 Skills** | 随 Hermes 安装 | 完全信任 |
| **Agent 创建** | Agent 自动创建 | 完全信任 |
| **Skills Hub** | 社区共享 | 需安全扫描 |

---

## 第二步：类比理解

### Skills = 员工的操作手册

新员工 → 只有基本能力（工具）
有 Skills 的员工 → 有操作手册，可以：
  - 快速完成复杂任务（按手册执行）
  - 避免常见错误（手册有陷阱提醒）
  - 传授给其他员工（共享 Skills）

### 类比示例

```
没有 Skills：
用户："部署 Kubernetes 应用"
Agent："好的，搜索怎么做...尝试...失败...再尝试...成功"
（下次遇到同样问题，又从头开始）

有 Skills：
用户："部署 Kubernetes 应用"
Agent："我有 deploy-k8s 技能，直接用！"
→ 加载 SKILL.md
→ 按步骤执行
→ 快速完成
```

### Skills Hub = 共享图书馆

Skills Hub 是社区共享的技能库：
- 下载别人的手册（hermes skills install）
- 上传自己的手册（hermes skills publish）
- 搜索需要的手册（hermes skills search）

---

## 第三步：代码/实践

### SKILL.md 格式

```markdown
---
name: my-skill
description: 简短描述
version: 1.0.0
platforms: [macos, linux]  # 可选：限制操作系统
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]  # 可选：条件激活
    requires_toolsets: [terminal]  # 可选：条件激活
    config:
      - key: my.setting
        description: "配置说明"
        default: "value"
---

# Skill Title

## When to Use
触发条件

## Procedure
1. 第一步
2. 第二步

## Pitfalls
- 已知的失败模式和修复方法

## Verification
如何确认成功
```

---

### Skills 目录结构

```
~/.hermes/skills/
├── mlops/              # 分类目录
│   ├── axolotl/
│   │   ├── SKILL.md    # 主指令（必需）
│   │   ├── references/ # 参考资料
│   │   ├── templates/  # 输出模板
│   │   └── scripts/    # 可调用脚本
│   │   └── assets/     # 补充文件
│   └── vllm/
│       └── SKILL.md
├── devops/
│   └── deploy-k8s/     # Agent 创建的技能
│       └── SKILL.md
├── .hub/               # Skills Hub 状态
│   ├── lock.json
│   ├── quarantine/
│   └── audit.log
└── .bundled_manifest   # 内置技能清单
```

---

### 渐进式加载

Skills 使用"渐进式披露"节省 token：

```
Level 0: skills_list()
    → [{name, description, category}]
    → ~3k tokens（列表很小）

Level 1: skill_view(name)
    → 完整内容 + 元数据
    → 真正需要时才加载

Level 2: skill_view(name, path)
    → 特定参考文件
    → 查看模板/参考资料
```

---

### 使用 Skills

#### 通过 Slash 命令

```bash
/gif-search funny cats
/axolotl help me fine-tune Llama 3
/github-pr-workflow create a PR
/plan design a rollout
```

#### 通过自然对话

```bash
hermes chat --toolsets skills -q "What skills do you have?"
hermes chat --toolsets skills -q "Show me the axolotl skill"
```

---

### Agent 创建 Skills

Agent 使用 `skill_manage` 工具：

```python
# 创建新技能
skill_manage(
    action="create",
    name="deploy-api",
    content="...",  # 完整 SKILL.md 内容
    category="devops"
)

# 改进技能（推荐）
skill_manage(
    action="patch",
    name="deploy-api",
    old_string="Step 1: ...",
    new_string="Step 1: Improved version..."
)

# 大幅修改
skill_manage(
    action="edit",
    name="deploy-api",
    content="..."  # 完整替换
)

# 删除技能
skill_manage(action="delete", name="deploy-api")

# 添加参考文件
skill_manage(
    action="write_file",
    name="deploy-api",
    file_path="references/docker-cheatsheet.md",
    file_content="..."
)
```

---

### Skills Hub 命令

```bash
# 浏览
hermes skills browse                    # 所有 Hub 技能
hermes skills browse --source official  # 仅官方可选技能

# 搜索
hermes skills search kubernetes
hermes skills search react --source skills-sh
hermes skills search https://mintlify.com/docs --source well-known

# 检查
hermes skills inspect openai/skills/k8s

# 安装
hermes skills install openai/skills/k8s
hermes skills install official/security/1password
hermes skills install skills-sh/vercel-labs/json-render/json-render-react --force

# 管理
hermes skills list --source hub         # 已安装的 Hub 技能
hermes skills check                     # 检查上游更新
hermes skills update                    # 更新有变化的技能
hermes skills audit                     # 安全扫描
hermes skills uninstall k8s             # 移除

# 发布
hermes skills publish skills/my-skill --to github --repo owner/repo
```

---

### 条件激活 Skills

Skills 可以根据工具可用性自动显示/隐藏：

```yaml
metadata:
  hermes:
    fallback_for_toolsets: [web]      # web 工具集不可用时显示
    requires_toolsets: [terminal]     # terminal 工具集可用时显示
```

**示例：** DuckDuckGo 搜索技能
- 当有 FIRECRAWL_API_KEY → web 工具集可用 → DuckDuckGo 技能隐藏
- 当没有 API Key → web 工具集不可用 → DuckDuckGo 技能自动显示作为替代

---

### 安全扫描

所有 Hub 安装的技能都会通过安全扫描：
- 数据外泄检测
- 提示注入检测
- 破坏性命令检测
- 供应链风险信号

使用 `--force` 可覆盖非危险警告，但**不能覆盖危险判定**。

---

### Slash 命令（在对话中）

```bash
/skills browse
/skills search react --source skills-sh
/skills install openai/skills/skill-creator --force
/skills check
/skills update
/skills list
```

---

## 第四步：知识关联

### Skills 与其他系统的关系

```
┌─────────────────┐
│   Memory        │  ← 记住"我知道什么"
│   (事实记忆)    │
└─────────────────┘
        ↓
┌─────────────────┐
│   Skills        │  ← 记住"我会做什么"
│   (流程记忆)    │
└─────────────────┘
        ↓
┌─────────────────┐
│   Tools         │  ← 执行具体动作
│   (执行能力)    │
└─────────────────┘
```

| 关系 | 说明 |
|------|------|
| Memory vs Skills | Memory 是"事实"，Skills 是"流程" |
| Skills vs Tools | Skills 是"指导"，Tools 是"执行" |
| Skills Hub | 社区共享，agentskills.io 标准 |

### 相关文档

| 文档 | 内容 |
|------|------|
| [02-核心概念](02-核心概念.md) | Skills 在学习闭环中的位置 |
| [05-记忆与用户建模](05-记忆与用户建模.md) | Memory vs Skills 的对比 |
| [07-Cron调度](07-Cron调度.md) | Skill-backed Cron Jobs |

---

## 🎯 关键理解

1. **Skills 是流程记忆**：记住"怎么做"，不是"是什么"
2. **渐进式加载**：节省 token，只加载需要的部分
3. **Agent 自动创建**：复杂任务后自动创建，无需人工
4. **Skills Hub 共享**：社区技能，安全扫描后安装
5. **条件激活**：可以根据工具可用性自动显示/隐藏

---

*费曼学习法文档 - Hermes Agent*