# Multi-Agent 协作

> 知识分支：advanced（进阶主题）

---

## 🎯 学习目标

理解多个 Agent 如何协作完成复杂任务。

---

## 第一步：概念解释

### Multi-Agent 是什么？

**给小孩解释**：
> 一个 Agent 可能不够聪明，但多个 Agent 组成团队就很厉害了！就像一个公司有产品经理、开发、测试、运维，各司其职。

**一句话定义**：
> Multi-Agent = 多个专业 Agent 分工协作，像团队一样完成任务。

### 协作架构

```
┌─────────────────────────────────────────────────────┐
│                 主 Agent (Router)                    │
│                  任务分发 + 结果汇总                  │
└─────────────────────────────────────────────────────┘
        │           │           │           │
        ▼           ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│ PM-Agent  │ │ Dev-Agent │ │ QA-Agent  │ │ Ops-Agent │
│ 产品经理   │ │ 开发工程师 │ │ 测试工程师 │ │ 运维工程师 │
├───────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ 需求调研  │ │ 代码实现   │ │ 测试用例   │ │ CI/CD     │
│ PRD 编写  │ │ 架构设计   │ │ 自动化测试 │ │ 部署监控  │
└───────────┘ └───────────┘ └───────────┘ └───────────┘
```

### Agent 角色定义

| Agent | 角色 | 职责 | 技能 |
|-------|------|------|------|
| pm-agent | 产品经理 | 需求调研、PRD 编写 | github, web_search |
| dev-agent | 开发工程师 | 代码实现、功能开发 | coding, git |
| qa-agent | 测试工程师 | 测试用例、质量报告 | coding, pytest |
| ops-agent | 运维工程师 | CI/CD、部署、监控 | docker, kubernetes |

---

## 第二步：类比理解

### 类比：软件开发团队

| Multi-Agent | 软件团队 |
|-------------|---------|
| 主 Agent | 技术经理 |
| PM-Agent | 产品经理 |
| Dev-Agent | 开发人员 |
| QA-Agent | 测试人员 |
| Ops-Agent | 运维人员 |

### 类比：医院科室

| Multi-Agent | 医院 |
|-------------|------|
| 主 Agent | 分诊台 |
| 专业 Agent | 各科室医生 |
| 任务分发 | 转诊 |
| 结果汇总 | 会诊 |

---

## 第三步：协作流程

### 标准 DevOps 流程

```
1. PM-Agent：需求调研
   ↓ 输出 PRD 文档
   
2. Architect-Agent：架构设计
   ↓ 输出技术方案
   
3. Dev-Agent：代码开发
   ↓ 输出代码 + PR
   
4. QA-Agent：测试验证
   ↓ 输出测试报告
   
5. Ops-Agent：部署上线
   ↓ 输出部署结果
```

### 任务路由代码示例

```python
def route_task(task_type, task_content):
    """根据任务类型路由到不同的 Agent"""
    
    routing_table = {
        "需求调研": "pm-agent",
        "代码开发": "dev-agent",
        "测试验证": "qa-agent",
        "部署上线": "ops-agent",
    }
    
    target_agent = routing_table.get(task_type, "default-agent")
    
    # 调用子 Agent
    result = await sessions_spawn(
        agentId=target_agent,
        task=task_content,
        mode="run"
    )
    
    return result
```

---

## 第四步：知识关联

### Multi-Agent 在知识体系中的位置

```
AI Agent 知识体系
│
├── foundation
│   └── 单个 Agent 的能力是协作的基础
│
├── tools
│   └── sessions_spawn 是调用子 Agent 的工具
│
├── evolution
│   └── EvoMap 可以共享多 Agent 的知识
│
└── advanced ◄── 你在这里
    └── Multi-Agent 协作
```

---

## 🧪 动手实验

### 实验：模拟 Multi-Agent 协作

```bash
# 使用 sessions_spawn 调用子 Agent
# 例如：让 dev-agent 实现一个功能

# 在 OpenClaw 中
> 请让 dev-agent 帮我实现用户登录功能

# 观察：
# 1. 主 Agent 分析任务
# 2. 路由到 dev-agent
# 3. dev-agent 执行任务
# 4. 返回结果给主 Agent
```

---

## ❓ 思考题

1. 为什么需要多个 Agent 协作？一个 Agent 不能完成所有任务吗？
2. 如何设计 Agent 之间的通信协议？
3. Multi-Agent 协作可能遇到什么问题？

---

## 📚 延伸阅读

- [EvoMap](../evolution/evomap.md) - Agent 知识共享
- [原始文档](../../docs/simple-bi-multi-agent-plan.md) - 完整方案
- [技术文档](../../learning/07-multi-agent-collaboration.md) - 详细实现

---

_📅 更新日期：2026-03-23_
_🐒 毛猴子整理_