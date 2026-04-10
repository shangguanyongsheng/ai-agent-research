# ClawHub Skills 推荐指南

> ClawHub 是 OpenClaw 的 Skills 市场，提供丰富的社区贡献技能

---

## 第一步：概念解释

**ClawHub 是什么？**

ClawHub 是 OpenClaw 的官方 Skills 市场：
- 发现和安装社区贡献的 Skills
- 一键安装，无需手动配置
- 支持 API 集成、自动化、数据分析等各类场景

**地址**：https://clawhub.ai

---

## 第二步：类比理解

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ClawHub = 手机应用商店                                    │
│                                                             │
│   Skills = App                                              │
│   → 浏览分类、评分、下载量                                   │
│   → 一键安装                                                │
│   → 自动更新                                                │
│                                                             │
│   没有 ClawHub：                                            │
│   → 手动下载 SKILL.md                                       │
│   → 手动配置路径                                            │
│   → 手动更新                                                │
│                                                             │
│   有 ClawHub：                                              │
│   → openclaw skill install xxx                              │
│   → 自动完成一切                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第三步：热门 Skills 推荐

### 生产效率类

| Skill | 功能 | 安装命令 |
|-------|------|----------|
| **github** | GitHub 操作（PR、Issue、CI） | `openclaw skill install github` |
| **weather** | 天气查询 | `openclaw skill install weather` |
| **coding-agent** | 编码任务委托 | `openclaw skill install coding-agent` |

### 数据处理类

| Skill | 功能 | 安装命令 |
|-------|------|----------|
| **searxng** | 本地搜索引擎 | `openclaw skill install searxng` |
| **agent-reach** | 多平台搜索（Twitter、Reddit等） | `openclaw skill install agent-reach` |
| **video-frames** | 视频帧提取 | `openclaw skill install video-frames` |

### 运维监控类

| Skill | 功能 | 安装命令 |
|-------|------|----------|
| **healthcheck** | 服务器安全检查 | `openclaw skill install healthcheck` |
| **mcporter** | MCP 工具管理 | `openclaw skill install mcporter` |

---

## 第四步：使用 ClawHub CLI

### 安装 Skill

```bash
# 搜索 Skills
openclaw skill search <关键词>

# 安装 Skill
openclaw skill install <skill-name>

# 查看已安装 Skills
openclaw skill list

# 更新 Skill
openclaw skill update <skill-name>

# 卸载 Skill
openclaw skill uninstall <skill-name>
```

### 发布自己的 Skill

```bash
# 初始化 Skill 项目
openclaw skill init my-skill

# 发布到 ClawHub
openclaw skill publish
```

---

## 第五步：创建自定义 Skill

### 目录结构

```
my-skill/
├── SKILL.md          # Skill 定义（必需）
├── skill.json        # 元数据（可选）
├── scripts/          # 脚本文件
├── references/       # 参考文档
└── assets/           # 静态资源
```

### SKILL.md 模板

```markdown
# My Skill

## 描述

这个 Skill 的功能说明。

## 触发条件

- 关键词：xxx
- 场景：xxx

## 执行步骤

1. 步骤一
2. 步骤二

## 示例

用户输入 → Skill 输出
```

---

## 第六步：社区贡献

### 如何贡献

1. Fork 官方 Skills 仓库
2. 创建你的 Skill
3. 提交 Pull Request
4. 审核通过后发布到 ClawHub

### 贡献规范

- 遵循 SKILL.md 格式规范
- 提供清晰的描述和使用示例
- 包含必要的测试用例
- 保持向后兼容

---

## 知识关联

- **Skills 基础** → 见 [03-skills.md](03-skills.md)
- **MCP 协议** → 见 [04-mcp.md](04-mcp.md)
- **高级模式** → 见 [13-advanced-patterns.md](13-advanced-patterns.md)

---

## 资源链接

| 资源 | 链接 |
|------|------|
| ClawHub 官网 | https://clawhub.ai |
| Skills 文档 | https://docs.openclaw.ai/skills |
| GitHub 仓库 | https://github.com/openclaw/skills |

---

*持续更新中...*