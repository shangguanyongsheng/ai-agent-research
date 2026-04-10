# Claude Code 学习文档整理进度

> 最后更新：2026-04-10 10:37

---

## 已抓取的官方内容

| 内容 | 来源 | 状态 | 整理文件 |
|------|------|------|----------|
| Auto Mode 安全机制 | Engineering Blog | ✅ 已整理 | `11-auto-mode-deep-dive.md` |
| Agent Patterns - Basic Workflows | Cookbook | 📝 待整理 | - |
| Agent Patterns - Orchestrator-Workers | Cookbook | 📝 待整理 | - |
| Agent Patterns - Evaluator-Optimizer | Cookbook | 📝 待整理 | - |
| Building Effective Agents | Engineering Blog | 📝 待整理 | - |
| Threat Intelligence Agent | Cookbook | 📝 待整理 | - |

---

## 文档体系规划

### 已有文档（旧）
```
01-getting-started.md      # 快速开始
02-core-concepts.md        # 核心概念
03-mcp-tools.md            # MCP 工具
04-skills-hooks.md         # Skills 和 Hooks
05-advanced.md             # 高级功能
06-best-practices.md       # 最佳实践
07-internal-architecture.md # 内部架构（源码分析）
08-architecture-nav.md     # 架构导航
09-practice-guide.md       # 落地实践
10-official-resources.md   # 官方资源导航
```

### 新增文档（整理中）
```
11-auto-mode-deep-dive.md  ✅ Auto Mode 深度解析
12-agent-patterns.md       📝 代理工作流模式详解
13-effective-agents.md     📝 构建有效代理
14-threat-intel-agent.md   📝 威胁情报代理实战
```

---

## 下一步

1. 整理 `12-agent-patterns.md`（合并 Basic Workflows + Orchestrator-Workers + Evaluator-Optimizer）
2. 整理 `13-effective-agents.md`（Building Effective Agents 完整内容）
3. 整理 `14-threat-intel-agent.md`（威胁情报代理实战案例）
4. 更新 `README.md` 导航，整合新文档
5. 提交到 GitHub

---

## 如何查看进度

```bash
# 查看进度文件
cat learning/claude-code/PROGRESS.md

# 查看所有文件
ls -la learning/claude-code/

# 查看最新文件内容
head -50 learning/claude-code/11-auto-mode-deep-dive.md
```