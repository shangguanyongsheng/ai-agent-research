# Claude Code 学习导航

> 🧭 你的 Claude Code 学习路线图

---

## 学习路径

| 序号 | 文件 | 内容 | 预计时长 |
|------|------|------|----------|
| 01 | [快速开始](01-getting-started.md) | 安装、配置、第一个任务 | 30 分钟 |
| 02 | [核心概念](02-core-concepts.md) | 代理型编码、斜杠命令、权限模式、Auto Memory | 45 分钟 |
| 03 | [MCP 工具连接](03-mcp-tools.md) | 连接外部工具、数据库、API | 60 分钟 |
| 04 | [Skills 和 Hooks](04-skills-hooks.md) | 内置 Skills、自定义工作流、自动化脚本 | 45 分钟 |
| 05 | [高级功能](05-advanced.md) | 调度任务、远程控制、Channels、Agent SDK | 60 分钟 |
| 06 | [最佳实践](06-best-practices.md) | Prompt 公式、CLAUDE.md 编写、效率技巧 | 30 分钟 |
| 07 | [内部架构](07-internal-architecture.md) | Agentic Loop、三层架构、Context Window | 45 分钟 |

---

## 费曼学习法

每个知识点都采用四步结构：

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   第一步：概念解释（简单语言）                                 │
│   → 用最简单的语言解释，像教给小孩                            │
│                                                             │
│   第二步：类比理解（生活例子）                                 │
│   → 用生活中的例子类比，建立直观理解                          │
│                                                             │
│   第三步：代码实践（动手实验）                                 │
│   → 实际动手操作或代码示例                                    │
│                                                             │
│   第四步：知识关联（与其他概念的关系）                         │
│   → 建立知识网络，理解概念间的联系                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 快速导航

### 我是新手，应该从哪里开始？

```
推荐路径：
1. 01-getting-started.md → 安装并运行第一个任务
2. 02-core-concepts.md → 理解 Claude Code 是什么
3. 06-best-practices.md → 学习如何写好 Prompt
4. 04-skills-hooks.md → 创建自定义工作流
```

### 我想连接外部工具

```
直接跳转：
→ 03-mcp-tools.md → MCP 连接指南
```

### 我想自动化重复任务

```
直接跳转：
→ 05-advanced.md → 调度任务、Channels
```

### 我想远程控制 Claude

```
直接跳转：
→ 05-advanced.md → 远程控制功能
```

---

## 官方资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://code.claude.com/docs/en/overview |
| 快速开始 | https://code.claude.com/docs/en/quickstart |
| MCP 文档 | https://code.claude.com/docs/en/mcp |
| CLI 参考 | https://code.claude.com/docs/en/cli-reference |
| 最佳实践 | https://code.claude.com/docs/en/best-practices |

---

## 学习检查清单

完成以下任务后，你就掌握了 Claude Code 的核心能力：

### ✅ 基础能力
- [ ] 安装并启动 Claude Code
- [ ] 使用 OAuth 登录
- [ ] 让 Claude 读取一个文件
- [ ] 让 Claude 编辑一个文件
- [ ] 让 Claude 运行一个命令

### ✅ 核心理解
- [ ] 理解"代理型编码"的含义
- [ ] 知道如何切换权限模式
- [ ] 使用斜杠命令（/clear、/compact、/status）
- [ ] 使用 @ 符号引用文件

### ✅ 进阶能力
- [ ] 配置一个 MCP 服务器
- [ ] 创建一个自定义 Skill
- [ ] 设置一个 Hook
- [ ] 使用 Remote Control
- [ ] 创建一个调度任务

---

## 知识图谱

```
                    Claude Code
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   核心概念           工具扩展          高级功能
        │                │                │
   ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
   │         │      │         │      │         │
 代理型    权限模式  MCP      Skills  调度任务  远程控制
   │         │      │         │      │         │
 会话管理  Plan模式  HTTP     Hooks   Channels  Agent SDK
           Auto    SSE      自定义   Web任务
           Accept  Stdio    工作流   Desktop
```

---

*开始你的学习之旅吧！[点击这里开始第一步](01-getting-started.md)*