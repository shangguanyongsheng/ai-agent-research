# Skills 技能系统

> 🎯 Skills 让 Agent 学会新能力

---

## 第一步：概念解释

**Skill 是什么？**
- 就像给 Agent 安装「App」
- 每个 Skill 是一组预设的工具和提示
- 让 Agent 学会：
  - 查天气
  - 写代码
  - 搜索网页
  - 控制智能家居

**类比**：
- Agent = 手机
- Skill = App
- ClawHub = App Store

---

## 第二步：类比理解

| 场景 | Skill 作用 |
|------|------------|
| 查天气 | 调用天气 API，返回结果 |
| 写代码 | 启动子 Agent，执行 Codex |
| 搜索网页 | 使用搜索工具，返回摘要 |
| 发送邮件 | 调用邮件插件，完成发送 |

**Skill 组成**：

```
Skill/
├── SKILL.md        # Agent 使用说明
├── scripts/        # 可执行脚本
├── references/     # 参考文档
└── assets/         # 静态资源
```

---

## 第三步：动手实践

### 安装 Skill

**从 ClawHub 安装**：
```bash
# 使用 clawhub CLI
npx clawhub@latest install weather

# 或直接克隆
cd ~/.openclaw/skills
git clone https://github.com/example/weather-skill weather
```

**内置 Skills**：
- `github` - GitHub 操作
- `weather` - 天气查询
- `coding-agent` - 代码任务
- `browser` - 浏览器控制
- `healthcheck` - 系统检查

### 配置 Skills

在 `openclaw.json` 中：

```json5
{
  agents: {
    defaults: {
      skills: ["github", "weather"],  // 默认加载的 Skills
    },
  },
}
```

**按 Agent 配置**：
```json5
{
  agents: {
    list: [
      { id: "main", skills: ["github", "weather"] },
      { id: "dev", skills: ["coding-agent", "github"] },
      { id: "minimal", skills: [] },  // 无 Skills
    ],
  },
}
```

### 使用 Skill

Agent 收到消息后，会：
1. 匹配 Skill 描述
2. 读取 SKILL.md
3. 按说明使用工具

**示例对话**：
```
用户: 北京今天天气怎么样？
Agent: [读取 weather SKILL.md]
       [调用天气 API]
       北京今天晴，25°C...
```

---

## 创建自己的 Skill

### Skill 结构

```
my-skill/
├── SKILL.md        # 必须 - Agent 指导
├── scripts/
│   └── my-tool.sh  # 可选 - 工具脚本
└── references/
    └── docs.md     # 可选 - 参考文档
```

### SKILL.md 模板

```markdown
# My Skill

## Description
一句话描述，用于 Agent 匹配。

## When to use
触发条件：
- 用户说 "XXX"
- 用户问 "XXX"

## How it works
执行步骤：
1. 调用工具 A
2. 处理结果
3. 返回用户

## Examples
示例对话。

## Scripts
可用的脚本命令。
```

### 安装本地 Skill

```bash
# 放到 skills 目录
mkdir -p ~/.openclaw/skills/my-skill
# 创建 SKILL.md 等

# 配置启用
openclaw config set agents.defaults.skills '["my-skill"]'
```

---

## 第四步：知识关联

### Skills vs MCP vs Plugins

| 概念 | 说明 | 关系 |
|------|------|------|
| Skill | Agent 指导包 | 包含 MCP 工具、脚本 |
| MCP | 工具协议 | Skill 可调用 MCP 服务器 |
| Plugin | 通道/提供商扩展 | 系统级扩展 |

### Skills 配置详解

```json5
{
  skills: {
    entries: {
      "weather": {
        path: "~/.openclaw/skills/weather",
        enabled: true,
      },
      "github": {
        path: "~/.openclaw/skills/github",
        enabled: true,
        apiKey: "${GITHUB_TOKEN}",  // 可配置 API Key
      },
    },
  },
}
```

### Skills 市场访问

**ClawHub** (https://clawhub.ai):
- 搜索 Skills
- 安装 Skills
- 发布自己的 Skills

```bash
# 搜索
npx clawhub@latest search weather

# 安装
npx clawhub@latest install weather

# 发布
npx clawhub@latest publish ./my-skill
```

---

## 常用 Skills 推荐

| Skill | 用途 | 安装 |
|-------|------|------|
| weather | 天气查询 | 内置 |
| github | GitHub 操作 | 内置 |
| coding-agent | 代码任务 | 内置 |
| browser | 浏览器自动化 | 内置 |
| agent-reach | 多平台搜索 | clawhub install |
| video-frames | 视频帧提取 | clawhub install |
| healthcheck | 系统健康检查 | 内置 |

---

## Skills 工作原理

```
用户消息
    ↓
Agent 收到
    ↓
检查 available_skills 描述
    ↓
匹配相关 Skill
    ↓
读取 SKILL.md
    ↓
按指导调用工具
    ↓
返回结果给用户
```

---

## 下一步

- [04-MCP协议](./04-mcp.md) - MCP 工具协议详解
- [12-ClawHub Skills](./12-clawhub-skills.md) - ClawHub Skills 推荐
- [创建 Skills](https://docs.openclaw.ai/tools/creating-skills) - 官方教程

---

> ✅ Skills 是扩展 Agent 能力的核心方式，就像给手机安装 App。