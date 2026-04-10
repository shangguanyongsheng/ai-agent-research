# OpenClaw 高级模式

> 进阶使用模式与最佳实践

---

## 一、多 Agent 协作模式

### 模式 1：Orchestrator-Workers

```
┌─────────────┐
│ Orchestrator│  ← 中央协调器
│   (main)    │
└──────┬──────┘
       │
       ├──→ Worker 1 (doc-agent)
       ├──→ Worker 2 (dev-agent)
       └──→ Worker 3 (ops-agent)
```

**实现方式**：

```javascript
// 派发任务给多个子 Agent
const results = await Promise.all([
  sessions_spawn({ agentId: "doc-agent", task: "写文档" }),
  sessions_spawn({ agentId: "dev-agent", task: "写代码" }),
  sessions_spawn({ agentId: "ops-agent", task: "部署配置" })
]);
```

---

### 模式 2：Evaluator-Optimizer

```
Generator → Evaluator → 反馈 → Generator（改进）
```

**实现方式**：

```javascript
// 生成初稿
const draft = await sessions_spawn({ agentId: "doc-agent", task: "写初稿" });

// 评估
const review = await sessions_spawn({ agentId: "qa-agent", task: "审查初稿" });

// 根据反馈改进
const final = await sessions_spawn({ 
  agentId: "doc-agent", 
  task: `根据反馈改进：${review.feedback}` 
});
```

---

### 模式 3：Fan-out/Fan-in

```
        ┌→ Agent 1 ─┐
Task ───┼→ Agent 2 ─┼→ 汇总结果
        └→ Agent 3 ─┘
```

**适用场景**：
- 并行处理独立任务
- 多视角分析
- 数据采集汇总

---

## 二、进度反馈机制

### 标准格式

```markdown
# PROGRESS.md

> 最后更新：YYYY-MM-DD HH:MM

## 状态

**当前**：正在执行的任务
**状态**：进行中 / 等待 / 完成

## 进度

- [x] 已完成步骤 1
- [ ] 正在执行步骤 2
- [ ] 待执行步骤 3

## 预计完成时间

约 X 分钟
```

### 工作流程规范

| 规则 | 说明 |
|------|------|
| 边做边说 | 超过 5 分钟每步汇报 |
| 进度文件 | 更新 PROGRESS.md |
| 卡住上报 | 超过 2 分钟无进展通知 |

---

## 三、子 Agent 工作目录

### 问题

```
sessions_spawn 默认使用 agent 自己的 workspace

doc-agent       → workspace-doc-agent/
architect-agent → workspace-architect-agent/
main            → workspace/
```

### 解决方案

```javascript
// 指定共享目录
sessions_spawn({
  agentId: "doc-agent",
  cwd: "/home/admin/.openclaw/workspace",  // 共享目录
  task: "..."
})
```

---

## 四、权限分层设计

### 三级权限体系

| 层级 | 操作类型 | 处理方式 |
|------|----------|----------|
| **Tier 1** | 安全操作（读文件、搜索） | 直接放行 |
| **Tier 2** | 可逆操作（写文件、发消息） | 静默执行 |
| **Tier 3** | 危险操作（删除、远程命令） | 人工确认 |

### 实现建议

```json
// openclaw.json
{
  "agents": {
    "permissions": {
      "dangerousOperations": ["rm", "delete", "format"],
      "requireConfirmation": true
    }
  }
}
```

---

## 五、Context 管理

### Context Graph

替代线性滑动窗口：
- 基于 DAG 的主题 + 时间组装
- 保留关键信息，丢弃冗余
- 语义检索替代固定窗口

### 实现要点

```javascript
// 记忆关键信息
memory.set("key-insight", content, {
  importance: "high",
  expires: "never"
});

// 检索相关记忆
const relevant = memory.search("当前任务关键词");
```

---

## 六、自动化工作流

### Cron 最佳实践

```json
{
  "crons": [
    {
      "id": "daily-report",
      "schedule": "0 9 * * *",
      "agent": "doc-agent",
      "task": "生成每日报告",
      "timezone": "Asia/Shanghai"
    }
  ]
}
```

### 错开执行时间

```
错误：所有任务都在 :00 执行
正确：:00, :07, :15, :23, :34 分散执行
```

---

## 七、监控与告警

### 日志聚合

```bash
# 查看错误日志
openclaw logs --level error --tail 50

# 实时监控
openclaw logs --follow --level warn
```

### Telegram 告警

```json
{
  "channels": {
    "telegram": {
      "alertChatId": "-100XXXXXXXXXX",
      "alertLevels": ["error", "critical"]
    }
  }
}
```

---

## 八、性能优化

### 内存管理

```bash
# 检查内存
free -h

# 清理缓存
sync && echo 3 > /proc/sys/vm/drop_caches
```

### 并发控制

```json
{
  "agents": {
    "maxConcurrent": 2,
    "queueSize": 10
  }
}
```

---

## 九、安全最佳实践

### 凭证管理

```bash
# 使用环境变量
export GITHUB_TOKEN="xxx"

# 在配置中引用
{
  "credentials": {
    "github": "${GITHUB_TOKEN}"
  }
}
```

### 权限最小化

```json
{
  "agents": {
    "permissions": {
      "filesystem": {
        "readOnly": ["/etc", "/var/log"],
        "readWrite": ["/home/admin/workspace"]
      }
    }
  }
}
```

---

## 十、故障排查清单

### 常见问题

| 问题 | 检查项 | 解决方案 |
|------|--------|----------|
| Agent 无响应 | `openclaw status` | 重启 Gateway |
| 消息未送达 | `openclaw logs` | 检查 Channel 配置 |
| Cron 未执行 | `openclaw cron list` | 检查时区和 schedule |
| 内存不足 | `free -h` | 清理或升级配置 |

---

## 知识关联

- **基础安装** → 见 [01-installation.md](01-installation.md)
- **Skills 系统** → 见 [03-skills.md](03-skills.md)
- **安全实践** → 见 [09-security.md](09-security.md)
- **ClawHub Skills** → 见 [12-clawhub-skills.md](12-clawhub-skills.md)

---

*高级用户必读*