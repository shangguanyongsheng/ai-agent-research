# OpenClaw Skills 技能系统

> 使用费曼学习法：理解技能如何扩展 Agent 能力。

## 📖 概念解释

**什么是 Skill？**

Skill 是告诉 Agent "如何使用某个工具"的说明书。每个 Skill 是一个目录，包含：
- `SKILL.md`：技能定义和说明
- 其他辅助文件（脚本、参考资料等）

Agent 读取 Skill 后，就知道：
- 这个工具做什么
- 什么时候应该使用
- 怎么正确调用

## 🎯 类比理解

**把 Skill 想象成"烹饪食谱"**

- 食谱说明食材 → Skill 说明工具
- 食谱描述步骤 → Skill 描述调用方法
- 食谱有备注技巧 → Skill 有实践示例

就像厨师需要食谱来学习新菜品，Agent 需要 Skill 来学习新工具。没有 Skill，Agent 不知道怎么正确使用工具。

## 🔧 实践示例

### Skill 文件结构

```
skills/weather/
├── SKILL.md          # 必需：技能定义
├── tools.md          # 可选：工具参考
└── examples/         # 可选：示例数据
```

### SKILL.md 格式

```markdown
---
name: weather
description: 获取天气信息和预报
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "env": ["OPENWEATHER_API_KEY"] },
      },
  }
---

# Weather Skill

## 何时使用
用户询问天气、温度、降雨时使用此技能。

## 工具说明
- `weather_current`: 获取当前天气
- `weather_forecast`: 获取未来预报

## 使用示例
用户说："北京今天天气怎么样？"
调用：weather_current(location="北京")
```

**关键要素：**
- `name`: 技能名称（必需）
- `description`: 简短描述（必需）
- `metadata`: OpenClaw 特定元数据（可选）
- 正文：详细使用说明

### Skill 加载位置

OpenClaw 按优先级加载技能：

| 位置 | 说明 | 优先级 |
|------|------|--------|
| `<workspace>/skills` | 工作空间技能 | 最高 |
| `<workspace>/.agents/skills` | 项目 Agent 技能 | 高 |
| `~/.agents/skills` | 个人 Agent 技能 | 中 |
| `~/.openclaw/skills` | 本地覆盖 | 低 |
| bundled skills | 内置技能 | 更低 |
| `skills.load.extraDirs` | 额外目录 | 最低 |

**优先级规则：**
同名技能，优先级高的覆盖低的。

### 多 Agent 技能配置

不同 Agent 可以使用不同技能：

```json5
{
  agents: {
    defaults: {
      skills: ["github", "weather"],  // 默认技能包
    },
    list: [
      { id: "writer" },                    // 继承：github, weather
      { id: "docs", skills: ["docs-search"] }, // 替换：只有 docs-search
      { id: "locked-down", skills: [] },   // 无技能
    ],
  },
}
```

**规则：**
- 空数组 `[]` = 无技能
- 不写 `skills` = 继承默认
- 有内容 = 完全替换（不合并）

### 技能安装

#### 从 ClawHub 安装

```bash
# 安装技能到工作空间
openclaw skills install weather

# 更新所有已安装技能
openclaw skills update --all

# 查看技能列表
openclaw skills list
```

#### 使用 ClawHub CLI

```bash
# 同步并发布
clawhub sync --all
```

### 技能过滤（加载条件）

Skill 可以声明加载条件：

```markdown
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["uv"],              # 需要 uv 命令存在
          "env": ["GEMINI_API_KEY"],   # 需要环境变量
          "config": ["browser.enabled"] # 需要配置启用
        },
        "os": ["darwin", "linux"],     # 只在 macOS/Linux 加载
      },
  }
```

**过滤条件：**
- `bins`: PATH 中必须存在的命令
- `env`: 环境变量必须存在或配置中提供
- `config`: `openclaw.json` 中必须为真
- `os`: 只在指定操作系统加载

### 技能配置

在 `openclaw.json` 中配置技能：

```json5
{
  skills: {
    entries: {
      "weather": {
        enabled: true,                        // 启用/禁用
        apiKey: "YOUR_API_KEY",               # API 密钥
        env: { "OPENWEATHER_API_KEY": "..." }, # 环境变量注入
        config: { endpoint: "https://..." },   # 自定义配置
      },
      "github": { enabled: false },            // 禁用
    },
  },
}
```

**说明：**
- `enabled: false` = 即使安装也不加载
- `env` = 注入环境变量（如果未设置）
- `apiKey` = 对应 `primaryEnv` 声明的变量

## 🔗 知识关联

### Skills 与其他概念

| 概念 | 与 Skills 的关系 |
|------|------------------|
| Tools | Skills 教 Agent 如何使用 Tools |
| Plugins | Plugins 可以打包 Skills |
| Workspace | 每个 workspace 有独立的 skills 目录 |
| Agent | Agent 通过 skills 列表决定可用技能 |

### Skills 与 Plugins

插件可以自带技能：

```json
// openclaw.plugin.json
{
  "skills": ["./skills/plugin-skill"]
}
```

插件技能优先级较低，会被同名的工作空间技能覆盖。

### 技能市场

ClawHub（https://clawhub.ai）是公共技能注册中心：
- 浏览社区技能
- 安装到工作空间
- 发布自定义技能

## ⚠️ 安全注意事项

### 信任边界

**第三方技能 = 未信任代码**

建议：
1. 安装前阅读 Skill 内容
2. 检查 `SKILL.md` 中的指令
3. 对风险操作使用沙箱运行

### 敏感信息

- `skills.entries.*.env` 和 `apiKey` 注入到**主机进程**
- 不是注入到沙箱
- 密钥不会出现在日志或提示词中

### 沙箱执行

```json5
{
  agents: {
    defaults: {
      sandbox: { mode: "non-main" },  // 非主会话使用沙箱
    },
  },
}
```

## 📝 总结

Skill 就像烹饪食谱：
- 教 Agent 如何使用工具
- 包含使用时机和示例
- 可以声明加载条件

技能来源多样：
- 内置技能（bundled）
- ClawHub 安装
- 本地创建

技能管理：
- 按优先级加载
- 按 Agent 配置可见性
- 按条件过滤

下一步：[MCP 协议](./04-MCP协议.md) → 学习如何通过 MCP 扩展能力。

---

*费曼学习法：概念解释 → 类比理解 → 实践示例 → 知识关联*