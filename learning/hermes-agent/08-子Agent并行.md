# 08-子Agent并行

> 理解 Hermes 的子 Agent 系统：spawn subagents、RPC 调用、并行处理。

---

## 第一步：概念解释

### 什么是子 Agent？

**子 Agent（Subagent）** 是 Hermes 创建的独立 Agent 实例，用于：
- 并行处理多个任务
- 隔离工作流（不影响主对话）
- 异步执行长任务

---

### 两种方式

| 方式 | 说明 | 用途 |
|------|------|------|
| **delegate_task** | Agent 调用工具，创建子 Agent | 自动并行处理 |
| **/background** | 用户命令，后台运行任务 | 用户主动触发 |
| **execute_code RPC** | Python 代码调用 Agent | 程序化控制 |

---

## 第二步：类比理解

### 子 Agent = 临时助手

主 Agent → 负责与用户对话
子 Agent → 临时助手，处理具体任务

**类比：**

```
用户："帮我检查 5 个服务器的状态"

传统方式：
Agent 一个一个检查，用户等待...

有子 Agent：
Agent："我派 5 个助手并行检查"
→ 同时检查 5 个服务器
→ 收集结果汇报给用户
```

### execute_code RPC = 批量处理

```python
# 在 execute_code 中可以调用 Agent
# 像 Python 代码调用外部 API

results = []
for url in urls:
    # 子 Agent 处理单个 URL
    result = agent_call(prompt=f"Summarize {url}")
    results.append(result)
```

---

## 第三步：代码/实践

### /background 命令

```bash
/background Check all servers in the cluster and report any that are down
```

**特点：**
- 独立会话，不影响主对话
- 继承当前模型/工具配置
- 完成后自动返回结果

**确认消息：**

```
🔄 Background task started: "Check all servers..."
Task ID: bg_143022_a1b2c3
```

---

### delegate_tool 工具

```python
# Agent 自动调用
delegate_task(
    prompt="Research competitor pricing and create a table",
    toolsets=["web", "file"],
)
```

**返回：**
- 子 Agent 的最终响应
- 完成状态

---

### execute_code RPC

在 `execute_code` sandbox 中，可以调用 Hermes Agent：

```python
# 示例：批量处理多个任务
from hermes_rpc import call_agent

tasks = [
    "Summarize the first article from https://example.com/blog",
    "Check if server 192.168.1.100 is reachable",
    "Extract contact info from https://company.com",
]

results = []
for task in tasks:
    result = call_agent(
        prompt=task,
        toolsets=["web", "terminal"],
    )
    results.append(result)

# 合并结果
final_summary = "\n\n".join(results)
```

**优势：**
- 多步流水线变成单次推理
- 无 context 成本
- 可编程控制

---

### 子 Agent 的隔离性

| 特性 | 说明 |
|------|------|
| **独立会话** | 无主对话历史 |
| **独立工具集** | 可指定特定工具 |
| **独立状态** | 不影响主 Agent |
| **异步执行** | 主对话继续 |

---

### 用途

| 场景 | 示例 |
|------|------|
| **服务器监控** | 检查集群所有服务器 |
| **长时间构建** | 部署时主对话继续 |
| **研究任务** | 竞品分析，批量处理 |
| **文件操作** | 批量整理文件 |

---

## 第四步：知识关联

### 子 Agent 与其他系统的关系

```
┌─────────────────┐
│   主 Agent      │  ← 与用户对话
│   (Gateway/CLI) │
└─────────────────┘
        ↓ spawn
┌─────────────────┐
│   子 Agent      │  ← 独立执行
│   (异步/并行)   │
└─────────────────┘
        ↓ RPC
┌─────────────────┐
│   execute_code  │  ← 程序化调用
│   (Python)      │
└─────────────────┘
```

### 相关概念

| 概象 | 关系 |
|------|------|
| [架构详解](03-架构详解.md) | delegate_tool.py |
| [Cron 调度](07-Cron调度.md) | Cron 也创建新 Agent（类似子 Agent） |
| [Skills](04-Skills系统.md) | 子 Agent 可加载特定 Skills |

---

## 🎯 关键理解

1. **子 Agent 是独立的**：无主对话历史，不影响主对话
2. **并行处理**：可同时处理多个任务
3. **异步执行**：主对话继续，结果自动返回
4. **RPC 调用**：execute_code 中可编程控制
5. **工具集指定**：可限制子 Agent 的能力

---

## 📋 最佳实践

### 选择合适的任务

```markdown
✅ 适合子 Agent：
- 批量检查多个服务器
- 长时间运行的任务（不影响主对话）
- 研究任务（需搜索多个来源）
- 可并行化的任务

❌ 不适合：
- 需要主对话上下文的任务
- 需要即时交互的任务
```

### 使用 Skills 提供上下文

```python
delegate_task(
    prompt="Check deployment status",
    skills=["deploy-k8s"],  # 加载技能提供上下文
)
```

### 合理使用工具集

```python
# 只给子 Agent 需要的工具
delegate_task(
    prompt="Research competitor pricing",
    toolsets=["web"],  # 只需 Web 工具
)
```

---

*费曼学习法文档 - Hermes Agent*

> 注：官方文档对子 Agent 的详细说明较少，更多细节可参考架构文档中的 `delegate_tool.py`。