# 07 - Multi-Agent 协作

> 多个 Agent 如何协同工作，完成复杂任务

---

## 🎯 概念解释

### 什么是 Multi-Agent 协作？

**简单说**：一个 Agent 做不了所有事，需要多个 Agent 分工合作。

就像公司里：
- 产品经理负责需求
- 架构师负责设计
- 开发负责实现
- 测试负责质量
- 运维负责部署

每个 Agent 有自己的专长，通过协作完成复杂项目。

### 为什么需要多 Agent？

| 场景 | 单 Agent 问题 | 多 Agent 解决 |
|------|--------------|--------------|
| 任务复杂 | Prompt 太长，效果差 | 拆分给专业 Agent |
| 上下文限制 | 记不住所有信息 | 每个 Agent 只关心自己领域 |
| 专业性 | 什么都懂 = 什么都不精 | 专精一个领域 |
| 并行执行 | 只能串行 | 多 Agent 可并行 |

---

## 🔄 协作模式

### 模式 1: 顺序协作（Pipeline）

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ PM      │───▶│ Dev     │───▶│ QA      │───▶│ Ops     │
│ 需求分析 │    │ 代码实现  │    │ 测试验证  │    │ 部署上线  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

**特点**：流水线式，前一个 Agent 的输出是后一个的输入

**代码示例**：

```python
class PipelineOrchestrator:
    """顺序协作编排器"""
    
    def __init__(self, agents: List[Agent]):
        self.agents = agents
    
    async def run(self, task: str) -> Result:
        context = {"task": task}
        
        for agent in self.agents:
            print(f"▶ 执行 {agent.name}...")
            result = await agent.execute(context)
            context.update(result)
        
        return context

# 使用
pipeline = PipelineOrchestrator([
    PMAgent(),      # 产品经理
    DevAgent(),     # 开发
    QAAgent(),      # 测试
    OpsAgent()      # 运维
])

result = await pipeline.run("开发一个用户登录功能")
```

### 模式 2: 层级协作（Hierarchy）

```
                    ┌─────────────┐
                    │  主 Agent   │
                    │  (协调者)    │
                    └──────┬──────┘
                           │ 分发任务
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
     ┌──────────┐   ┌──────────┐   ┌──────────┐
     │ Agent A  │   │ Agent B  │   │ Agent C  │
     │ 数据分析  │   │ 报告生成  │   │ 图表绘制  │
     └──────────┘   └──────────┘   └──────────┘
            │              │              │
            └──────────────┴──────────────┘
                           │ 汇总结果
                           ▼
                    ┌─────────────┐
                    │   最终输出   │
                    └─────────────┘
```

**特点**：主 Agent 负责任务分发和结果汇总

**代码示例**：

```python
class HierarchicalOrchestrator:
    """层级协作编排器"""
    
    def __init__(self, coordinator: Agent, workers: List[Agent]):
        self.coordinator = coordinator
        self.workers = workers
    
    async def run(self, task: str) -> Result:
        # 1. 主 Agent 分析任务，拆分子任务
        subtasks = await self.coordinator.execute({
            "task": task,
            "action": "decompose"
        })
        
        # 2. 分发给子 Agent 并行执行
        results = await asyncio.gather(*[
            worker.execute({"subtask": subtask})
            for worker, subtask in zip(self.workers, subtasks)
        ])
        
        # 3. 主 Agent 汇总结果
        final = await self.coordinator.execute({
            "action": "aggregate",
            "results": results
        })
        
        return final
```

### 模式 3: 对等协作（Peer-to-Peer）

```
┌──────────┐  消息  ┌──────────┐
│ Agent A  │◀──────▶│ Agent B  │
└────┬─────┘        └────┬─────┘
     │                   │
     │    请求/响应       │
     ▼                   ▼
┌──────────┐        ┌──────────┐
│ Agent C  │◀──────▶│ Agent D  │
└──────────┘  消息  └──────────┘
```

**特点**：Agent 之间直接通信，无中心协调

**代码示例**：

```python
class AgentBus:
    """Agent 消息总线"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.messages: asyncio.Queue = asyncio.Queue()
    
    def register(self, agent: Agent):
        self.agents[agent.name] = agent
    
    async def send(self, from_agent: str, to_agent: str, message: dict):
        await self.messages.put({
            "from": from_agent,
            "to": to_agent,
            "data": message
        })
    
    async def run(self):
        while True:
            msg = await self.messages.get()
            target = self.agents.get(msg["to"])
            if target:
                response = await target.handle_message(msg)
                # 可能触发新的消息
                if response:
                    await self.send(
                        msg["to"], 
                        response["to"], 
                        response["data"]
                    )
```

---

## 🤝 上下文共享

### 问题：每个 Agent 怎么知道其他 Agent 做了什么？

**方案 1: 共享记忆**

```python
class SharedMemory:
    """共享记忆系统"""
    
    def __init__(self):
        self.global_context = {}  # 所有 Agent 可见
        self.agent_contexts = {}  # Agent 私有
    
    def set_global(self, key: str, value: Any):
        """设置全局上下文"""
        self.global_context[key] = value
    
    def get_for_agent(self, agent_name: str) -> dict:
        """获取 Agent 可见的上下文"""
        return {
            **self.global_context,
            **self.agent_contexts.get(agent_name, {})
        }

# 使用
memory = SharedMemory()
memory.set_global("project_name", "Simple BI")

# Dev Agent 可以看到 project_name
dev_context = memory.get_for_agent("dev-agent")
```

