# 社区资源

> 🌐 GitHub、Discord、ClawHub 社区资源

---

## 第一步：概念解释

**OpenClaw 社区是什么？**
- 就像「业主俱乐部」
- 用户、开发者、贡献者聚集地
- 互助、分享、讨论

**类比**：
- GitHub = 工具仓库（源码、Issue）
- Discord = 聊天室（实时讨论）
- ClawHub = App Store（Skills 市场）
- Discussions = 论坛（深度讨论）

---

## 第二步：类比理解

| 平台 | 类比 | 用途 |
|------|------|------|
| GitHub Repo | 工具房 | 源码、Issue、PR |
| GitHub Discussions | 公告栏 | 深度讨论、问答 |
| Discord | 咖啡厅 | 实时聊天、求助 |
| ClawHub | App 商店 | Skills 发布下载 |

---

## 第三步：动手实践

### GitHub 资源

**仓库地址**：https://github.com/openclaw/openclaw

**主要内容**：
- 源代码
- Issue 追踪
- Pull Requests
- Release 版本

**如何使用**：

```bash
# 克隆源码
git clone https://github.com/openclaw/openclaw

# 查看最新版本
git log --oneline -5

# 提交 Issue
# https://github.com/openclaw/openclaw/issues/new
```

**GitHub Discussions**：
- https://github.com/openclaw/openclaw/discussions

**热门话题**：
- 配置最佳实践
- Skills 开发讨论
- 新功能建议
- Bug 报告

### Discord 社区

**邀请链接**：https://discord.gg/clawd

**频道结构**：

| 频道 | 内容 |
|------|------|
| `#general` | 一般讨论 |
| `#help` | 问题求助 |
| `#skills` | Skills 讨论 |
| `#announcements` | 发布公告 |
| `#dev` | 开发者讨论 |

**如何参与**：
1. 点击邀请链接
2. 加入 Discord 服务器
3. 在相应频道发言
4. 遵守社区规则

### ClawHub Skills 市场

**地址**：https://clawhub.ai

**功能**：
- 搜索 Skills
- 安装 Skills
- 发布自己的 Skills
- 查看热门 Skills

**使用 CLI**：

```bash
# 搜索 Skills
npx clawhub@latest search weather

# 安装 Skills
npx clawhub@latest install github

# 发布 Skills
npx clawhub@latest publish ./my-skill

# 更新 Skills
npx clawhub@latest update weather
```

---

## 第四步：知识关联

### 社区贡献方式

| 方式 | 说明 |
|------|------|
| 提交 Issue | 报告 Bug、建议功能 |
| 提交 PR | 修复 Bug、添加功能 |
| 编写 Skills | 开发并发布 Skills |
| 文档贡献 | 改进文档 |
| Discussions 讨论 | 分享经验 |
| Discord 帮助 | 回答他人问题 |

### 社区规范

**GitHub**：
- Issue 描述清晰
- 使用模板
- 提供复现步骤

**Discord**：
- 友好礼貌
- 在正确频道发言
- 不刷屏
- 遵守服务规则

**ClawHub**：
- Skills 有清晰描述
- 提供使用文档
- 版本号规范

---

## 官方文档

**地址**：https://docs.openclaw.ai

**文档结构**：

| 部分 | 内容 |
|------|------|
| Getting Started | 安装、快速上手 |
| Channels | 通道配置 |
| Gateway | 网关配置 |
| Tools | 工具使用 |
| Skills | Skills 系统 |
| Automation | 定时任务 |
| Security | 安全指南 |
| Help | 故障排查 |

**LLMs.txt 索引**：
- https://docs.openclaw.ai/llms.txt
- 完整文档索引，适合 AI 阅读

---

## 精选社区资源

### 热门 Skills

| Skill | 作者 | 用途 |
|-------|------|------|
| weather | 内置 | 天气查询 |
| github | 内置 | GitHub 操作 |
| coding-agent | 内置 | 代码任务 |
| agent-reach | 社区 | 多平台搜索 |
| video-frames | 社区 | 视频处理 |
| healthcheck | 内置 | 系统检查 |

### 社区最佳实践

**配置分享**：
- Discord `#tips` 频道
- GitHub Discussions "Show & Tell"

**Skills 开发教程**：
- https://docs.openclaw.ai/tools/creating-skills

**安全建议**：
- https://docs.openclaw.ai/gateway/security

---

## 获取帮助途径

| 问题类型 | 最佳途径 |
|----------|----------|
| Bug 报告 | GitHub Issue |
| 功能建议 | GitHub Discussions |
| 快速问答 | Discord `#help` |
| Skills 讨论 | Discord `#skills` |
| 深度讨论 | GitHub Discussions |
| 紧急问题 | Discord @mention 管理员 |

---

## 社区命令速查

```bash
# GitHub
git clone https://github.com/openclaw/openclaw

# ClawHub
npx clawhub@latest search <skill>
npx clawhub@latest install <skill>
npx clawhub@latest publish <skill-folder>

# Discord
# 加入: https://discord.gg/clawd
```

---

## 下一步

- [12-ClawHub Skills](./12-clawhub-skills.md) - Skills 推荐
- [03-Skills系统](./03-skills.md) - Skills 开发
- [官方文档](https://docs.openclaw.ai) - 完整文档

---

> ✅ 社区是学习和成长的最佳场所，积极参与！