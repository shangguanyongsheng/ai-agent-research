# OpenClaw 社区贡献指南

欢迎来到 OpenClaw 社区！本文档将帮助你了解如何参与 OpenClaw 项目的开发、贡献代码、创建技能（Skills），以及与社区互动。

---

## 目录

1. [OpenClaw 社区简介](#1-openclaw-社区简介)
2. [参与方式](#2-参与方式)
3. [Skills 开发](#3-skills-开发)
4. [社区资源](#4-社区资源)
5. [行为准则](#5-行为准则)

---

## 1. OpenClaw 社区简介

### 社区定位

OpenClaw 是一个开源的 AI Agent 框架，致力于让 AI 助手更加智能、可定制、易扩展。我们的社区由开发者、研究人员和 AI 爱好者组成，共同构建下一代 AI Agent 生态系统。

**核心理念：**

- **模块化设计**：通过 Skills（技能）系统，让 AI Agent 可以灵活扩展能力
- **开放协作**：所有代码开源，欢迎社区贡献
- **开发者友好**：提供完善的工具链和文档，降低开发门槛

### 核心价值观

| 价值观 | 说明 |
|--------|------|
| **开放** | 代码开源，决策透明，欢迎所有贡献者 |
| **协作** | 尊重每一位贡献者，鼓励知识共享和团队协作 |
| **创新** | 鼓励尝试新技术、新思路，推动 AI Agent 技术发展 |
| **质量** | 注重代码质量、文档完善和用户体验 |

### 社区资源

- **GitHub 仓库**：核心代码托管在 GitHub，是代码贡献的主要平台
- **ClawHub**：技能市场，发现和分享 Skills
- **Discord 社区**：实时交流、问题解答、技术讨论
- **文档站点**：完整的开发文档和使用指南

---

## 2. 参与方式

### 2.1 GitHub 贡献流程

OpenClaw 使用标准的 GitHub Flow 进行协作开发：

```
Fork → Clone → Branch → Commit → Push → Pull Request → Review → Merge
```

**步骤详解：**

1. **Fork 仓库**
   ```bash
   # 在 GitHub 页面点击 Fork 按钮
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/openclaw.git
   cd openclaw
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/issue-number-description
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   # 或
   git commit -m "fix: 修复问题描述 (#issue-number)"
   ```

5. **推送并创建 PR**
   ```bash
   git push origin feature/your-feature-name
   # 在 GitHub 页面创建 Pull Request
   ```

**提交信息规范：**

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加语音识别技能` |
| `fix` | Bug 修复 | `fix: 修复内存泄漏问题` |
| `docs` | 文档更新 | `docs: 更新安装指南` |
| `style` | 代码格式 | `style: 格式化代码` |
| `refactor` | 重构 | `refactor: 重构配置模块` |
| `test` | 测试 | `test: 添加单元测试` |
| `chore` | 其他 | `chore: 更新依赖版本` |

### 2.2 报告 Bug

发现 Bug？请通过 GitHub Issues 提交报告。

**Bug 报告模板：**

```markdown
## Bug 描述
简要描述遇到的问题

## 复现步骤
1. 执行命令 `openclaw start`
2. 配置文件设置...
3. 出现错误

## 期望行为
描述你期望发生什么

## 实际行为
描述实际发生了什么

## 环境信息
- OpenClaw 版本: vX.Y.Z
- 操作系统: macOS / Linux / Windows
- Node.js 版本: vX.Y.Z

## 日志输出
```
粘贴相关日志
```

## 截图
如有必要，添加截图帮助说明问题
```

**使用 GitHub CLI：**

```bash
gh issue create --title "Bug: 简要描述" --body "$(cat bug_template.md)"
```

### 2.3 提交 Feature Request

有新功能想法？我们很乐意听取你的建议！

**Feature Request 模板：**

```markdown
## 功能描述
清晰描述你希望添加的功能

## 问题背景
这个功能解决了什么问题？

## 建议方案
你希望如何实现这个功能？

## 替代方案
是否有其他可以考虑的方案？

## 附加信息
截图、原型图、参考链接等
```

### 2.4 贡献代码

**代码贡献最佳实践：**

1. **从小开始**：先从 Good First Issue 标签的问题开始
2. **阅读文档**：熟悉项目架构和编码规范
3. **保持简洁**：每个 PR 只解决一个问题
4. **添加测试**：确保代码质量
5. **更新文档**：如有必要，同步更新文档

**PR 检查清单：**

- [ ] 代码遵循项目风格指南
- [ ] 添加了必要的测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰规范
- [ ] PR 描述完整，关联了相关 Issue

---

## 3. Skills 开发

Skills 是 OpenClaw 的核心扩展机制。一个 Skill 是一个模块化的、自包含的能力包，为 AI Agent 提供专业知识、工作流和工具。

### 3.1 Skill 结构

```
my-skill/
├── SKILL.md           # 必需：技能定义文件
│   ├── YAML frontmatter (name, description)
│   └── Markdown 指令
├── scripts/           # 可选：可执行脚本
├── references/        # 可选：参考文档
└── assets/            # 可选：资源文件（模板、图标等）
```

### 3.2 创建 Skill

**Step 1: 初始化 Skill**

```bash
# 使用初始化脚本
scripts/init_skill.py my-skill --path ./skills

# 带资源目录
scripts/init_skill.py my-skill --path ./skills --resources scripts,references,assets

# 带示例文件
scripts/init_skill.py my-skill --path ./skills --examples
```

**Step 2: 编写 SKILL.md**

```markdown
---
name: my-skill
description: |
  简明扼要的技能描述。
  包含触发条件和适用场景。
  这是 AI 判断何时使用此技能的主要依据。
---

# My Skill

技能的详细说明和使用指南...

## 使用方法

具体的使用步骤...

## 示例

使用示例...
```

**YAML Frontmatter 要点：**

- `name`：技能名称，小写字母、数字和连字符
- `description`：触发描述，是 AI 判断是否使用的关键

**Step 3: 添加资源**

- `scripts/`：可执行脚本，用于需要确定性的任务
- `references/`：参考文档，按需加载
- `assets/`：资源文件，用于输出

**Step 4: 测试和打包**

```bash
# 验证和打包
scripts/package_skill.py ./skills/my-skill

# 指定输出目录
scripts/package_skill.py ./skills/my-skill ./dist
```

### 3.3 Skill 设计原则

| 原则 | 说明 |
|------|------|
| **简洁优先** | Context window 是公共资源，每个字都值得斟酌 |
| **适度约束** | 脆弱任务用脚本，灵活任务用指令 |
| **渐进披露** | 核心内容在 SKILL.md，详细内容在 references |
| **避免冗余** | 只包含必要文件，不创建多余的文档 |

**Context 分层加载：**

1. **Metadata**（始终加载）：`name` + `description`，约 100 字
2. **SKILL.md body**（触发时加载）：核心指令，建议 < 500 行
3. **Bundled resources**（按需加载）：无限制

### 3.4 发布到 ClawHub

ClawHub 是 OpenClaw 的技能市场，让你可以分享和发现 Skills。

**安装 ClawHub CLI：**

```bash
npm i -g clawhub
```

**认证：**

```bash
clawhub login
clawhub whoami
```

**发布 Skill：**

```bash
clawhub publish ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 1.0.0 \
  --changelog "首次发布"
```

**搜索和安装：**

```bash
# 搜索技能
clawhub search "postgres backups"

# 安装技能
clawhub install my-skill

# 安装特定版本
clawhub install my-skill --version 1.2.3

# 更新技能
clawhub update my-skill
clawhub update --all

# 列出已安装
clawhub list
```

### 3.5 Skill 最佳实践

1. **精准的 Description**
   - 描述技能做什么
   - 说明何时使用
   - 包含触发关键词

2. **合理的文件组织**
   ```
   bigquery-skill/
   ├── SKILL.md (概览和导航)
   └── references/
       ├── finance.md (财务指标)
       ├── sales.md (销售数据)
       └── marketing.md (营销分析)
   ```

3. **脚本优先处理脆弱操作**
   - 文件操作、API 调用用脚本
   - 需要灵活性的用自然语言指令

4. **避免过度文档化**
   - 不需要 README.md、CHANGELOG.md 等
   - SKILL.md 就是为 AI 服务的唯一文档

---

## 4. 社区资源

### 4.1 Discord 频道

Discord 是我们主要的实时交流平台。

**频道说明：**

| 频道 | 用途 |
|------|------|
| `#general` | 一般讨论和公告 |
| `#help` | 使用问题和帮助 |
| `#dev` | 开发者讨论 |
| `#showcase` | 展示你的项目 |
| `#skills` | Skills 开发交流 |

**加入方式：**
访问 [OpenClaw Discord](https://discord.gg/openclaw) 获取邀请链接。

### 4.2 文档站点

完整的文档托管在官方文档站点：

- **安装指南**：快速开始
- **配置参考**：详细配置选项
- **Skills 开发**：技能开发教程
- **API 参考**：开发者 API
- **最佳实践**：社区推荐做法

### 4.3 GitHub 仓库

- **OpenClaw Core**：核心框架代码
- **OpenClaw Skills**：官方技能仓库
- **Documentation**：文档源码

**常用操作：**

```bash
# 查看仓库状态
gh repo view openclaw/openclaw

# 列出 Issues
gh issue list --repo openclaw/openclaw --state open

# 查看 PR 状态
gh pr list --repo openclaw/openclaw

# 查看 CI 运行状态
gh run list --repo openclaw/openclaw --limit 5
```

### 4.4 ClawHub 技能市场

[ClawHub](https://clawhub.com) 是技能发现和分享的中心。

**功能：**

- 搜索和发现 Skills
- 版本管理
- 安装统计
- 作者信息

---

## 5. 行为准则

### 5.1 社区规范

我们致力于为所有人提供友好、安全和欢迎的环境。

**我们期望：**

- **尊重**：尊重不同的观点、经验和技能水平
- **包容**：欢迎不同背景的贡献者
- **协作**：乐于帮助他人，接受建设性反馈
- **专业**：保持专业和建设性的交流

### 5.2 禁止行为

以下行为将不被容忍：

| 行为类型 | 示例 |
|----------|------|
| **骚扰** | 骚扰性评论、人身攻击、不当言论 |
| **歧视** | 基于种族、性别、宗教等的歧视 |
| **恶意破坏** | 故意破坏代码、文档或社区资源 |
| **垃圾信息** | 发布无关或垃圾内容 |
| **隐私侵犯** | 未经同意分享他人私人信息 |
| **冒犯性内容** | 发布冒犯性或不雅内容 |

### 5.3 举报机制

如果你目睹或经历不当行为：

1. 通过 GitHub Issues 私密举报
2. 联系 Discord 管理员
3. 发送邮件至 abuse@openclaw.ai

我们会在 48 小时内回应举报。

---

## 附录：快速参考

### 常用命令

```bash
# ClawHub
clawhub search <query>
clawhub install <skill>
clawhub update --all

# GitHub CLI
gh issue create --title "..." --body "..."
gh pr create --title "..." --body "..."
gh pr checks <number>

# Skill 开发
scripts/init_skill.py <name> --path ./skills
scripts/package_skill.py <path>
```

### 相关链接

- 📚 文档：https://docs.openclaw.ai
- 💬 Discord：https://discord.gg/openclaw
- 🐙 GitHub：https://github.com/openclaw
- 🛒 ClawHub：https://clawhub.com

---

*感谢你参与 OpenClaw 社区！每一个贡献都让这个项目变得更好。*

---

**版本**: 1.0.0  
**最后更新**: 2025年1月