**方案 2: 消息传递**

```python
class AgentMessage:
    """Agent 间消息"""
    from_agent: str
    to_agent: str
    action: str
    payload: dict
    context: dict  # 携带上下文

# Dev Agent 完成后通知 QA Agent
await bus.send(
    from_agent="dev-agent",
    to_agent="qa-agent",
    message={
        "action": "code_ready",
        "payload": {"files": ["main.py", "utils.py"]},
        "context": {"feature": "user-login"}  # 传递上下文
    }
)
```

---

## 🧠 类比理解

### 类比 1: 软件团队

| Agent 角色 | 职责 | 交互方式 |
|-----------|------|---------|
| 产品经理 | 需求分析 | PRD 文档 → 开发 |
| 架构师 | 技术设计 | 架构图 → 开发 |
| 开发 | 代码实现 | PR → 测试 |
| 测试 | 质量验证 | Bug 报告 → 开发 |
| 运维 | 部署上线 | 发布通知 → 产品 |

### 类比 2: 餐厅后厨

```
顾客点单 → 服务员记录 → 传菜员分发
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           炒菜师傅      凉菜师傅      甜点师傅
              │            │            │
              └────────────┴────────────┘
                           │
                           ▼
                        出餐
```

---

## 🔧 OpenClaw 多 Agent 实践

### 当前架构

```python
# OpenClaw Agent 配置
agents:
  main:
    model: dashscope/glm-5
    description: "主 Agent，处理用户交互"
  
  pm-agent:
    model: dashscope/glm-5
    description: "产品经理 Agent"
  
  dev-agent:
    model: dashscope/glm-5
    description: "开发 Agent"
  
  qa-agent:
    model: dashscope/glm-5
    description: "测试 Agent"
```

### 协作流程

```
用户 → main-agent → 判断任务类型
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      pm-agent      dev-agent     qa-agent
          │             │             │
          └─────────────┴─────────────┘
                        │
                        ▼
                   main-agent → 用户
```

---

## ⚠️ 多 Agent 挑战

### 挑战 1: 任务分配

**问题**：谁来决定哪个 Agent 做什么？

**解决**：
- Router Agent：专门负责任务分发
- 基于 Prompt 分类：LLM 判断任务类型

```python
class RouterAgent:
    """任务路由 Agent"""
    
    async def route(self, task: str) -> str:
        prompt = f"""
        分析任务类型，返回对应的 Agent：
        - 需求分析 → pm-agent
        - 代码实现 → dev-agent
        - 测试验证 → qa-agent
        
        任务：{task}
        """
        return await self.llm.generate(prompt)
```

### 挑战 2: 结果汇总

**问题**：多个 Agent 的结果如何合并？

**解决**：
- Aggregator Agent：专门负责汇总
- 结构化输出：每个 Agent 输出统一格式

```python
class AggregatorAgent:
    """结果汇总 Agent"""
    
    async def aggregate(self, results: List[dict]) -> dict:
        return {
            "summary": "汇总报告",
            "parts": results,
            "recommendations": [...]
        }
```

### 挑战 3: 错误传播

**问题**：一个 Agent 出错，整个流程失败？

**解决**：
- 错误隔离：每个 Agent 独立错误处理
- 重试机制：失败后重试或降级

```python
async def run_with_retry(agent: Agent, task: dict, max_retries: int = 3):
    for i in range(max_retries):
        try:
            return await agent.execute(task)
        except Exception as e:
            if i == max_retries - 1:
                return {"error": str(e), "agent": agent.name}
            await asyncio.sleep(1)  # 等待后重试
```

---

## 📊 状态：实现情况

| 功能 | 状态 | 说明 |
|------|------|------|
| Agent 配置 | ✅ 已实现 | 7 个 Agent 配置完成 |
| 顺序协作 | ⚠️ 部分 | 可通过 sessions_spawn 实现 |
| 层级协作 | 🔲 待开发 | 需要实现主 Agent 分发逻辑 |
| 对等协作 | 🔲 待开发 | 需要实现消息总线 |
| 共享记忆 | 🔲 待开发 | 当前为隔离模式 |
| 任务路由 | 🔲 待开发 | 需要 Router Agent |

---

## 💡 练习思考

1. **思考**：如果让你设计一个"自动化编程团队"，需要哪几个 Agent？

2. **实践**：尝试用 OpenClaw 的 `sessions_spawn` 实现 Agent 间调用：
   ```python
   # 在 main-agent 中调用 dev-agent
   result = await sessions_spawn(
       agentId="dev-agent",
       task="实现用户登录功能",
       mode="run"
   )
   ```

3. **挑战**：如何让 Agent 之间共享上下文而不冲突？

---

## 🔗 相关概念

- [ReAct 框架](./01-react-framework.md) - 单 Agent 内部循环
- [记忆系统](./02-memory-system.md) - 上下文存储
- [Hooks 机制](./05-hooks-mechanism.md) - Agent 间通信扩展点

---

*下一篇：[安全与沙箱](./08-safety-sandbox.md)*