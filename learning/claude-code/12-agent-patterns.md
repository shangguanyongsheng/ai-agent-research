# Agent Patterns 工作流详解

> 来源：Claude Cookbook - Agent Patterns 系列

---

## 核心工作流模式总览

Anthropic 总结了 5 种核心 Agent 工作流模式：

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **Prompt Chaining** | 任务分解为固定步骤，顺序执行 | 可预测的固定流程 |
| **Routing** | 输入分类，路由到不同处理分支 | 多类别输入，需要分离关注点 |
| **Parallelization** | 并行执行多个子任务 | 需要多视角、提速 |
| **Orchestrator-Workers** | 中央 LLM 动态分解任务并委派 | 子任务不可预测 |
| **Evaluator-Optimizer** | 生成-评估循环，迭代优化 | 有明确评估标准 |

---

## 1. Prompt Chaining（串行流）

### 概念解释
把一个大任务拆成多个小步骤，按顺序执行，每一步的输出是下一步的输入。

### 类比理解
```
就像做菜：
1. 切菜 → 2. 炒菜 → 3. 装盘

每一步依赖上一步的结果。
中间可以加"检查点"确保没走偏。
```

### 适用场景
- 任务可以干净地分解为固定子任务
- 牺牲延迟换取更高准确率

### 示例
- 生成营销文案 → 翻译成其他语言
- 写大纲 → 检查大纲 → 写正文

---

## 2. Routing（路由分发）

### 概念解释
对输入进行分类，然后分发到不同的专门处理流程。

### 类比理解
```
就像客服中心：
- 账号问题 → 转账号组
- 账单问题 → 转账单组
- 技术问题 → 转技术组

不同问题用不同专长处理。
```

### 适用场景
- 复杂任务有明确分类
- 不同类别需要不同处理方式

### 示例：客服路由

```python
# 路由到不同分支
routes = ['billing', 'technical', 'account', 'product']

# 分析输入，选择路由
selected_route = classify_and_route(user_query)

# 执行对应的专门流程
response = process_with_specialist(selected_route, user_query)
```

---

## 3. Parallelization（并行处理）

### 概念解释
多个 LLM 同时工作，结果聚合。有两种变体：

- **Sectioning**：把任务拆成独立子任务并行执行
- **Voting**：同一任务多次执行，取多数结果

### 类比理解
```
Sectioning = 多人分工做不同菜，最后拼成一顿饭
Voting = 多人同时做同一道菜，选最好的一份
```

### 适用场景
- 子任务可以并行（提速）
- 需要多视角提高置信度

### 示例
- **Sectioning**：一个模型处理用户请求，另一个检查内容是否合规
- **Voting**：多个 prompt 同时审查代码漏洞，任一发现问题就标记

---

## 4. Orchestrator-Workers（编排-工作者）

### 概念解释
一个中央 LLM（Orchestrator）分析任务，动态决定需要什么子任务，然后委派给多个 Worker LLM 执行，最后汇总结果。

**关键区别**：子任务不是预先定义的，而是 Orchestrator 根据具体输入动态生成的。

### 类比理解
```
就像项目经理：
- 看到任务 → 分析需要什么工种
- 动态分配给设计师、开发、测试
- 汇报结果

不是固定分配，而是根据任务灵活调整。
```

### 适用场景
- 复杂任务，子任务无法预测
- 不同输入需要不同的分解策略

### 代码示例

```python
class FlexibleOrchestrator:
    def process(self, task: str, context: str = ""):
        # Phase 1: Orchestrator 分析并生成子任务
        orchestrator_prompt = f"""
        分析任务：{task}
        上下文：{context}

        确定需要哪些专门的处理方式。
        用 XML 格式输出子任务列表。
        """
        orchestrator_response = llm_call(orchestrator_prompt)
        tasks = self.parse_tasks(orchestrator_response)

        # Phase 2: Workers 执行每个子任务
        results = []
        for task in tasks:
            worker_prompt = f"""
            原始任务：{task['original']}
            你的子任务类型：{task['type']}
            指导：{task['description']}
            """
            result = llm_call(worker_prompt)
            results.append({"type": task['type'], "result": result})

        return results
```

### 实战案例：营销文案多风格生成

输入："为一个环保水瓶写营销文案"

Orchestrator 分析后生成 3 个子任务：
1. **技术规格风格** - 强调材料、认证、数据
2. **生活方式风格** - 情感故事、价值观
3. **实用利益风格** - 解决问题、日常便利

三个 Worker 分别生成，最后汇总。

---

## 5. Evaluator-Optimizer（评估-优化）

### 概念解释
一个 LLM 生成内容，另一个 LLM 评估并给出反馈，循环迭代直到满意。

### 类比理解
```
就像作家和编辑：
作家 → 写初稿
编辑 → 给反馈："这段逻辑不通"
作家 → 修改
编辑 → 再看："好了，通过"
```

### 适用场景
- 有明确评估标准
- 人类反馈能显著改进结果
- LLM 能提供有效反馈

### 代码示例

```python
def evaluator_optimizer_loop(task: str):
    memory = []

    # 生成初稿
    result = generate(task)

    while True:
        # 评估
        evaluation, feedback = evaluate(task, result)

        if evaluation == "PASS":
            return result

        # 根据反馈改进
        context = f"之前的尝试：{memory}\n反馈：{feedback}"
        result = generate(task, context)
        memory.append(result)
```

### 适用案例
- 文学翻译 - 评估者捕捉细节
- 复杂搜索任务 - 评估者决定是否继续搜索

---

## 如何选择合适的模式？

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   任务能固定分解？                                               │
│       │                                                         │
│       ├── 是 → Prompt Chaining                                  │
│       │                                                         │
│       └── 否 → 输入有明确类别？                                   │
│                 │                                               │
│                 ├── 是 → Routing                                │
│                 │                                               │
│                 └── 否 → 需要多视角/提速？                        │
│                           │                                     │
│                           ├── 是 → Parallelization              │
│                           │                                     │
│                           └── 否 → 子任务不可预测？               │
│                                     │                           │
│                                     ├── 是 → Orchestrator-Workers│
│                                     │                           │
│                                     └── 否 → 有评估标准？         │
│                                               │                 │
│                                               ├── 是 → Evaluator-│
│                                               │     Optimizer   │
│                                               │                 │
│                                               └── 否 → 可能不需要│
│                                                        Agent   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 重要原则

**Anthropic 的核心建议**：

> "成功不是构建最复杂的系统，而是构建适合你需求的系统。
> 从简单 prompt 开始，用评估优化，只有在简单方案不够时才添加多步骤 Agent 系统。"

**三大原则**：
1. 保持设计简单
2. 优先透明 - 显式展示规划步骤
3. 精心设计工具接口（ACI）

---

## 知识关联

- **Tools 设计** → 见 [03-mcp-tools.md](03-mcp-tools.md)
- **Subagents** → 见 [02-core-concepts.md](02-core-concepts.md)
- **Auto Mode** → 见 [11-auto-mode-deep-dive.md](11-auto-mode-deep-dive.md)

---

## 原文链接

- [Basic Workflows](https://platform.claude.com/cookbook/patterns-agents-basic-workflows)
- [Orchestrator-Workers](https://platform.claude.com/cookbook/patterns-agents-orchestrator-workers)
- [Evaluator-Optimizer](https://platform.claude.com/cookbook/patterns-agents-evaluator-optimizer)
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)