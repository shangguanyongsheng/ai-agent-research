# Skills 和 Hooks

> ⏱️ 45 分钟 | 📍 第四章

[← 返回导航](README.md) | [上一章：MCP 工具连接](03-mcp-tools.md) | [下一章：高级功能 →](05-advanced.md)

---

## 知识点 3：内置 Skills（Bundled Skills）

> ⚠️ **重要**：这些是 Claude Code 自带的 Skills，无需配置即可使用！

### 第一步：概念解释（简单语言）

Claude Code 内置了几个常用的 Skills，开箱即用。这些是最常用的命令，帮你快速完成任务。

### 第二步：类比理解（生活例子）

就像手机自带的 App——不用安装就能用的相机、计算器、备忘录。内置 Skills 是 Claude Code 自带的"生产力工具"。

### 第三步：代码实践（动手实验）

| Skill | 用途 | 示例 |
|-------|------|------|
| `/batch <instruction>` | 并行批量处理 | `/batch 为每个文件添加 README` |
| `/debug [description]` | 调试当前会话 | `/debug 测试失败，帮我排查` |
| `/simplify [focus]` | 代码质量审查 | `/simplify 检查重复代码` |
| `/loop [interval] <prompt>` | 周期性执行 | `/loop 5m 检查部署状态` |

**`/batch` 详解**：

```text
> /batch 为 src/components/ 下的每个组件添加 PropTypes
```

Claude 会：
1. 找到所有组件文件
2. 并行处理每个文件
3. 汇总结果

**`/simplify` 详解**：

```text
> /simplify 分析 src/api/ 目录的代码复杂度
```

Claude 会：
1. 分析代码复杂度
2. 找出可简化的部分
3. 提供重构建议

### 第四步：知识关联

- 内置 Skills 是最快上手的方式
- 学会这些后，再创建自己的 Skills
- `/batch` 适合多文件操作，`/simplify` 适合代码审查

---

## 知识点 4：自定义 Skills

### 第一步：概念解释（简单语言）

除了内置 Skills，你可以创建自己的 `/command` 来封装重复的工作流程。

### 第二步：类比理解（生活例子）

就像在手机上创建"快捷指令"——一键完成多个步骤。比如"上班模式"会自动打开导航、播放播客、发送消息告诉家人你出发了。Skills 就是给 Claude Code 创建这样的"一键操作"。

### 第三步：代码实践（动手实验）

**创建一个 Skill**：

1. 创建目录：
```bash
mkdir -p ~/.claude/skills/review-pr
```

2. 创建 SKILL.md：
```markdown
---
name: review-pr
description: 审查当前 PR 并提供反馈
---

请帮我审查当前的 PR：

1. 使用 `gh pr view` 获取 PR 信息
2. 分析代码变更
3. 检查是否有：
   - 潜在的 bug
   - 代码风格问题
   - 安全风险
4. 提供改进建议

PR 编号：$ARGUMENTS
```

3. 使用：
```text
/review-pr 123
```

### 第四步：知识关联

- Skills 目录位置：`~/.claude/skills/` 或 `.claude/skills/`
- `$ARGUMENTS` 会被替换为命令后跟的参数
- Skills 可以调用 MCP 工具、执行命令、读取文件

---

## 知识点 2：Skills 目录结构

### 第一步：概念解释（简单语言）

每个 Skill 都是一个独立的目录，里面有一个 `SKILL.md` 文件定义这个命令做什么。

### 第二步：类比理解（生活例子）

就像每个工具都有自己的使用说明书——打开工具箱，找到对应的说明书，按照说明操作。

### 第三步：代码实践（动手实验）

**目录结构**：
```
~/.claude/skills/
├── review-pr/
│   └── SKILL.md           # PR 审查技能
├── deploy-staging/
│   └── SKILL.md           # 部署到测试环境
└── create-component/
    └── SKILL.md           # 创建组件模板
```

**SKILL.md 格式**：
```markdown
---
name: skill-name           # 命令名称（用于 /skill-name）
description: 描述          # Claude 会根据这个判断何时使用
disable-model-invocation: true  # 可选：禁止 Claude 自动触发
---

这里是你的提示词模板，可以使用 $ARGUMENTS 接收参数。
```

### 第四步：知识关联

- 个人 Skills：`~/.claude/skills/`
- 项目 Skills：`.claude/skills/`
- 项目 Skills 优先级更高

---

## 知识点 3：Hooks 是什么？

### 第一步：概念解释（简单语言）

**Hooks = 钩子**。在特定事件发生时自动执行的脚本。比如每次文件修改后自动格式化代码。

### 第二步：类比理解（生活例子）

就像设置"触发器"——门铃响了自动开灯，邮件收到了自动推送通知。Hooks 让 Claude Code 的操作自动触发你的脚本。

### 第三步：代码实践（动手实验）

**配置 Hooks**：

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

**Hook 类型**：

| 事件 | 说明 |
|------|------|
| `PreToolUse` | 工具执行前 |
| `PostToolUse` | 工具执行后 |
| `Notification` | 通知事件 |
| `Stop` | 会话结束时 |

**匹配器**：
```json
{
  "matcher": "Edit",           // 匹配 Edit 工具
  "matcher": "Bash",           // 匹配 Bash 命令
  "matcher": ".*",             // 匹配所有
  "matcher": "Edit|Bash"       // 匹配 Edit 或 Bash
}
```

### 第四步：知识关联

- `$FILE_PATH`：被编辑的文件路径
- `$TOOL_NAME`：工具名称
- `$TOOL_INPUT`：工具输入参数
- `$TOOL_OUTPUT`：工具输出结果

---

## 知识点 4：常用 Hooks 示例

### 第一步：概念解释（简单语言）

Hooks 可以自动化很多重复操作，让开发流程更顺畅。

### 第二步：类比理解（生活例子）

就像流水线上的自动检测——产品经过每个环节都有自动检查，确保质量。

### 第三步：代码实践（动手实验）

**示例 1：编辑后自动格式化**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

**示例 2：提交前运行 lint**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*git commit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint"
          }
        ]
      }
    ]
  }
}
```

**示例 3：发送通知**
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' '任务完成'"
          }
        ]
      }
    ]
  }
}
```

### 第四步：知识关联

- Hooks 可以组合使用
- 可以设置条件判断
- 注意不要设置太多 hooks 影响性能

---

## 知识点 5：Skills + Hooks 组合

### 第一步：概念解释（简单语言）

Skills 和 Hooks 可以配合使用，创建完整的自动化工作流。

### 第二步：类比理解（生活例子）

Skills 是"菜单"（定义要做什么），Hooks 是"自动化设备"（执行过程中的自动化）。

### 第三步：代码实践（动手实验）

**场景：自动化 PR 工作流**

Skill（`/review-pr`）：
```markdown
---
name: review-pr
description: 审查并修复 PR 问题
---

请帮我审查 PR #$ARGUMENTS：

1. 获取 PR 信息
2. 分析代码
3. 发现问题并修复
4. 更新 PR 描述
```

Hook（自动运行测试）：
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- --related --passWithNoTests"
          }
        ]
      }
    ]
  }
}
```

### 第四步：知识关联

- Skills 定义"做什么"
- Hooks 定义"过程中自动化什么"
- 配合 MCP 可以连接更多工具

---

## 总结检查清单

完成本章后，你应该能够：

- [ ] 创建自定义 Skill
- [ ] 配置 Hook
- [ ] 使用常用 Hooks 模式
- [ ] Skills 和 Hooks 组合使用

---

## 下一步

[下一章：高级功能 →](05-advanced.md)

学习调度任务、远程控制、Channels 等高级功能。