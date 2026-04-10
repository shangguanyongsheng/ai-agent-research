# OpenClaw 最佳实践指南

> 来源：GitHub 社区 + 国外博主经验汇总

---

## 方案一：GitHub 社区最佳实践

来源：[garrettekinsman/openclaw-best-practices](https://github.com/garrettekinsman/openclaw-best-practices)

### 核心章节（v2 版本，23 个章节）

| 章节 | 内容 |
|------|------|
| **安全网关** | Firewall & Network Setup |
| **Skill 架构** | Keep It Slim（保持精简） |
| **上下文管理** | Context Window Management |
| **本地 AI 计算** | Local AI Compute |
| **集群构建** | Building a Cluster |
| **Sub-Agent 模式** | Sub-Agent Patterns |
| **记忆与连续性** | Memory & Continuity |
| **研究循环** | Research Loops: Adversarial Multi-Sprint |
| **Agent 人格** | Agent Personas |
| **信道集成** | Channel Integration & Communication |
| **系统管理工作流** | Sysadmin Workflows |
| **内容隔离** | Content Isolation & Trust Boundaries |
| **命令权限** | Command Authority & Access Control |
| **上下文图谱集成** | Context Graph Integration（v2 新增） |
| **会话上下文膨胀** | Session Context Bloat（v2 新增） |
| **Agent 团队协作** | Running Agent Teams（v2 新增） |
| **并行 Agent 工作流** | Parallel Agent Workflows（v2 新增） |
| **本地计算利用** | Leveraging Local Compute（v2 新增） |

### 关键洞察

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Context Graph Integration                                 │
│   → 语义检索引擎替代线性滑动窗口                             │
│   → 基于 DAG 的主题+时间组装                                │
│                                                             │
│   Session Context Bloat                                     │
│   → 长时间运行会话达到 100k+ tokens 的预防和恢复             │
│                                                             │
│   Running Agent Teams                                       │
│   → 命名人格、构建/审计循环、身份注入                       │
│   → 记忆访问策略、报告归属                                  │
│                                                             │
│   Parallel Agent Workflows                                  │
│   → Fan-out/Fan-in 研究、任务中转向                         │
│   → GPU 竞争管理、反模式                                    │
│                                                             │
│   Leveraging Local Compute                                  │
│   → 编排器模式、任务模型选择                                │
│   → LiteLLM 路由、VRAM 管理、PBAR 检查点                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 方案二：200+ 小时 Power User 经验

来源：[MindStudio - 14 Tips for Power Users](https://www.mindstudio.ai/blog/openclaw-best-practices-power-users-200-hours)

### Tips 1-3：架构设计先行

| Tip | 内容 |
|-----|------|
| **1. 画图再构建** | 构建前先画 Agent Graph，标明输入/输出/决策点 |
| **2. 单一职责** | 一个 Agent 做一件事，描述超过一句话就该拆分 |
| **3. 并行 Sub-Agent** | 独立任务并行执行，45 秒串行 → 20 秒并行 |

### Tips 4-6：模型路由优化

| Tip | 内容 |
|-----|------|
| **4. 匹配任务选模型** | 简单任务用便宜模型，复杂任务用昂贵模型 |
| **5. 专用 Router Agent** | 统一入口路由，方便更换模型和降级 |
| **6. 缓存重复查询** | 高频相同输入缓存输出，节省 30-50% 成本 |

**模型分层建议**：

| 任务类型 | 推荐模型 |
|----------|----------|
| 分类、路由、简单判断 | GPT-4o Mini / Claude Haiku / Gemini Flash |
| 结构化提取、摘要 | Mid-tier 模型 |
| 复杂推理、代码生成 | Frontier 模型（Opus/GPT-4） |

### Tips 7-8：Telegram 管理

| Tip | 内容 |
|-----|------|
| **7. 用 Threads 分离信号** | Errors / Completed / Approvals / Info 分开 |
| **8. 标准化消息格式** | 统一模板：`[STATUS] Agent Name\nTask: xxx\nResult: xxx` |

### Tips 9-10：Sub-Agent 可靠性

| Tip | 内容 |
|-----|------|
| **9. 传结构化 JSON** | Agent 间用 JSON 通信，定义 schema 并验证 |
| **10. 幂等设计** | 同样输入跑多次结果一样，防止重复邮件/记录 |

### Tips 11-12：Cron 稳定性

| Tip | 内容 |
|-----|------|
| **11. 错开 Cron 时间** | 不要都在整点跑，分散到 :00, :07, :15, :23, :34 |
| **12. 内置重试逻辑** | 重试次数、延迟、失败通知、恢复行为 |

### Tips 13-14：安全实践

| Tip | 内容 |
|-----|------|
| **13. 凭证不入代码** | 用环境变量，不用 prompt/workflow 存储 |
| **14. 季度权限审计** | 每三个月检查 Agent 权限、凭证有效性 |

---

## 常见错误与解决方案

来源：[Dev.to - 15+ Issues Covered](https://dev.to/kunpeng-ai-2026/openclaw-common-errors-and-solutions-15-issues-covered-2ofn)

### 安装错误

| 错误 | 解决方案 |
|------|----------|
| 下载失败 | 用国内镜像：`npm config set registry https://registry.npmmirror.com/` |
| Node.js 版本不对 | 需要 24.x，用 nvm 切换 |
| PowerShell 脚本禁止 | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| 安装卡住 | `openclaw logs --follow` 查看日志 |

### 运行时错误

| 错误 | 解决方案 |
|------|----------|
| 端口 8080 被占用 | `lsof -i :8080` 找进程 kill，或改端口 |
| 消息收不到 | 检查 `openclaw status`、Bot 在线、防火墙 |
| Telegram 群消息不收 | BotFather 关闭 Group Privacy |
| 飞书 Webhook 失败 | 需要 ICP 备案域名 + HTTPS |

### 性能优化

| 优化项 | 方法 |
|--------|------|
| 高延迟 | 用本地 Ollama，启用缓存 |
| 内存泄漏 | 限制上下文，定期重启 |
| SSL 过期 | `certbot renew` + cron 自动续期 |

---

## 最佳实践检查清单

### 安装前
- [ ] Node.js >= 24
- [ ] 端口 8080 空闲
- [ ] 网络连通

### 配置
- [ ] 每次 `openclaw config validate`
- [ ] 本地测试再上线
- [ ] 版本控制 `~/.openclaw/`

### 监控
- [ ] `openclaw logs --level error --follow`
- [ ] Cron 记录错误日志

### 安全
- [ ] 凭证用环境变量
- [ ] 季度权限审计
- [ ] 生产环境加审批步骤

---

## 资源链接

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.openclaw.ai |
| GitHub Issues | https://github.com/openclaw/openclaw/issues |
| Discord 社区 | https://discord.gg/clawd |
| 最佳实践仓库 | https://github.com/garrettekinsman/openclaw-best-practices |

---

*下一步：将本文档整合到 learning/openclaw/ 目录*